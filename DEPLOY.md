# 部署说明

## 本地测试

1. **进入项目目录**
   ```bash
   cd new
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务**
   ```bash
   python run.py
   ```

4. **访问系统**
   - 本地：http://localhost:8080
   - 局域网：http://你的IP:8080

## 部署到Railway

### 方法1：通过GitHub部署（推荐）

1. **创建GitHub仓库**
   - 访问 https://github.com
   - 点击 "New repository"
   - 仓库名称：question-bank-system
   - 选择 "Public"
   - 点击 "Create repository"

2. **上传代码到GitHub**
   ```bash
   cd new
   git init
   git add .
   git commit -m "Initial commit: 多用户题库系统 v2.0"
   git branch -M main
   git remote add origin https://github.com/你的用户名/question-bank-system.git
   git push -u origin main
   ```

3. **Railway部署**
   - 登录Railway: https://railway.app
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择您的仓库
   - 点击 "Deploy Now"

### 方法2：直接上传文件

1. **准备文件**
   - 确保new目录包含所有必要文件
   - 检查文件完整性

2. **Railway部署**
   - 登录Railway: https://railway.app
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 如果看到 "Deploy from directory" 选项，选择它
   - 拖拽new文件夹到上传区域
   - 点击 "Deploy Now"

## 环境变量设置

部署完成后，在Railway项目设置中添加：
- `PORT` = 8080

## 访问地址

部署完成后，您将获得类似地址：
```
https://your-app-name.railway.app
```

## 注意事项

1. **文件完整性检查**
   - app.py - Flask主应用
   - run.py - 启动脚本
   - requirements.txt - Python依赖
   - full_questions.json - 题库数据
   - templates/ - HTML模板目录
   - static/ - 静态资源目录

2. **部署后测试**
   - 访问登录页面
   - 注册新用户
   - 测试多选题功能
   - 验证用户数据隔离

3. **常见问题**
   - 如果部署失败，检查requirements.txt中的依赖版本
   - 确保所有文件都已上传
   - 检查部署日志中的错误信息

## 更新部署

如果需要更新代码：

1. **修改代码后提交到GitHub**
   ```bash
   git add .
   git commit -m "Update: 描述更新内容"
   git push
   ```

2. **Railway会自动重新部署**
   - Railway会检测到GitHub仓库的更新
   - 自动触发重新部署
   - 无需手动操作

## 系统功能验证

部署完成后，请验证以下功能：

- ✅ 用户注册和登录
- ✅ 多选题多选功能
- ✅ 个人数据隔离
- ✅ 错题记录和统计
- ✅ 模拟考试功能
- ✅ 响应式界面设计 