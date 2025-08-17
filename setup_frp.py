#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import urllib.request
import zipfile
import subprocess

def download_frp():
    """下载frp工具"""
    print("=== 配置frp内网穿透 ===")
    print()
    
    # 检测系统类型
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "darwin":  # macOS
        if "arm" in arch or "aarch64" in arch:
            frp_url = "https://github.com/fatedier/frp/releases/download/v0.51.3/frp_0.51.3_darwin_arm64.tar.gz"
            filename = "frp_0.51.3_darwin_arm64.tar.gz"
        else:
            frp_url = "https://github.com/fatedier/frp/releases/download/v0.51.3/frp_0.51.3_darwin_amd64.tar.gz"
            filename = "frp_0.51.3_darwin_amd64.tar.gz"
    elif system == "linux":
        if "arm" in arch or "aarch64" in arch:
            frp_url = "https://github.com/fatedier/frp/releases/download/v0.51.3/frp_0.51.3_linux_arm64.tar.gz"
            filename = "frp_0.51.3_linux_arm64.tar.gz"
        else:
            frp_url = "https://github.com/fatedier/frp/releases/download/v0.51.3/frp_0.51.3_linux_amd64.tar.gz"
            filename = "frp_0.51.3_linux_amd64.tar.gz"
    else:
        print("❌ 不支持的操作系统")
        return False
    
    print(f"检测到系统: {system} {arch}")
    print(f"下载地址: {frp_url}")
    print()
    
    # 下载frp
    print("正在下载frp...")
    try:
        urllib.request.urlretrieve(frp_url, filename)
        print("✅ 下载完成")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False
    
    # 解压
    print("正在解压...")
    try:
        import tarfile
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall('.')
        print("✅ 解压完成")
    except Exception as e:
        print(f"❌ 解压失败: {e}")
        return False
    
    # 查找frpc可执行文件
    frpc_path = None
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'frpc':
                frpc_path = os.path.join(root, file)
                break
        if frpc_path:
            break
    
    if not frpc_path:
        print("❌ 未找到frpc可执行文件")
        return False
    
    print(f"✅ 找到frpc: {frpc_path}")
    
    # 创建配置文件
    config_content = """[common]
server_addr = frp.freefrp.net
server_port = 7000
token = freefrp.net

[web]
type = tcp
local_ip = 127.0.0.1
local_port = 8080
remote_port = 0
"""
    
    config_file = "frpc.ini"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ 配置文件已创建: {config_file}")
    
    # 设置执行权限
    os.chmod(frpc_path, 0o755)
    
    print()
    print("🚀 启动frp内网穿透:")
    print(f"执行命令: {frpc_path} -c {config_file}")
    print()
    print("📱 启动后，您将获得一个公网地址")
    print("🌐 任何人都可以通过该地址访问您的题库系统")
    
    return True

def create_start_script():
    """创建启动脚本"""
    script_content = """#!/bin/bash
# frp内网穿透启动脚本

echo "启动frp内网穿透..."

# 查找frpc
FRPC_PATH=""
for root in . frp_*; do
    if [ -f "$root/frpc" ]; then
        FRPC_PATH="$root/frpc"
        break
    fi
done

if [ -z "$FRPC_PATH" ]; then
    echo "❌ 未找到frpc，请先运行: python setup_frp.py"
    exit 1
fi

echo "使用frpc: $FRPC_PATH"

# 启动frp
$FRPC_PATH -c frpc.ini
"""
    
    with open("start_frp.sh", 'w') as f:
        f.write(script_content)
    
    os.chmod("start_frp.sh", 0o755)
    print("✅ 启动脚本已创建: start_frp.sh")

def main():
    if download_frp():
        create_start_script()
        
        print()
        print("=== 使用说明 ===")
        print("1. 确保题库系统正在运行: python app.py")
        print("2. 启动frp内网穿透: ./start_frp.sh")
        print("3. 等待连接成功，获得公网地址")
        print("4. 使用公网地址访问题库系统")
        print()
        print("💡 提示:")
        print("- frp会自动分配一个可用的端口")
        print("- 公网地址格式类似: http://frp.freefrp.net:xxxxx")
        print("- 如果连接失败，请检查网络连接")
    else:
        print("❌ 配置失败")

if __name__ == "__main__":
    main() 