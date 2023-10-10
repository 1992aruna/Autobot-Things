# export_data.py
import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
database_name = "personal_bot"
csv_folder_path = "D:/New Project/Python/Autobot Things/MongoDB_files_Export/Export_CSV_Files"

client = MongoClient(mongo_uri)
db = client[database_name]

# Get all collection names in the database
collection_names = db.list_collection_names()

def export_csv():
    try:
        # Ensure the directory exists
        os.makedirs(csv_folder_path, exist_ok=True)

        for collection_name in collection_names:
            collection_data = list(db[collection_name].find())
            collection_df = pd.DataFrame(collection_data)
            csv_export_file = os.path.join(csv_folder_path, f"{collection_name}.csv")
            collection_df.to_csv(csv_export_file, index=False)

        print("CSV export completed successfully")
    except Exception as e:
        # Print exception message for debugging
        print(str(e))

if __name__ == '__main__':
    export_csv()
