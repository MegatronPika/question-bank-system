#!/bin/bash

# 停止题库系统

echo "正在停止题库系统..."

if [ -f "app.pid" ]; then
    pid=$(cat app.pid)
    if ps -p $pid > /dev/null; then
        echo "停止进程 $pid..."
        kill $pid
        rm app.pid
        echo "系统已停止"
    else
        echo "进程 $pid 不存在，可能已经停止"
        rm app.pid
    fi
else
    echo "未找到进程ID文件，尝试查找Python进程..."
    pkill -f "python.*app.py"
    echo "已尝试停止所有相关进程"
fi 