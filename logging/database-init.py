from pymongo import MongoClient
import config

# Specify the MongoDB server connection URL
connectionURL = "mongodb://localhost:27017"

# Specify the name of the database
databaseName = config.ROOM

# Specify the name of the collection
collectionName = "measurements"

def create_database_and_collection():
    try:
        # Connect to the MongoDB server
        client = MongoClient(connectionURL)

        # Access the "DTLab" database
        db = client[databaseName]

        # Create the collection
        db.create_collection(collectionName)

        print(f'Database "{databaseName}" with collection "{collectionName}" created successfully.')

        # Close the connection to the MongoDB server
        client.close()
    except Exception as error:
        print(f'Error: {error}')

if __name__ == "__main__":
    create_database_and_collection()
