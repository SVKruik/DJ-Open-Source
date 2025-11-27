cd ..

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
else
    echo "Deployment failed. Dist directory missing."
    exit 1
fi
