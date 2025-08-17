#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile

def create_railway_package():
    """创建Railway专用部署包"""
    print("=== 创建Railway部署包 ===")
    print()
    
    # 创建部署目录
    deploy_dir = "railway_deploy"
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
    
    # 创建Railway配置文件
    railway_toml = """[build]
builder = "nixpacks"

[deploy]
startCommand = "python app.py"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "on_failure"
"""
    
    with open(os.path.join(deploy_dir, "railway.toml"), 'w') as f:
        f.write(railway_toml)
    print("✅ 创建railway.toml")
    
    # 创建nixpacks配置文件
    nixpacks_toml = """[phases.setup]
nixPkgs = ["python39", "python39Packages.pip"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "python app.py"
"""
    
    with open(os.path.join(deploy_dir, "nixpacks.toml"), 'w') as f:
        f.write(nixpacks_toml)
    print("✅ 创建nixpacks.toml")
    
    # 创建部署说明
    deploy_readme = """# Railway部署说明

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
"""
    
    with open(os.path.join(deploy_dir, "RAILWAY_README.md"), 'w', encoding='utf-8') as f:
        f.write(deploy_readme)
    print("✅ 创建部署说明")
    
    # 创建zip包
    zip_filename = "railway_deploy.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Railway部署包已创建: {zip_filename}")
    print(f"📦 文件大小: {os.path.getsize(zip_filename)} 字节")
    
    return zip_filename

def main():
    zip_file = create_railway_package()
    if zip_file:
        print()
        print("=== Railway部署步骤 ===")
        print("1. 解压 railway_deploy.zip")
        print("2. 登录Railway: https://railway.app")
        print("3. 点击 'New Project'")
        print("4. 选择 'Deploy from GitHub repo'")
        print("5. 如果看到 'Deploy from directory' 选项，选择它")
        print("6. 拖拽解压后的文件夹到上传区域")
        print("7. 点击 'Deploy Now'")
        print("8. 等待部署完成")
        print()
        print("💡 提示:")
        print("- 如果找不到上传选项，建议使用GitHub方法")
        print("- 确保所有文件都已包含在部署包中")
        print("- 部署完成后会自动获得HTTPS地址")

if __name__ == "__main__":
    main() 