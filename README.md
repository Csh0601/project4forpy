# Django博客系统

## 项目简介

基于Django 5.2开发的功能完整的博客系统，实现Python程序设计课程Project 4

## 功能特性

### 核心功能（作业要求）

- ✅ **BlogPost模型**：包含title、text、date_added、owner字段
- ✅ **用户认证系统**：注册、登录、登出功能
- ✅ **文章CRUD操作**：创建、展示、编辑、删除文章
- ✅ **权限保护**：只有文章作者可以编辑和删除自己的文章
- ✅ **时间排序**：文章按发布时间倒序显示

### 扩展功能

- 🏷️ **标签系统**：支持文章分类和标签筛选
- 💬 **评论功能**：用户可以发表和删除评论
- ❤️ **点赞功能**：支持AJAX实时点赞/取消点赞
- 🖼️ **图片上传**：文章可添加封面图片
- 🔍 **全文搜索**：支持标题和内容搜索
- 👤 **用户主页**：显示用户统计信息（文章数、点赞数、评论数）
- 📄 **分页显示**：首页文章列表分页展示

## 技术栈

- **后端框架**：Django 5.2
- **数据库**：SQLite3
- **前端框架**：Bootstrap 5
- **图片处理**：Pillow
- **前端交互**：JavaScript（AJAX）

## 安装运行

### 环境要求

- Python 3.8+
- pip

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 运行开发服务器

```bash
python manage.py runserver
```

### 5. 访问系统

- **前台首页**：http://127.0.0.1:8000/
- **Admin后台**：http://127.0.0.1:8000/admin/

## 项目结构

```
blogs/                  # Django项目根目录
├── Blog/               # 项目配置
│   ├── settings.py     # 全局配置文件
│   ├── urls.py         # 主路由配置
│   └── wsgi.py         # WSGI部署配置
├── blogs/              # 博客应用
│   ├── models.py       # 数据模型（BlogPost、Tag、Comment）
│   ├── views.py        # 视图函数（CRUD+扩展功能）
│   ├── forms.py        # 表单类（BlogPostForm、CommentForm）
│   ├── urls.py         # 应用路由配置
│   ├── admin.py        # Admin后台配置
│   └── templates/      # HTML模板文件
│       └── blogs/
│           ├── base.html           # 基础模板
│           ├── index.html          # 首页
│           ├── post_detail.html   # 文章详情
│           ├── new_post.html      # 新建文章
│           ├── edit_post.html     # 编辑文章
│           ├── delete_post.html   # 删除确认
│           ├── search_results.html # 搜索结果
│           ├── tag_posts.html     # 标签文章
│           └── user_profile.html  # 用户主页
├── accounts/           # 用户认证应用
│   ├── views.py        # 注册视图
│   ├── urls.py         # 认证路由
│   └── templates/      # 认证模板
│       └── registration/
│           ├── login.html         # 登录页面
│           ├── register.html      # 注册页面
│           └── logged_out.html    # 登出页面
├── media/              # 媒体文件目录（用户上传的图片）
│   └── post_images/    # 文章封面图片
├── db.sqlite3          # SQLite数据库文件
├── manage.py           # Django管理脚本
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明文档
```

## 数据模型

### BlogPost（博客文章）

| 字段       | 类型                  | 说明                    |
| ---------- | --------------------- | ----------------------- |
| title      | CharField             | 文章标题（最大200字符） |
| text       | TextField             | 文章内容                |
| date_added | DateTimeField         | 发布时间（自动添加）    |
| owner      | ForeignKey(User)      | 文章作者                |
| tags       | ManyToManyField(Tag)  | 文章标签（多对多）      |
| likes      | ManyToManyField(User) | 点赞用户（多对多）      |
| views      | PositiveIntegerField  | 浏览量                  |
| image      | ImageField            | 文章封面图              |

### Tag（标签）

| 字段 | 类型      | 说明             |
| ---- | --------- | ---------------- |
| name | CharField | 标签名称（唯一） |

