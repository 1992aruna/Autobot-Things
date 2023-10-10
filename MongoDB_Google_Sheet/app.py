from flask import Flask, request, jsonify
from bot import Bot
import os
import traceback
from dotenv import load_dotenv
import gspread
from google.oauth2 import service_account

load_dotenv()

API_URL = os.getenv("API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


# Specify the path to your service account JSON key file
CREDENTIALS_FILE = 'google_cloud.json'

# Authenticate using the service account JSON key file
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE, 
    # scopes=['https://www.googleapis.com/auth/spreadsheets']
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
)

# Authorize with gspread using the credentials
client = gspread.authorize(credentials)

# Open the Google Sheets document by its title
SPREADSHEET_NAME = 'Personal_Bot'  # Replace with the title of your Google Sheets document
spreadsheet = client.open(SPREADSHEET_NAME)

# Select the worksheet where you want to export data (if it exists)
chat_worksheet = spreadsheet.worksheet('Sheet1')  # Replace 'Sheet1' with your sheet name

order_worksheet = spreadsheet.worksheet('Sheet2')

UPLOAD_FOLDER = 'static/data/images'

app = Flask(__name__)


app.secret_key = b'_m9y2L*79xQ8z\n\xec]/'

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.errorhandler(500)
def internal_server_error(e):
    # Log the error details to a file or other logging system
    traceback.print_exc()

    # You can customize the error response sent to the client
    error_response = "Internal Server Error"

    # You can also include additional error details if needed
    error_response += "\n" + str(e)

    # Return the error response and 500 status code
    return error_response, 500

@app.route('/', methods=['GET'])
def home():
    return "Bot Live 3.0"

@app.route('/webhook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        data = request.json
        if "created" in data:
            number = data['waId']
            bot = Bot(chat_worksheet, order_worksheet, data, number, API_URL, ACCESS_TOKEN, app.config["UPLOAD_FOLDER"])
            return bot.processing()
    return "Processing..."

if __name__ == '__main__':
    app.run(debug=True)
