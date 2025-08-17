#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import requests
import subprocess
import time

def check_port_forwarding():
    """检查端口转发状态"""
    print("=== 端口转发诊断工具 ===")
    print()
    
    # 检查本地服务
    print("1. 检查本地服务状态:")
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        if response.status_code == 200:
            print("   ✅ 本地服务运行正常")
        else:
            print(f"   ❌ 本地服务异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 本地服务无法访问: {e}")
    
    # 检查局域网访问
    print("\n2. 检查局域网访问:")
    try:
        response = requests.get("http://192.168.0.240:8080", timeout=5)
        if response.status_code == 200:
            print("   ✅ 局域网访问正常")
        else:
            print(f"   ❌ 局域网访问异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 局域网访问失败: {e}")
    
    # 检查公网端口
    print("\n3. 检查公网端口状态:")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex(('216.181.107.152', 8080))
        sock.close()
        
        if result == 0:
            print("   ✅ 公网端口8080开放")
        else:
            print("   ❌ 公网端口8080未开放")
            print("   💡 可能的原因:")
            print("      - 端口转发未生效")
            print("      - ISP阻止了端口转发")
            print("      - 路由器配置错误")
    except Exception as e:
        print(f"   ❌ 检查公网端口时出错: {e}")
    
    # 检查其他常见端口
    print("\n4. 检查其他端口:")
    common_ports = [80, 443, 8080, 3000, 5000]
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('216.181.107.152', port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ 端口{port}开放")
            else:
                print(f"   ❌ 端口{port}关闭")
        except:
            print(f"   ❌ 端口{port}检查失败")
    
    print("\n5. 路由器配置建议:")
    print("   请检查以下配置:")
    print("   - 服务名称: 题库系统")
    print("   - 外部端口: 8080")
    print("   - 内部IP: 192.168.0.240")
    print("   - 内部端口: 8080")
    print("   - 协议: TCP")
    print("   - 状态: 启用")
    
    print("\n6. 常见解决方案:")
    print("   a) 重启路由器")
    print("   b) 尝试其他端口（如80、443）")
    print("   c) 检查ISP是否阻止端口转发")
    print("   d) 联系ISP客服确认端口转发服务")
    
    print("\n7. 替代方案:")
    print("   - 使用云服务器部署")
    print("   - 使用内网穿透工具（如frp）")
    print("   - 使用VPN方案")

def test_alternative_ports():
    """测试其他端口"""
    print("\n=== 测试其他端口 ===")
    
    alternative_ports = [80, 443, 3000, 5000, 9000]
    
    for port in alternative_ports:
        print(f"\n测试端口 {port}:")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(('216.181.107.152', port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ 端口{port}可用")
                print(f"   🌐 可以尝试: http://216.181.107.152:{port}")
            else:
                print(f"   ❌ 端口{port}不可用")
        except Exception as e:
            print(f"   ❌ 端口{port}检查失败: {e}")

def main():
    check_port_forwarding()
    test_alternative_ports()
    
    print("\n=== 总结 ===")
    print("如果端口转发仍然不工作，建议:")
    print("1. 联系您的ISP确认是否支持端口转发")
    print("2. 考虑使用云服务器部署")
    print("3. 使用内网穿透工具")
    print("4. 暂时使用局域网访问: http://192.168.0.240:8080")

if __name__ == "__main__":
    main() 