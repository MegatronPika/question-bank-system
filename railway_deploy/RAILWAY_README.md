# Railway部署说明

## 方法1：通过GitHub部署（推荐）

### 步骤1：创建GitHub仓库
1. 访问 https://github.com
2. 点击 "New repository"
3. 仓库名称：question-bank-system
4. 选择 "Public"
5. 点击 "Create repository"

### 步骤2：上传代码
在项目目录中执行：
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/您的用户名/question-bank-system.git
git push -u origin main
```

### 步骤3：Railway部署
1. 登录Railway: https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择您的仓库
5. 点击 "Deploy Now"

## 方法2：直接上传文件

### 步骤1：准备文件
1. 解压此文件夹到本地
2. 确保包含以下文件：
   - app.py
   - requirements.txt
   - full_questions.json
   - templates/ (目录)
   - static/ (目录)
   - railway.toml
   - nixpacks.toml

### 步骤2：Railway部署
1. 登录Railway: https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 点击 "Deploy from GitHub repo" 下方的 "Deploy from directory"
5. 拖拽或选择此文件夹
6. 点击 "Deploy Now"

## 环境变量设置
部署完成后，在Railway项目设置中添加：
- PORT = 8080

## 访问地址
部署完成后，您将获得类似地址：
https://your-app-name.railway.app

## 注意事项
1. 确保所有文件都已上传
2. 检查部署日志是否有错误
3. 如果部署失败，检查requirements.txt中的依赖版本
