from django.shortcuts import render

# 导入数据模型ArticlePost
from .models import ArticlePost

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
	# 需要传递给模板的对象
	context = { 'article': article }
	# 载入模板，并返回context对象
	return render(request, 'article/detail.html', context)