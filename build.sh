#!/usr/bin/env bash
set -o errexit

echo "🔍 Checking for Node.js..."
if ! command -v node &>/dev/null; then
  echo "📦 Installing Node.js 20 (LTS) via nvm..."
  curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  # shellcheck source=/dev/null
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
  nvm install 20
  nvm use 20
fi

echo "✅ Node $(node -v)  npm $(npm -v)"

echo "📦 Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "🐍 Installing Python backend dependencies..."
pip install -r backend/requirements.txt

echo "✅ Build complete!"
