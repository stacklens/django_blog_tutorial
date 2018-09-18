from django.shortcuts import render
# 导入数据模型ArticlePost
from .models import ArticlePost

# 引入markdown模块
import markdown

# 文章列表
def article_list(request):
	# 取出所有博客文章
	articles = ArticlePost.objects.all()
	# 需要传递给模板（templates）的对象
	context = { 'articles': articles }
	# render函数：载入模板，并返回context对象
	return render(request, 'article/list.html', context)

# 文章详情
def article_detail(request, id):
	# 取出相应的文章
	article = ArticlePost.objects.get(id=id)

	# 将markdown语法渲染成html样式
	article.body = markdown.markdown(article.body,
		extensions=[
		# 包含 缩写、表格等常用扩展
		'markdown.extensions.extra',
		# 语法高亮扩展
		'markdown.extensions.codehilite',
		])

	# 需要传递给模板的对象
	context = { 'article': article }
	# 载入模板，并返回context对象
	return render(request, 'article/detail.html', context)