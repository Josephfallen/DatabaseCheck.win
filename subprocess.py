import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def check_mongodb_service_status():
    try:
        # Use system-level command to check MongoDB service status
        result = os.system("systemctl is-active mongod")
        
        if result == 0:
            print("MongoDB service is running.")
            return True
        else:
            print("MongoDB service is not running.")
            return False
        
    except Exception as e:
        print(f"Error checking MongoDB service status: {e}")
        return False

def check_database_status(host, port, dbname, username, password):
    if not check_mongodb_service_status():
        return
    
    try:
        # Construct the MongoDB connection URI
        if host == "":
            host = "localhost"
        
        uri = f"mongodb://{username}:{password}@{host}:{port}/{dbname}"
        
        # Create a MongoClient object
        client = MongoClient(uri)
        
        # Access the database
        db = client[dbname]
        
        # Check if the connection is successful by fetching a collection list
        collection_names = db.list_collection_names()
        
        print(f"Database is online. Available collections: {collection_names}")
        
        # Close the connection
        client.close()
        
    except ConnectionFailure as e:
        print(f"Database is offline. Error: {e}")

if __name__ == "__main__":
    # Database connection parameters
    host = input("Enter the database host (default is localhost): ") or "localhost"
    port = int(input("Enter the database port (default is 27017 for MongoDB): ") or 27017)
    dbname = input("Enter the database name: ")
    username = input("Enter the database username (leave empty if none): ")
    password = input("Enter the database password (leave empty if none): ")
    
    # Check the database status
    check_database_status(host, port, dbname, username, password)
