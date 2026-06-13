#!/bin/bash
cd
cp /etc/skel/.bashrc .

cat << 'EOF' >> ~/.bashrc
 "\. "$HOME/.nvm/nvm.sh"
 export SECRET_KEY=mySecretKey
export DATABASE_USERNAME=$POSTGRES_USER
export DATABASE_PASSWORD=$POSTGRES_PASSWORD
export DATABASE_NAME=$POSTGRES_DB

[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion"

EOF

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