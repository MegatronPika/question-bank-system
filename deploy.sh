#!/bin/bash

# 金融业数字化转型技能大赛题库系统部署脚本

echo "=== 金融业数字化转型技能大赛题库系统部署脚本 ==="

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt

# 检查题库文件
if [ ! -f "full_questions.json" ]; then
    echo "错误: 题库文件 full_questions.json 不存在"
    exit 1
fi

echo "✓ 题库文件检查通过"

# 创建日志目录
mkdir -p logs

# 启动系统
echo "正在启动系统..."
echo "访问地址: http://localhost:8080"
echo "如需公网访问，请配置防火墙开放8080端口"
echo "按 Ctrl+C 停止服务器"

# 使用nohup后台运行
nohup python3 app.py > logs/app.log 2>&1 &

# 保存进程ID
echo $! > app.pid

echo "系统已启动，进程ID: $(cat app.pid)"
echo "日志文件: logs/app.log"
echo ""
echo "停止系统命令: ./stop.sh"
echo "查看日志命令: tail -f logs/app.log" 