### Comment（评论）

| 字段       | 类型                 | 说明     |
| ---------- | -------------------- | -------- |
| post       | ForeignKey(BlogPost) | 关联文章 |
| author     | ForeignKey(User)     | 评论作者 |
| content    | TextField            | 评论内容 |
| created_at | DateTimeField        | 评论时间 |

## 主要功能说明

### 用户认证

- **注册**：新用户注册并自动登录
- **登录**：已注册用户登录访问
- **登出**：安全退出登录

### 文章管理

- **创建文章**：登录用户可发布新文章，支持添加标签和封面图
- **编辑文章**：只能编辑自己的文章（权限验证）
- **删除文章**：只能删除自己的文章（权限验证）
- **浏览文章**：所有访客可浏览文章，自动增加浏览量

### 社交功能

- **评论**：登录用户可发表评论，只能删除自己的评论
- **点赞**：登录用户可点赞/取消点赞，支持AJAX实时更新
- **用户主页**：查看用户的文章、点赞、评论统计

### 搜索与筛选

- **全文搜索**：搜索标题和内容
- **标签筛选**：点击标签查看相关文章
- **分页显示**：首页每页显示5篇文章

## 权限说明

| 操作     | 游客 | 登录用户 | 文章作者 |
| -------- | ---- | -------- | -------- |
| 浏览文章 | ✅   | ✅       | ✅       |
| 发布文章 | ❌   | ✅       | ✅       |
| 编辑文章 | ❌   | ❌       | ✅       |
| 删除文章 | ❌   | ❌       | ✅       |
| 发表评论 | ❌   | ✅       | ✅       |
| 点赞文章 | ❌   | ✅       | ✅       |

## 功能截图展示

### 1. Django Admin后台管理

Django Admin提供完善的后台管理界面，支持对Blog posts、Comments、Tags的完整CRUD操作。

![Admin后台首页](pics%20+%20requires/b03944302ad5db6201efccd8f4688654.png)

### 2. 发布新文章

登录用户可以发布新文章，支持输入标题、内容、上传封面图片、添加标签。

![发布新文章](pics%20+%20requires/4ebde2e40c1284776fc24e24683a5c68.png)

### 3. 编辑文章（权限保护）

只有文章作者可以编辑自己的文章，系统会验证用户权限。

![编辑文章](pics%20+%20requires/5b2c8713571c0a988f2efc6a0081b371.png)

### 4. 文章详情页（点赞/评论/标签）

文章详情页展示完整内容，支持点赞、评论、显示浏览量和标签。

![文章详情](pics%20+%20requires/3afd18108ae7702f5ec20a062c2bf230.png)

### 5. 用户注册

新用户可以注册账号，注册后自动登录。

![用户注册](pics%20+%20requires/70217143b031ed5406656005fb390546.png)

### 6. 用户登录

已注册用户可以登录系统。

![用户登录](pics%20+%20requires/84d7c1d0a504cc11416ff3daaabf27d9.png)

### 7. 用户个人主页

用户主页显示统计信息（文章数、点赞数、评论数）和文章列表。

![用户主页](pics%20+%20requires/23339f826fa86a56f3044074b84fb6f1.png)

## 作业要求完成情况

### Project 4-1: Blog

- ✅ 创建Django项目Blog，包含blogs应用
- ✅ 创建BlogPost模型（title、text、date_added）
- ✅ 创建superuser
- ✅ 注册模型到Admin
- ✅ 按时间倒序显示所有文章
- ✅ 创建新文章表单
- ✅ 创建编辑文章表单

### Project 4-5: Protected Blog

- ✅ BlogPost关联User（owner字段）
- ✅ 所有人可以浏览文章
- ✅ 只有注册用户可以发布文章
- ✅ 只有文章作者可以编辑自己的文章
- ✅ 编辑前验证用户权限（post.owner == request.user）

## 作者

陈铄涵 - 2024140014

## 课程信息

- **课程**：Python程序设计
- **日期**：2025年12月
