#!/bin/bash

git clone https://github.com/maeri18/UniResidences.git ~/

cd ~/UniResidences 

# loading the sample database 
psql --username ${DATABASE_USERNAME} ${DATABASE_NAME} < sample_database/uniResidences.sql

# Run the app backend
python3 app.py &

# install frontend dependencies
cd frontend
npm install

# run frontend
npm run dev

