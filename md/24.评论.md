在没有互联网的年代，我们用日记来记录每天的心得体会。小的时候我有一个带锁的日记本，生怕被别人看见里面写了啥，钥匙藏得那叫一个绝。

现在时代变了，网络版的日记本：博客，却巴不得越多人看越好。

别人看完你写的深度好文，难免也想高谈阔论一番，这就是“评论”功能。

本章将要编写的评论模块，几乎没有新的知识点，而是将前面章节内容的综合应用。

**强烈建议读者自行尝试编写这部分内容，测试自己的知识掌握程度。**

## 准备工作

评论是一个相对独立的功能，因此新建一个评论的app：

```bash
(env) E:\django_project\my_blog > ppython manage.py startapp comment
```

> 有的人觉得奇怪，没有博文就没有评论，为什么说评论是“独立”的功能？
>
> 那是因为不仅博文可以评论，照片、视频甚至网站本身都可以“被评论”。将其封装成单独的模块方便以后的扩展。

确认app创建成功后，记得在`settings.py`中注册：

```python
my_blog/settings.py

...
INSTALLED_APPS = [
    ...
    'comment',
]
...

TIME_ZONE = 'Asia/Shanghai'

...
```

因为我们想显示发表评论的时间，修改时区设置`TIME_ZONE`为上海的时区。

然后在`my_blog/urls.py`中注册根路由：

```python
my_blog/urls.py

...
urlpatterns = [
    ...
    # 评论
    path('comment/', include('comment.urls', namespace='comment')),
]
...
```

## 编写核心功能

### 评论的模型

首先编写评论的模型：

```python
comment/models.py

from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost

# 博文的评论
class Comment(models.Model):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]
```

模型中共有2个外键：

- `article`是被评论的文章
- `user`是评论的发布者

别忘了每次新增、修改Model后，必须**数据迁移**。

> 提示：你必须先在setting.py中注册app，这个app中的数据迁移才能生效

### 评论的表单

用户提交评论时会用到表单，因此**新建**表单类：

```python
comment/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
```

因为模型中的2个外键将通过视图逻辑自动填写，所以这里只需要提交`body`就足够了。

### 评论的url

在comment app中**新建**路由文件：

```python
comment/urls.py

from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
]
```

评论必须关联在某篇具体的博文里，因此传入博文的`id`，方便后续调用。

`post_comment()`视图还没写，先取个名字占位置。

### 评论的视图

评论的视图函数如下：

```python
comment/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm

# 文章评论
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")
```

**代码中有2个新面孔。**

`get_object_or_404()`：它和`Model.objects.get()`的功能基本是相同的。区别是在生产环境下，如果用户请求一个不存在的对象时，`Model.objects.get()`会返回`Error 500`（服务器内部错误），而`get_object_or_404()`会返回`Error 404`。相比之下，返回404错误更加的准确。

`redirect()`：返回到一个适当的url中：即用户发送评论后，重新定向到文章详情页面。当其参数是一个Model对象时，会自动调用这个Model对象的`get_absolute_url()`方法。因此接下来马上修改`article`的模型。

> 实际上之前的章节已经用过`redirect()`了。功能是相同的，实现上略有区别。

### 文章的模型

按照上面说的，在文章模型中添加`get_absolute_url()`方法：

```python
article/models.py

...
# 记得导入
from django.urls import reverse

class ArticlePost(models.Model):
    ...

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
```

通过`reverse()`方法返回文章详情页面的url，实现了路由重定向。

### 文章详情视图

评论模块需要在**文章详情**页面展示，所以必须把评论模块的上下文也传递到模板中。

因此修改`article/views.py`中的`article_detail()`：

```python
article/views.py

...

from comment.models import Comment

def article_detail(request, id):
    # 已有代码
    article = ArticlePost.objects.get(id=id)

    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    ...
    
    # 添加comments上下文
    context = { 'article': article, 'toc': md.toc, 'comments': comments }

    ...
```

> `filter()`可以取出多个满足条件的对象，而`get()`只能取出1个，注意区分使用

### 文章详情模板

到最后一步了，坚持。所有后台的功能已经写完了，就差把所有这些展现到页面中了。

