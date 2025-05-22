#!/bin/bash

# Create necessary directories
mkdir -p backend/logs

# Install dependencies
pip install -r requirements.txt

# Start the server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 