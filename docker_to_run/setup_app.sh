#!/bin/bash

git clone https://github.com/maeri18/UniResidences.git ~/UniResidences

cd ~/UniResidences 

# installing python dependencies
pip install -r requirements/txt --break-system-packages --ignore-installed

# loading the sample database 
psql --username ${DATABASE_USERNAME} ${DATABASE_NAME} < sample_database/uniResidences.sql

# install frontend dependencies
cd frontend
npm install

./start_app.sh