from django.db import models

# Django本身具有一个简单又完整的账号系统（User），足以满足一般网站的账号申请、建立、权限、群组等基本功能
# 因此这里导入内建的User模型，以便使用。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

# Django中所有的模型(Model)都必须继承django.db.models.Model模型，即顶部的导入
# 建立博客文章类 class Article，处理与文章有关的数据，它包含需要的字段和保存数据的行为
class ArticlePost(models.Model):

    # 定义文章作者。 author 通过 models.ForeignKey 外键与内建的 User 模型关联在一起
    # 参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。通常设置为 CASCADE 级联删除就可以了
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。
    # models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    # CharField 有一个必填参数 max_length，它规定字符的最大长度
    title = models.CharField(max_length=100)

    # 文章正文。
    # 保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。 
    # DateTimeField 为一个日期字段
    # 参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。
    # 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    # 元数据：不是一个字段的任何数据
    class Meta:
    	# ordering 指定模型返回的数据的排列顺序
    	# '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    # 它最常见的就是在Django管理后台中做为对象的显示值。因此应该总是为 __str__ 返回一个友好易读的字符串
    def __str__(self):
    	# return self.title 将文章标题返回
        return self.title