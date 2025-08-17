#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile

def create_deployment_package():
    """创建部署包"""
    print("=== 创建在线部署包 ===")
    print()
    
    # 创建部署目录
    deploy_dir = "deploy_package"
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # 复制必要文件
    files_to_copy = [
        "app.py",
        "requirements.txt",
        "full_questions.json"
    ]
    
    print("正在复制文件...")
    for item in files_to_copy:
        if os.path.isfile(item):
            shutil.copy2(item, deploy_dir)
            print(f"✅ 复制文件: {item}")
    
    # 复制目录
    dirs_to_copy = ["templates", "static"]
    for dir_name in dirs_to_copy:
        if os.path.isdir(dir_name):
            shutil.copytree(dir_name, os.path.join(deploy_dir, dir_name))
            print(f"✅ 复制目录: {dir_name}")
    
    # 创建Procfile (Heroku)
    procfile_content = "web: python app.py"
    with open(os.path.join(deploy_dir, "Procfile"), 'w') as f:
        f.write(procfile_content)
    print("✅ 创建Procfile")
    
    # 创建部署说明
    deploy_readme = """# 题库系统在线部署说明

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
"""
    
    with open(os.path.join(deploy_dir, "DEPLOY_README.md"), 'w', encoding='utf-8') as f:
        f.write(deploy_readme)
    print("✅ 创建部署说明")
    
    # 创建zip包
    zip_filename = "question_bank_deploy.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ 部署包已创建: {zip_filename}")
    print(f"📦 文件大小: {os.path.getsize(zip_filename)} 字节")
    
    return zip_filename

def main():
    zip_file = create_deployment_package()
    if zip_file:
        print()
        print("=== 部署说明 ===")
        print("1. 解压 question_bank_deploy.zip")
        print("2. 选择以下任一平台部署:")
        print("   - Railway: https://railway.app")
        print("   - Render: https://render.com")
        print("   - Heroku: https://heroku.com")
        print("3. 上传解压后的文件")
        print("4. 等待部署完成")
        print("5. 获得公网访问地址")
        print()
        print("🎉 部署包已准备完成！")

if __name__ == "__main__":
    main() 