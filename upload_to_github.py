#!/usr/bin/env python3
import os
import base64
import requests

# 配置
GITHUB_USER = "yanchx"
REPO_NAME = "my-games"
BRANCH = "main"

# 读取文件
files_to_upload = [
    ("index.html", "游戏中心首页 - 包含虾虾侦探和太空射击"),
    ("shooter.html", "太空射击游戏")
]

print("🚀 开始上传到 GitHub...")
print(f"仓库：https://github.com/{GITHUB_USER}/{REPO_NAME}")
print()

# 注意：这里需要 GitHub Token
# 如果你已经配置了 SSH 或 Git 凭证，可以直接用 git push
# 否则需要创建一个 Personal Access Token

token = os.environ.get("GITHUB_TOKEN", "")

if not token:
    print("❌ 未找到 GITHUB_TOKEN")
    print()
    print("请按以下步骤创建 Token:")
    print("1. 访问：https://github.com/settings/tokens/new")
    print("2. Note: 填写 'OpenClaw Upload'")
    print("3. Scopes: 勾选 'repo'")
    print("4. 点击 'Generate token'")
    print("5. 复制生成的 token")
    print()
    print("然后执行:")
    print(f"export GITHUB_TOKEN='你的 token'")
    print(f"python3 {__file__}")
    exit(1)

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

for filename, message in files_to_upload:
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在：{filename}")
        continue
    
    # 读取文件内容并编码
    with open(filepath, 'rb') as f:
        content = f.read()
        content_base64 = base64.b64encode(content).decode('utf-8')
    
    # GitHub API 上传文件
    api_url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{filename}"
    
    data = {
        "message": f"🎮 Upload {filename}: {message}",
        "content": content_base64,
        "branch": BRANCH
    }
    
    response = requests.put(api_url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        print(f"✅ 上传成功：{filename}")
    elif response.status_code == 422:
        # 文件已存在，需要更新
        print(f"⚠️  文件已存在，尝试更新：{filename}")
        
        # 获取当前文件的 SHA
        get_response = requests.get(api_url, headers=headers)
        if get_response.status_code == 200:
            sha = get_response.json()['sha']
            data['sha'] = sha
            
            update_response = requests.put(api_url, headers=headers, json=data)
            if update_response.status_code == 200:
                print(f"✅ 更新成功：{filename}")
            else:
                print(f"❌ 更新失败：{filename} - {update_response.text}")
        else:
            print(f"❌ 无法获取文件信息：{filename}")
    else:
        print(f"❌ 上传失败：{filename}")
        print(f"   状态码：{response.status_code}")
        print(f"   错误：{response.text}")

print()
print("=====================================")
print("📋 下一步：启用 GitHub Pages")
print("=====================================")
print(f"1. 访问：https://github.com/{GITHUB_USER}/{REPO_NAME}/settings/pages")
print("2. Source: Deploy from a branch")
print("3. Branch: main / (root)")
print("4. 点击 Save")
print()
print(f"🌐 完成后访问：https://{GITHUB_USER}.github.io/{REPO_NAME}/")
