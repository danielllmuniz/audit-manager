#!/bin/bash

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ .env file created from .env.example"
else
    echo "✓ .env file already exists"
fi

docker-compose down -v

docker-compose up --build -d

echo ""
echo "✓ Setup complete! Services are starting..."
