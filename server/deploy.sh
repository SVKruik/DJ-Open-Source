#!/bin/sh
export HOME=/home/svkruik

# Git
cd ..
git config --global --add safe.directory "$HOME/Documents/GitHub/DJ-Open-Source"
git reset --hard
git pull
echo "Git setup complete"

# Hosting - oss.stefankruik.com
cd frontend
npm install
npm run build
echo "Build complete"

if [ -d "dist" ]; then
    cd ../server
    npm install
    npm run build
    rm -rf frontendDist
    mkdir -p frontendDist
    mv ../frontend/dist/* frontendDist/
    echo "Migration complete"

    cd ../frontend
    rm -rf dist
    echo "Cleanup complete"

    echo "Deployment complete. Reloading server."
    sudo systemctl restart dj-open-source.service
else
    echo "Deployment failed. Dist directory missing."
    exit 1
fi
