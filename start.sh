#!/bin/bash

# Railway startup script
echo "🚀 Starting Court Case Application on Railway"

# Install Chrome dependencies if needed
if [ "$RAILWAY_ENVIRONMENT" = "production" ]; then
    echo "📦 Setting up production environment..."
fi

# Start the application
echo "🌐 Starting Flask server..."
python app.py
