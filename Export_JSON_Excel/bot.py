import requests
import os
import json
import pandas as pd
from messages import send_message, send_reply_button, send_list, upload_image, send_videos, format_order_summary, send_images_one_by_one, send_email, count
from intents import intent
import re
from requests.auth import HTTPBasicAuth
import json
import datetime
from googletrans import Translator
from dotenv import load_dotenv
import pymongo
from datetime import datetime
import random
import string
from translate import Translator
from utils import *
from google.oauth2 import service_account
import gspread
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

allowed_extensions=["png", "jpg", "jpeg"]

def allowed_file(filename):
  ext=filename.split(".")[-1]
  if ext in allowed_extensions:
      return True
  
# Specify the path to your service account JSON key file
keyfile_path = 'google_cloud.json'

# Authenticate using the service account JSON key file
credentials = service_account.Credentials.from_service_account_file(
    keyfile_path, 
    # scopes=['https://www.googleapis.com/auth/spreadsheets']
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
)

# Authorize with gspread using the credentials
client = gspread.authorize(credentials)

# Open the Google Sheets document by its title
spreadsheet = client.open('Order_data')

# Select the worksheet where you want to export data (if it exists)
worksheet = spreadsheet.worksheet('Sheet1')  # Replace 'Sheet1' with your sheet name


  
load_dotenv()

api_url=os.getenv("API_URL")
access_token=os.getenv("ACCESS_TOKEN")


