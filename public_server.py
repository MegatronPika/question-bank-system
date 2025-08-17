#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import requests
import json
import time
import threading
from flask import Flask, request, jsonify
import subprocess
import os

def get_public_ip():
    """获取公网IP地址"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        try:
            response = requests.get('https://ifconfig.me/ip', timeout=5)
            return response.text.strip()
        except:
            return None

def get_local_ip():
    """获取本地IP地址"""
    try:
        # 创建一个UDP套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个外部地址（不需要真实连接）
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def check_port_open(host, port):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("=== 金融业数字化转型技能大赛题库系统 - 公网访问配置 ===")
    print()
    
    # 获取IP地址
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    print(f"🌐 本地IP地址: {local_ip}")
    if public_ip:
        print(f"🌍 公网IP地址: {public_ip}")
    else:
        print("❌ 无法获取公网IP地址")
    
    print()
    print("📱 访问地址:")
    print(f"   本地访问: http://localhost:8080")
    print(f"   局域网访问: http://{local_ip}:8080")
    
    if public_ip:
        print(f"   公网访问: http://{public_ip}:8080")
        print()
        print("⚠️  注意事项:")
        print("   1. 确保您的路由器已配置端口转发（8080端口）")
        print("   2. 确保防火墙已开放8080端口")
        print("   3. 如果无法访问，请检查网络配置")
    else:
        print()
        print("❌ 无法获取公网IP，请检查网络连接")
    
    print()
    print("🔧 配置建议:")
    print("   1. 登录路由器管理界面")
    print("   2. 找到'端口转发'或'虚拟服务器'设置")
    print("   3. 添加规则：外部端口8080 -> 内部IP {local_ip}:8080")
    print("   4. 保存设置并重启路由器")
    
    print()
    print("📋 路由器配置示例:")
    print("   服务名称: 题库系统")
    print("   外部端口: 8080")
    print("   内部IP: {local_ip}")
    print("   内部端口: 8080")
    print("   协议: TCP")
    
    print()
    print("🚀 系统状态:")
    if check_port_open("localhost", 8080):
        print("   ✅ 本地服务运行正常")
    else:
        print("   ❌ 本地服务未运行，请先启动系统")
    
    if public_ip and check_port_open(public_ip, 8080):
        print("   ✅ 公网端口开放")
    else:
        print("   ❌ 公网端口未开放，需要配置端口转发")
    
    print()
    print("💡 快速测试:")
    print("   1. 在手机浏览器中访问: http://{local_ip}:8080")
    print("   2. 如果手机能访问，说明局域网配置正常")
    print("   3. 配置端口转发后，即可通过公网IP访问")
    
    print()
    print("📞 如果遇到问题:")
    print("   1. 检查防火墙设置")
    print("   2. 确认路由器支持端口转发")
    print("   3. 尝试使用其他端口（如80、443）")
    print("   4. 考虑使用云服务器部署")

if __name__ == "__main__":
    main() 