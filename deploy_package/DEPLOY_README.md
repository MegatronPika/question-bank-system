# 题库系统在线部署说明

## 部署平台推荐

### 1. Railway (推荐)
- 免费额度：每月500小时
- 部署简单，支持GitHub集成
- 自动HTTPS

### 2. Render
- 免费额度：每月750小时
- 部署简单，支持多种语言

### 3. Heroku
- 免费额度：每月550小时
- 功能强大，生态丰富

## 部署步骤

### Railway部署
1. 注册Railway账号: https://railway.app
2. 连接GitHub仓库
3. 上传此文件夹内容
4. 设置环境变量: PORT=8080
5. 部署完成

### Render部署
1. 注册Render账号: https://render.com
2. 创建Web Service
3. 连接GitHub仓库
4. 设置构建命令: pip install -r requirements.txt
5. 设置启动命令: python app.py
6. 部署完成

## 访问地址
部署完成后，您将获得一个公网地址，类似：
- https://your-app.railway.app
- https://your-app.onrender.com
- https://your-app.herokuapp.com

任何人都可以通过该地址访问您的题库系统！
