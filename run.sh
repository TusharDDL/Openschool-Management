#!/bin/bash

# Kill any existing processes
pkill -f "uvicorn|next|npm|node" || true
sleep 2

# Start backend
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8002 > backend.log 2>&1 &
cd ..

# Start frontend
npm run dev -- --port 3002 > frontend.log 2>&1 &

# Wait for services to start
sleep 5

# Show running processes
ps aux | grep -E "uvicorn|next|npm"

# Show logs
echo "Backend log:"
cat backend/backend.log
echo "Frontend log:"
cat frontend.log

# Keep script running
tail -f backend/backend.log frontend.log