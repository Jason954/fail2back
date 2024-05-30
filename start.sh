#!/bin/sh

# Start uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start scheduler.py
python scheduler.py &

# Wait for all background processes to finish
wait
