#!/bin/bash

# Check if MongoDB is installed
if ! command -v mongosh &> /dev/null
then
    echo "MongoDB not found. Installing MongoDB..."
    
    # Install MongoDB (for Debian-based systems)
    sudo apt install software-properties-common gnupg apt-transport-https ca-certificates -y
    curl -fsSL https://pgp.mongodb.com/server-7.0.asc |  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse
    sudo apt update
    sudo apt install mongodb-org -y
    mongod --version
    
    
    echo "MongoDB installed successfully."
fi

# Start MongoDB service
sudo service mongod start

# MongoDB connection details
MONGODB_HOST="localhost"
MONGODB_PORT="27017"
DATABASE_NAME="housing_scrapper"
COLLECTION_NAME="properties"

# Create MongoDB collection
mongosh $MONGODB_HOST:$MONGODB_PORT/$DATABASE_NAME --eval "db.createCollection('$COLLECTION_NAME')"
echo "MongoDB collection '$COLLECTION_NAME' created in '$DATABASE_NAME' database."