修改文章详情页面：

```html
templates/article/detail.html

...

<div class="col-9">
    ...
    <!-- 已有代码，文章正文 -->
    <div class="col-12">
        ...
    </div>

    <!-- 发表评论 -->
    <hr>
    {% if user.is_authenticated %}
        <div>
            <form 
                action="{% url 'comment:post_comment' article.id %}" 
                method="POST"
            >
            {% csrf_token %}
                <div class="form-group">
                    <label for="body">
                        <strong>
                            我也要发言：
                        </strong>
                    </label>
                    <textarea 
                        type="text" 
                        class="form-control" 
                        id="body" 
                        name="body" 
                        rows="2"></textarea>
                </div>
                <!-- 提交按钮 -->
                <button type="submit" class="btn btn-primary ">发送</button>                    
            </form>
        </div>
        <br>
    {% else %}
        <br>
        <h5 class="row justify-content-center">
            请<a href="{% url 'userprofile:login' %}">登录</a>后回复
        </h5>
        <br>
    {% endif %}
    


    <!-- 显示评论 -->
    <h4>共有{{ comments.count }}条评论</h4>
    <div>
        {% for comment in comments %}
            <hr>
            <p>
                <strong style="color: pink">
                    {{ comment.user }}
                </strong> 于 
                <span style="color: green">
                    {{ comment.created|date:"Y-m-d H:i:s" }}
                </span> 时说：
            </p>
            <pre style="font-family: inherit; font-size: 1em;">
{{ comment.body }}</pre>
        {% endfor %}
    </div>
</div>

<!-- 目录 -->
<div class="col-3 mt-4">
    ...
</div>

...
```

- 表单组件中的`action`指定数据提交到哪个url中

- 显示评论中的`comments.count`是模板对象中内置的方法，对包含的元素进行计数

- `|date:"Y-m-d H:i :s"`：管道符你已经很熟悉了，用于给对象“粘贴”某些属性或功能。这里用于格式化日期的显示方式。请尝试修改其中的某些字符试试效果。

- `<pre>`定义预格式化的文本，在我们的项目中最关键的作用是保留空格和换行符。该标签会改变文字的字体、大小等，因此用`style`属性重新定义相关内容。尝试将`<pre>`替换为`div`，输入多行文本试试效果。

  > 之前说代码最好不要复制粘贴，否则有些“小坑”你是留意不到的。比如在`<pre>`标签中的文本千万不能缩进。

## 测试

又到了激动人心的测试环节了。

登录自己的账户，进入某个文章详情页面，发现已经可以进行留言了：

![](https://www.dusaiphoto.com/media/image/image_source/20190101/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE137.jpg)

如果退出登录，显示提示语：

![](https://www.dusaiphoto.com/media/image/image_source/20190101/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE138.jpg)

点击登录就回到登录页面。

评论模块的发布、展示功能就搞定了。

### 扫尾工作

数据的删、改功能我们已经做过很多遍，这里不打算再赘述了。

评论同样也可以支持Markdown语法，或者插入Emoji表情符号。

读者可以自己去实现感兴趣的功能。

> 有些网站干脆就没有删除、更新评论的功能。因为对小站来说，这些功能用到的次数太少太少了，不如把精力用在更有价值的地方去。比如[我的博客](https://www.dusaiphoto.com/)就没有。
>
> 还有的网站提供软删除，删除后仅仅是不显示而已，实际上数据还存在。
>
> 具体应该如何做，都以你的喜好而定。

## 总结

本章实现了发表评论、展示评论的功能。像开头说的一样，本章的内容是前面所学章节的综合。

如果你没有看本章代码，而是完全靠自己完成了评论功能，那么恭喜你获得了**“Django入门程序员”**的称号！不要小看“入门”两字，万事开头难嘛。

- 有疑问请在[杜赛的个人网站](http://www.dusaiphoto.com)留言，我会尽快回复。
- 或Email私信我：dusaiphoto@foxmail.com
- 项目完整代码：[Django_blog_tutorial](https://github.com/stacklens/django_blog_tutorial)

> 转载请注明出处。