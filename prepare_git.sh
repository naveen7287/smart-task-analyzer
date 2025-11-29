#!/bin/bash
# Initialize a git repo with sensible .gitignore and first commit
git init
git checkout -b main
cat > .gitignore <<'EOF'
venv/
__pycache__/
db.sqlite3
*.pyc
*.log
node_modules/
*.zip
EOF
git add .
git commit -m "Initial commit - Smart Task Analyzer enhanced package"
echo "Repository initialized. Run: git remote add origin <your-repo> && git push -u origin main"
