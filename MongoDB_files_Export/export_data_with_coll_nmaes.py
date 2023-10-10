# export_data.py
import os
import pandas as pd
from pymongo import MongoClient

mongo_uri = "mongodb+srv://anton:rBfxVpwPAZs4kAz@cluster0.mjydb2j.mongodb.net/personal_bot?retryWrites=true&w=majority"
database_name = "personal_bot"
csv_folder_path = "D:/New Project/Python/Autobot Things/MongoDB_files_Export/csv_files"
collection_names = ["chat", "order"]

client = MongoClient(mongo_uri)
db = client[database_name]

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
