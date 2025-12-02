cd ..

# Hosting - djos.stefankruik.com
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
    echo "Cleanup complete. Ready to serve."
else
    echo "Deployment failed. Dist directory missing."
    exit 1
fi
