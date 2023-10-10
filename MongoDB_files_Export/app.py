import pandas as pd
from pymongo import MongoClient

# Replace these with your MongoDB Atlas connection details
mongo_uri = "mongodb+srv://anton:rBfxVpwPAZs4kAz@cluster0.mjydb2j.mongodb.net/personal_bot?retryWrites=true&w=majority"
database_name = "personal_bot"

# List of collection names to export
collection_names = ["chat", "order"]

# Initialize MongoDB client
client = MongoClient(mongo_uri)
db = client[database_name]

# Export data from each collection and save to separate CSV files
for collection_name in collection_names:
    collection_data = list(db[collection_name].find())
    collection_df = pd.DataFrame(collection_data)

    # Define the CSV export file path for each collection
    csv_export_file = f"{collection_name}.csv"
    
    # Export the data to a CSV file
    collection_df.to_csv(csv_export_file, index=False)
    
    print(f"Data from {collection_name} exported to {csv_export_file}")

# Close the MongoDB client connection
client.close()
