[![](https://img.shields.io/badge/python-3.7.0-orange.svg)](https://www.python.org/downloads/release/python-370/)
[![](https://img.shields.io/badge/django-2.1-green.svg)](https://docs.djangoproject.com/en/2.1/releases/2.1/)
[![](https://img.shields.io/badge/bootstrap-4.1.3-blue.svg)](https://getbootstrap.com/docs/4.1/getting-started/introduction/)
[![](https://img.shields.io/badge/license-MIT-000000.svg)](https://opensource.org/licenses/MIT)

# Django搭建个人博客教程

这是面向新人的**Django搭建个人博客教程**的项目代码。

**教程为零基础的小白准备，目的是快速搭建一个博客网站。**

点击下面的链接前往教程：

[Django搭建个人博客](https://www.dusaiphoto.com/article/detail/2/)

教程内容包括：
- [搭建开发环境](https://www.dusaiphoto.com/article/detail/4/)
- [博客文章管理](https://www.dusaiphoto.com/article/detail/11/)
- [用户管理](https://www.dusaiphoto.com/article/detail/31/)
- [文章分页、统计浏览量及搜索](https://www.dusaiphoto.com/article/detail/42/)
- [评论功能](https://www.dusaiphoto.com/article/detail/49/)
- [以及其他功能](https://www.dusaiphoto.com/article/detail/53/)

## 教程特点
- 零基础、免费、中文、完整项目代码
- 基于最新的Python3.7、Django2.1和Bootstrap4版本
- **博主热情的技术支持！**

## 适合人群
- 拥有一台能开机的电脑
- 有一点点最基础的python编程知识
- 每天能抽出一个小时学习

不要犹豫，现在立刻开始Django的学习吧！

## 联系方式
- 简单问题，请在[杜赛的个人网站](https://www.dusaiphoto.com)留言
- 复杂问题，请Email私信我：dusaiphoto@foxmail.com

## 注意事项
不含依赖项（如Django框架、Pillow等模块），安装方式如下。

解压项目后，在项目目录创建**虚拟环境**：

```bash
python -m venv env
```

运行**虚拟环境**（Windows环境）:

```bash
env\Scripts\activate.bat
```

或（Linux环境）：

```bash
source env/bin/activate
```

然后输入：

```bash
pip install -r requirements.txt
```

即可自动安装所有依赖项。

## 更新列表
### 2019.01.29
- 文章栏目

### 2019.01.16
- 基于类的视图

### 2019.01.01
- 结束和开始
- 评论

### 2018.12.30
- 文章目录
- 搜索

### 2018.12.28
- 现在包含static目录了
- 最热文章
- 文章浏览量

### 2018.12.20
- 文章分页

### 2018.12.05

- 扩展用户信息
- 上传头像

### 2018.11.03

- 用户登录、登出
- 用户注册
- 用户删除
- 密码重置

### 2018.10.20

- 编写更新文章的功能

### 2018.10.08

- 使用Markdown语法书写文章
- 删除文章功能

### 2018.09.27

- 使用Form表单类发表新文章

### 2018.09.16

- 用bs改写了模板文件
- 增加了查看文章详情功能

### 2018.08.25
- 创建了项目
- 创建了article应用
- 编写了article模型