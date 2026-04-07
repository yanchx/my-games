#!/bin/bash
echo "🚀 开始部署到 GitHub Pages..."
echo ""

# 设置 Git 用户信息
git config user.email "bot@openclaw.local"
git config user.name "OpenClaw Bot"

# 添加远程仓库
git remote set-url origin https://github.com/yanchx/shooter.git

# 重命名分支为 main
git branch -M main 2>/dev/null || true

# 推送到 GitHub
echo "📤 推送到 GitHub..."
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    echo "====================================="
    echo "🎉 下一步：启用 GitHub Pages"
    echo "====================================="
    echo ""
    echo "1️⃣ 访问这个链接:"
    echo "   https://github.com/yanchx/shooter/settings/pages"
    echo ""
    echo "2️⃣ 在 'Build and deployment' 部分:"
    echo "   Source: Deploy from a branch"
    echo "   Branch: main / (root)"
    echo "   点击 Save"
    echo ""
    echo "3️⃣ 等待 2-5 分钟，然后访问:"
    echo "   https://yanchx.github.io/shooter/"
    echo ""
    echo "🎮 你的游戏中心就上线了！"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能需要 GitHub 认证，请手动执行:"
    echo "cd /root/.openclaw/workspace/games_website"
    echo "git remote set-url origin https://github.com/yanchx/shooter.git"
    echo "git push -u origin main --force"
fi
