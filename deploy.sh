#!/bin/bash
# AIHOT Topics · Deploy Script
# 推送到 GitHub Pages

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_DIR"

echo "🚀 Deploying AIHOT Topics..."

# Check for changes
if [[ -z "$(git status --porcelain)" ]]; then
  echo "ℹ️  No changes to commit."
else
  git add -A
  git commit -m "deploy: $(date '+%Y-%m-%d %H:%M') [auto]"
fi

# Push (use proxy if needed for WSL)
if git remote get-url origin &>/dev/null; then
  echo "📤 Pushing to GitHub..."
  # Use SSH (HTTPS may be blocked in some networks)
  git push origin main
  echo "✅ Deployed!"
else
  echo "⚠️  No remote configured. Set up with:"
  echo "   git remote add origin https://github.com/zhangs1r/aihot-topics.git"
fi
