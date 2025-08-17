# 🎯 金融业数字化转型技能大赛题库系统

## 📋 项目概述

这是一个完整的在线题库练习系统，基于Flask开发，支持随机做题、模拟考试和错题记录功能。系统包含1468道金融业数字化转型技能大赛题目，涵盖单选题、多选题和判断题三种题型。

## ✨ 核心功能

### 🎲 随机做题功能
- **全量题库模式**: 从所有1468道题目中随机出题
- **未做题库模式**: 从未做过的题目中随机出题  
- **错题库模式**: 从做错的题目中随机出题
- **实时反馈**: 立即显示答案正确性和详细解析
- **智能提示**: 当所有题目都做过时，会提示选择其他模式

### 📝 模拟考试功能
- **考试规模**: 150道题目（50单选+50多选+50判断），总分1000分
- **时间限制**: 60分钟倒计时，时间到自动交卷
- **答题卡**: 实时显示答题进度和已答题目
- **成绩统计**: 考试完成后显示分数和错题回顾
- **错题记录**: 考试错题自动加入错题库

### 📊 错题记录功能
- **分类展示**: 按题型（单选、多选、判断）分类显示
- **多种排序**: 支持按时间、错题次数、题目编号排序
- **详细记录**: 记录做错时间、次数、答案和解析
- **错题回顾**: 点击查看错题详情和解析

## 🚀 快速开始

### 方法一：直接运行
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动系统
python app.py

# 3. 访问系统
# 打开浏览器访问: http://localhost:8080
```

### 方法二：使用部署脚本
```bash
# 1. 部署系统
./deploy.sh

# 2. 停止系统
./stop.sh

# 3. 查看日志
tail -f logs/app.log
```

### 方法三：Docker部署
```bash
# 1. 构建并启动容器
docker-compose up -d

# 2. 查看容器状态
docker-compose ps

# 3. 停止容器
docker-compose down
```

## 📁 项目结构

```
gonghui/
├── app.py                 # Flask主应用
├── run.py                 # 启动脚本
├── requirements.txt       # Python依赖
├── deploy.sh             # 部署脚本
├── stop.sh               # 停止脚本
├── Dockerfile            # Docker配置
├── docker-compose.yml    # Docker Compose配置
├── full_questions.json   # 题库数据（1468题）
├── user_data.json        # 用户数据（自动生成）
├── templates/            # HTML模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 主页
│   ├── random_practice.html  # 随机做题页面
│   ├── exam.html         # 考试页面
│   └── wrong_questions.html  # 错题记录页面
├── static/               # 静态文件
│   ├── css/              # 样式文件
│   └── js/               # JavaScript文件
└── logs/                 # 日志目录（自动生成）
```

## 🌐 公网部署

### 1. 服务器要求
- Linux服务器（Ubuntu/CentOS）
- Python 3.7+
- 至少1GB内存
- 开放8080端口

### 2. 部署步骤
```bash
# 1. 上传项目文件到服务器
scp -r gonghui/ user@your-server:/home/user/

# 2. 登录服务器
ssh user@your-server

# 3. 进入项目目录
cd /home/user/gonghui

# 4. 运行部署脚本
./deploy.sh

# 5. 配置防火墙（如果需要）
sudo ufw allow 8080
```

### 3. 域名配置（可选）
```nginx
# Nginx配置示例
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 题库统计

- **总题数**: 1468题
- **总分**: 9915分
- **题目类型分布**:
  - 单选题: 520题
  - 多选题: 515题
  - 判断题: 433题
- **分值分布**: 每道题5-10分不等

## 🔧 技术栈

- **后端**: Flask (Python)
- **前端**: Bootstrap 5 + jQuery
- **数据格式**: JSON
- **样式**: 响应式设计，支持手机和电脑访问
- **部署**: Docker + Docker Compose

## 📱 移动端支持

系统采用响应式设计，完美支持：
- 📱 手机浏览器
- 📱 平板设备
- 💻 桌面浏览器

## 🔒 数据安全

- 用户数据存储在本地JSON文件中
- 建议定期备份 `user_data.json` 文件
- 生产环境建议使用数据库存储

## 🛠️ 维护命令

```bash
# 查看系统状态
ps aux | grep python

# 查看日志
tail -f logs/app.log

# 重启系统
./stop.sh && ./deploy.sh

# 备份数据
cp user_data.json user_data_backup_$(date +%Y%m%d).json
```

## 📞 技术支持

如遇到问题，请检查：
1. Python版本是否为3.7+
2. 依赖是否正确安装
3. 端口8080是否被占用
4. 题库文件是否存在

## 🎉 系统特色

- ✅ 完整的题库管理系统
- ✅ 智能的做题模式选择
- ✅ 真实的考试环境模拟
- ✅ 详细的错题记录分析
- ✅ 美观的响应式界面
- ✅ 简单的部署和维护
- ✅ 支持Docker容器化
- ✅ 完善的日志记录

---

**🎯 开始您的学习之旅吧！访问 http://localhost:8080 开始使用系统。** 