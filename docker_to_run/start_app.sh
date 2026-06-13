#!/bin/bash
cd ~/UniResidences 

# Run the app backend
python3 app.py &

# run frontend
cd frontend
npm run dev