class Order():
    def __init__(self, db):
        self.db = db.order

    def check_payment_status(self):
        pass
    def generate_order_id(self):
        # Generate a 7-digit order ID
        return ''.join(random.choices(string.digits, k=7))
    
    def create_order(self, number, post):
        order = post
        order["status"] = ""
        order["order_summary"] = ""
        order["created_date"] = datetime.now()
        order["last_modified"] = datetime.now()
        order["phone_number"] = number
        
        # Generate a 7-digit order ID
        order_id = self.generate_order_id()
        order["order_id"] = order_id

        # Insert the order into the database
        self.db.insert_one(order)
       
        self.export_to_json(order, order_id)
        self.export_to_google_sheets(order, order_id)
        # self.send_order_email(order, order_id)
        # self.export_to_excel(order, order_id)
        # self.send_whatsapp_message(order_id)

        return order_id
    
    def export_to_google_sheets(self, order, order_id):
        # Convert ObjectId to string
        order["_id"] = str(order["_id"])

        # Serialize to JSON
        order_json = json.dumps(order, indent=4, default=self.datetime_to_str)
        print("JSON Data to be Appended to Google Sheets:")
        print(order_json)

        # Check if the header row exists (assumes header is in the first row)
        if not worksheet.row_values(1):
            # Create the header row if it doesn't exist
            header_row = [
                "Order ID",
                "Design",
                "Output Type",
                "Function",
                "Created Date",
                "Last Modified",
                "Phone Number",
            ]
            worksheet.append_row(header_row)

        # Parse the JSON data
        order_data = json.loads(order_json)

        # Create a list of values from the JSON data
        order_values = [
            order_data['order_id'],
            order_data['design'],
            order_data['output_type'],
            order_data['function'],
            order_data['created_date'],
            order_data['last_modified'],
            order_data['phone_number']
        ]

        # Append the new order data as a new row
        worksheet.append_row(order_values)

        print("Data successfully appended to Google Sheets.")

    def datetime_to_str(self, dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    def export_to_json(self, order, order_id):
        # Convert ObjectId to string
        order["_id"] = str(order["_id"])

        # Serialize to JSON
        order_json = json.dumps(order, indent=4, default=self.datetime_to_str)
        with open(f'order_{order_id}.json', 'w') as json_file:
            json_file.write(order_json)

    
             
    

        
load_dotenv()

# Access the MongoDB URL from the environment variables
mongodb_url = os.getenv("MONGO_URI")
API_URL=os.getenv("API_URL")

# Create a MongoDB connection using the loaded URL
client = pymongo.MongoClient(mongodb_url)
db = client["personal_bot"]

incomplete_collection = db["incomplete"]

class Chat():
    def __init__(self, db):
        self.db = db.chat
        # self.last_data_received = {}

    def is_waId_Exists(self, number):
        return self.db.find_one({"_id": number})

    def create_chat(self, number):
        new_user = {'_id': number,
                    "state": "lang",
                    # "video_message": "",
                    "lang": "",
                    "last_activity": datetime.now()
                    }
        self.db.insert_one(new_user)

        

    def update_last_activity(self, number):
        current_time = datetime.now()
        self.db.update_one({'_id': number}, {'$set': {'last_activity': current_time}})

    def update_chat(self, number, key, state, value, id="", order=0):
        old_user = {"$set": {"state": state, key: value}}
        if state == "payment":
            old_user["$push"] = {"payment": {"$each": [id]}}

        if order == 1:
            # Empty design details as order is created
            old_user["$set"] = {"state": state, "design": {}}
            old_user["$push"] = {"order": {"$each": [id]}}

        elif state == "plan":
            old_user["$set"]["subscription"] = "enrolled"

        self.db.update_one({'_id': number}, old_user)

    def get_post(self, number, key=""):
        data = self.db.find_one({"_id": number})
        return data["design"]

    def get_payment_check(self, number):
        data = self.db.find_one({'_id': number})
        return data["payment"][-1]

    def get_enroll_status(self, number):
        data = self.db.find_one({'_id': number})
        return data["lang"]

    def get_chat_lang(self, number):
        data = self.db.find_one({'_id': number})
        return data["lang"]


class Bot():
    def __init__(self, db, json, number,  API_URL, ACCESS_TOKEN, upload, pay_user, pay_pass):
        
        self.db=db
        self.chat= Chat(self.db)
        self.order= Order(self.db)
        # self.payment= Payment(self.db)

        self.dict_message= json
        self.number = number
        self.APIUrl = API_URL
        self.token = ACCESS_TOKEN

        self.upload=upload

        self.pay_user=pay_user
        self.pay_pass=pay_pass
        

    def send_message(self, waID, text):
        answer = send_message(waID, text)
        return answer
    

    def send_reply_button(self, waID, text, buttons):
        answer = send_reply_button(waID, text, buttons)
        print(answer)
        return answer

    def send_list(self, waID, text, list):
        answer = send_list(waID, text, list)
        return answer
    


    def next_question(self, waID, state,chat_lang, custom_msg=""):
        question= intent[chat_lang][state]["question"]+custom_msg
        type=   intent[chat_lang][state]["type"]

        if type == "text":
               self.send_message(waID, question )

        elif type == "list":
            list= intent[chat_lang][state]["list"]
            self.send_list(waID, question, list)

        elif type=="button":
            button= intent[chat_lang][state]["button"]
            self.send_reply_button(waID, question, button)

        else:
            pass
    
        
    def restart_chatbot(self, waID):
        chat_lang = "english"  # Default to English if the user doesn't select a language
        if self.dict_message["type"] == "interactive":
            selected_option = self.dict_message['listReply']["title"]
            if selected_option in ["english", "tamil", "hindi", "telugu", "malayalam", "kannada"]:
                chat_lang = selected_option

        self.chat.update_chat(self.number, "lang", "lang", "")
        question = intent[chat_lang]["lang"]["question"]
        self.send_list(waID, question, intent[chat_lang]["lang"]["list"])
        return True

    
    def keyword_state_change(self,text, state, update, new_state):
        subscription_status= self.chat.get_enroll_status(self.number)
        if subscription_status=="subscribed":
            status=keyword_node(text)
            if status!="None":
                new_state=status
                state="design.post_design"
                update=1
                return state, update, new_state
        return False


    def generate_payment_link(self, amount):
        
        #reference_id = reference_id
        data = {
            "amount": amount,
            "currency": "INR",
            "description": "Testing",
            "options": {
                  "checkout": {
                  "name": "ABC Test Corp"
                              }
                }         
        }
        data = json.dumps(data)
        headers = {
            'Content-type': 'application/json'
        }
        res = requests.post(url="https://api.razorpay.com/v1/payment_links/", headers=headers, data=data,
                            auth=HTTPBasicAuth(self.pay_user,self.pay_pass)).json()
        #print(res)
        return res
    
    def check_payment_status(self, id):
        
        url=f"https://api.razorpay.com/v1/payment_links/{id}"
    
        headers = {
            'Content-type': 'application/json'
        }
        res = requests.get(url= url, headers=headers,
                            auth=HTTPBasicAuth(self.pay_user, self.pay_pass)).json()
        #print(res)
        return res
    
    def text_translate(self, lang, text):
        try:
            translator = Translator(to_lang=lang)
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return "Translation error"  # Handle the error as needed
        
    
    
    def processing(self):
        text=self.dict_message['text']
        _type=self.dict_message['type']
        option=""
        item_id=""
        global count
        
        custom_msg=""
        order=0
        chat_lang="english"

        
        if self.dict_message["type"]=="interactive":
                text =self.dict_message['listReply']["title"]
                option= self.dict_message["listReply"]["title"]
        
        elif self.dict_message["type"]=="button":
            pass
        
        # Checking whether waID present in db or not
        record= self.chat.is_waId_Exists(self.number)
        
        
        if record == None:
            print("new")
            self.chat.create_chat(self.number) 
            self.chat.update_last_activity(self.number)  # Update last activity on interaction
            
            contact_number = self.number
            print(contact_number)
            send_videos(contact_number)
                
            update=1
            state="lang"
            new_state=state
            # state="video_message"
            # new_state=state
           
        
        else:
            chat_lang= self.chat.get_chat_lang(self.number)  # chat lang chosen by user in "lang" step
            state=record["state"]
            new_state=state
            update =0

            if text=="Restart":
                if self.restart_chatbot(self.number):
                   return "Chat has been Restarted "
                
            node_change_list= self.keyword_state_change(text,state,update,new_state)
            if node_change_list !=False:
                state=node_change_list[0]
                update=node_change_list[1]
                new_state=node_change_list[2]
                
        
            if state=="lang":
                try:
                    # text=text.lower()
                    if text.lower() not in ["english", "tamil", "hindi", "telugu", "malayalam", "kannada"]:
                        raise Exception
                    update=1
                    # self.chat.update_last_activity(self.number)
                    #old_state=state
                    chat_lang = text.lower()
                    print(chat_lang)   
                    new_state="design"
                    
                
                except Exception as e:
                    # print(e)
                    print("Error occured")
                    warning_msg= self.text_translate(chat_lang, "Please Enter a Valid input")
                    err_msg= f"{warning_msg}\n\n{intent[chat_lang][state]['question']}"
                    self.send_list(self.number,err_msg, intent[chat_lang][state]['list'] )

            
            elif state=="design":
                #print("inside enroll")
                print("count design",count)
                try:
                    chat_lang = chat_lang.lower()
                    if text.lower() not in design_list[chat_lang]:
                      raise Exception  
                    
                    if text in ["Inivitation", "Poster", "Social Media Post", "Advertisement", "Presentation", "அழைப்பு", "சுவரொட்டி", "சமூக ஊடக இடுகை", "விளம்பரம்", "விளக்கக்காட்சி"]:
                        new_state="output_type"
                        count = 0
                        
                    update=1
                    self.chat.update_last_activity(self.number)
                    #chat_lang = text.lower()
                    state=f"design.{state}"
                    #old_state=state
                    #print("inside if")
                    
                
                except Exception :
                    print("count 1",count)
                    count += 1
                    print("count 2",count)
                    if count >= 3:
                        print("You have exceeded the maximum number of attempts.")
                        if self.restart_chatbot(self.number):
                            return "Chat has been Restarted "
                    else:
                        #print(e)
                        print("count 3",count)
                        warning_msg= self.text_translate(chat_lang, "Please Enter a Valid input")
                        err_msg= f"{warning_msg}\n\n{intent[chat_lang][state]['question']}"
                        self.send_list(self.number,err_msg, intent[chat_lang][state]['list'] )

            elif state=="output_type":
                #print("inside enroll")
                try:
                    chat_lang = chat_lang.lower()                   
                    if text not in ["Image", "GIF", "Short Video", "Long Video"]:
                        raise Exception
                        
                        
                    update=1
                    self.chat.update_last_activity(self.number)
                    #chat_lang = text.lower()
                    state=f"design.{state}"
                    new_state="function"
                    count = 0
                    #old_state=state
                    #print("inside if")
                    
                
                except Exception :
                    print("count 4",count)
                    count += 1
                    print("count 5",count)
                    if count >= 3:
                        print("You have exceeded the maximum number of attempts.")
                        if self.restart_chatbot(self.number):
                            return "Chat has been Restarted "
                    else:
                        #print(e)
                        print("count 6",count)
                        warning_msg= self.text_translate(chat_lang, "Please Enter a Valid input")
                        err_msg= f"{warning_msg}\n\n{intent[chat_lang][state]['question']}"
                        self.send_list(self.number,err_msg, intent[chat_lang][state]['list'] )


            elif state=="function":
                #print("inside enroll")
                try:
                    chat_lang = chat_lang.lower()
                    if text.lower() not in function_list[chat_lang]:
                      raise Exception  
                    
                    if text in ["Wedding", "Birthday", "Anniversary", "Religious Activity", "Retirement", "Orbiturary", "Party", "Events"]:
                        update=1
                        self.chat.update_last_activity(self.number)
                        #chat_lang = text.lower()
                        state=f"design.{state}"
                        order=1
                        new_state="end"
                        count = 0  
                        
                                         
                    
                
                except Exception :
                    print("count 7",count)
                    count += 1
                    print("count 8",count)
                    if count >= 3:
                        print("You have exceeded the maximum number of attempts.")
                        if self.restart_chatbot(self.number):
                            return "Chat has been Restarted "
                    else:
                        #print(e)
                        print("count 9",count)
                        warning_msg= self.text_translate(chat_lang, "Please Enter a Valid input")
                        err_msg= f"{warning_msg}\n\n{intent[chat_lang][state]['question']}"
                        self.send_list(self.number,err_msg, intent[chat_lang][state]['list'] )

            

        ##  Updating Coverstion status, details and sending the next question

        if update == 1:
            if new_state == "end":
                if order == 1:
                    # Update last details of post before creation of order
                    self.chat.update_chat(self.number, state, new_state, text)

                    # Get details of the post
                    post = self.chat.get_post(self.number)  

                    # Generate order id and create order
                    order_id = self.order.create_order(self.number,post)
                    print("Order Created")

                    self.chat.update_chat(self.number, state, new_state, text, order_id, order)

                    success_msg = self.text_translate(chat_lang, "Order Created Successfully")
                    self.send_message(self.number, success_msg)

                else:
                    self.chat.update_chat(self.number, state, new_state, text)


            elif new_state=="payment" :
                self.chat.update_chat(self.number,state, new_state, text, item_id)
                self.next_question(self.number, new_state,chat_lang, custom_msg)
            else:
                
                self.chat.update_chat(self.number,state, new_state, text)
                self.next_question(self.number, new_state,chat_lang, custom_msg) 

        return "Message Sent"