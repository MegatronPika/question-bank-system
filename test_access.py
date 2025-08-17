#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_access():
    """测试各种访问方式"""
    print("=== 题库系统访问测试 ===")
    print()
    
    # 测试地址列表
    test_urls = [
        ("本地访问", "http://localhost:8080"),
        ("局域网访问", "http://192.168.0.240:8080"),
        ("公网访问", "http://216.181.107.152:8080")
    ]
    
    for name, url in test_urls:
        print(f"测试 {name}: {url}")
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name} - 成功")
                if "金融业数字化转型技能大赛" in response.text:
                    print(f"   📋 页面内容正确")
                else:
                    print(f"   ⚠️  页面内容可能不正确")
            else:
                print(f"   ❌ {name} - 状态码: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {name} - 连接失败")
        except requests.exceptions.Timeout:
            print(f"   ⏰ {name} - 连接超时")
        except Exception as e:
            print(f"   ❌ {name} - 错误: {e}")
        print()

def main():
    test_access()
    
    print("📱 手机访问测试:")
    print("1. 确保手机和电脑在同一个WiFi网络")
    print("2. 在手机浏览器中输入: http://192.168.0.240:8080")
    print("3. 如果手机能访问，说明局域网配置正常")
    print()
    
    print("🌍 公网访问配置:")
    print("要启用公网访问，您需要:")
    print("1. 登录路由器管理界面 (通常是 http://192.168.0.1)")
    print("2. 找到'端口转发'或'虚拟服务器'设置")
    print("3. 添加以下规则:")
    print("   - 服务名称: 题库系统")
    print("   - 外部端口: 8080")
    print("   - 内部IP: 192.168.0.240")
    print("   - 内部端口: 8080")
    print("   - 协议: TCP")
    print("4. 保存设置")
    print()
    
    print("🎯 当前推荐访问方式:")
    print("✅ 电脑访问: http://localhost:8080")
    print("✅ 手机访问: http://192.168.0.240:8080")
    print("⏳ 公网访问: 需要配置端口转发")

if __name__ == "__main__":
    main() 