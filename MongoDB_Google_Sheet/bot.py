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
# logging.basicConfig(level=logging.DEBUG)

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
spreadsheet = client.open('Personal_Bot')

# Select the worksheet where you want to export data (if it exists)
chat_worksheet = spreadsheet.worksheet('Sheet1')  # Replace 'Sheet1' with your sheet name

order_worksheet = spreadsheet.worksheet('Sheet2')


  
load_dotenv()

api_url=os.getenv("API_URL")
access_token=os.getenv("ACCESS_TOKEN")


class Order():
    def __init__(self, order_worksheet):
        self.worksheet = order_worksheet

    def generate_order_id(self):
        return ''.join(random.choices(string.digits, k=7))

    def create_order(self, number, post):
        order = post
        order["status"] = ""
        order["created_date"] = datetime.now()
        order["last_modified"] = datetime.now()
        order["phone_number"] = number

        # Generate a 7-digit order ID
        order_id = self.generate_order_id()
        order["order_id"] = order_id

        # Append data to the order data worksheet
        data_to_insert = [
            order_id,
            number,
            order["status"],
            str(order["created_date"]),
            str(order["last_modified"]),
            # Add other fields here
        ]
        self.worksheet.append_row(data_to_insert)
       
        
        return order_id
    
    
    def datetime_to_str(self, dt):
        return dt.strftime('%Y-%m-%d %H:%M:%S')

class Chat():
    def __init__(self, chat_worksheet):
        self.worksheet = chat_worksheet

    def is_waId_Exists(self, number):
        try:
            # Get all values in the worksheet
            values = self.worksheet.get_all_values()

            # Check if the "number" exists in the first column of the worksheet
            for row in values:
                if row and row[0] == number:
                    # Return the record (a dictionary) if the WhatsApp ID is found
                    return {
                        "_id": row[0],
                        "state": row[1],
                        "lang": row[2],
                        "last_activity": row[3],
                    }

            # If the number is not found in the worksheet, return None
            return None

        except Exception as e:
            # Handle any exceptions (e.g., worksheet not found, API errors)
            print(f"Error in is_waId_Exists: {e}")
            return None

    def create_chat(self, number):
        try:
            print("Creating chat...")
            # Check if a chat with the same number already exists
            existing_chat = self.get_chat_by_number(number)
            
            if existing_chat:
                print("Chat already exists. Updating last activity...")
                # Update the last activity of the existing chat
                self.update_last_activity(number)
            else:
                # Add header row if the worksheet is empty
                if not self.worksheet.get_all_values():
                    print("Adding header row...")
                    header_row = ["_id", "state", "language", "last Activity"]
                    self.worksheet.append_row(header_row)

                new_user = {'_id': number,
                            "state": "lang",
                            "lang": "",
                            "last_activity": datetime.now()
                            }

                # Append data row below the header row
                data_to_insert = [
                    new_user['_id'],
                    new_user['state'],
                    new_user['lang'],
                    str(new_user['last_activity']),
                ]
                self.worksheet.append_row(data_to_insert)
                print("New chat created successfully.")

        except Exception as e:
            # Handle any exceptions (e.g., worksheet not found, API errors)
            print(f"Error in create_chat: {e}")

    def get_chat_by_number(self, number):
        try:
            # Get all values in the worksheet
            values = self.worksheet.get_all_values()

            # Find the row with the provided WhatsApp ID
            for row in values:
                if row and row[0] == number:
                    # Return the chat information as a dictionary or relevant data structure
                    chat_info = {
                        '_id': row[0],
                        'state': row[1],
                        'lang': row[2],
                        'last_activity': row[3],
                    }
                    return chat_info

            # If chat with the given number is not found, return None
            return None

        except Exception as e:
            # Handle any exceptions (e.g., worksheet not found, API errors)
            print(f"Error in get_chat_by_number: {e}")
            return None


    def update_last_activity(self, number):
        try:
            # Get all values in the worksheet
            values = self.worksheet.get_all_values()

            # Find the row with the provided WhatsApp ID
            for index, row in enumerate(values):
                if row and row[0] == number:
                    # Update the last activity in the corresponding row
                    values[index][-1] = str(datetime.now())
                    self.worksheet.update(f"A{index+2}:A{index+2}", [[values[index][-1]]])
                    break  # Exit the loop once the WhatsApp ID is found and updated

        except Exception as e:
            # Handle any exceptions (e.g., worksheet not found, API errors)
            print(f"Error in update_last_activity: {e}")

    def update_chat(self, number, key, state, value, id="", order=0):
        try:
            values = self.worksheet.get_all_values()
            for index, row in enumerate(values):
                if row and row[0] == number:
                    row_index = index + 2
                    state_index = values[0].index('state')  # Find the index of 'state' in the first row (header)
                    print("Before updating state in update_chat:", state)
                    print("Row before update:", row)  # Print 'row' before the update
                    print("State index:", state_index)
                    print("Type Row",type(row))
                    row = list(row)
                    row[state_index] = state 
                    if state == "payment":
                        row[-1] = id  
                        # row[state_index] = 'new_state'  # Update 'state' to 'new_state'
                        # print("State index1:", state_index)

                    elif order == 1:
                        row[-1] = id  
                        # Update 'state' if necessary
                    elif state == "plan":
                        row[-1] = "enrolled"  
                        # Update 'state' if necessary
                    else:
                        pass
                    print("After updating state in update_chat:", state)
                    print("Row after update:", row)  # Print 'row' after the update
                    self.worksheet.update(f"A{row_index}:{chr(ord('A') + len(row) - 1)}{row_index}", [row])
                    break  
        except Exception as e:
            print(f"Error in update_chat: {e}")

    def get_chat_lang(self, number):
        try:
            # Get all values in the worksheet
            values = self.worksheet.get_all_values()

            # Find the row with the provided WhatsApp ID
            for row in values:
                if row and row[0] == number:
                    # Assuming the language information is stored in a specific column, e.g., "B"
                    lang_index = 1  # Replace with the actual column index
                    return row[lang_index] if len(row) > lang_index else ""

            return ""  # Return an empty string if the WhatsApp ID is not found

        except Exception as e:
            # Handle any exceptions (e.g., worksheet not found, API errors)
            print(f"Error in get_chat_lang: {e}")
            return ""  # Return an empty string in case of an error
        
    def get_post(self, number, key="design"):
        try:
            # Get all values in the worksheet
            values = self.worksheet.get_all_values()

            # Find the row with the provided WhatsApp ID
            for index, row in enumerate(values):
                if row and row[0] == number:
                    # Assuming the key corresponds to a specific column, e.g., "D"
                    key_index = 3  # Replace with the actual column index for the key
                    return row[key_index] if len(row) > key_index else ""

            return ""  # Return an empty string if the WhatsApp ID is not found

        except Exception as e:
            # Handle any exceptions (e.g., worksheet not found, API errors)
            print(f"Error in get_post: {e}")
            return ""  # Return an empty string in case of an error

class Bot():
    def __init__(self, chat_worksheet, order_worksheet, json, number, API_URL, ACCESS_TOKEN, upload):
        self.chat = Chat(chat_worksheet)
        self.order = Order(order_worksheet)

        self.dict_message = json
        self.number = number
        self.APIUrl = API_URL
        self.token = ACCESS_TOKEN

        self.upload = upload

        

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

    
    
    def text_translate(self, lang, text):
        try:
            translator = Translator(to_lang=lang)
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return "Translation error"  # Handle the error as needed
        
    
    
    def processing(self):
        text = self.dict_message['text']
        _type = self.dict_message['type']
        option = ""
        item_id = ""
        global count
        custom_msg = ""
        order = 0
        chat_lang = "english"

        if self.dict_message["type"] == "interactive":
            text = self.dict_message['listReply']["title"]
            option = self.dict_message["listReply"]["title"]

        elif self.dict_message["type"] == "button":
            pass

        # Checking whether waID present in db or not
        record = self.chat.is_waId_Exists(self.number)

        if record is None:
            try:
                print("Creating new chat...")
                # Create a new chat record and update last activity
                self.chat.create_chat(self.number)
                self.chat.update_last_activity(self.number)
                contact_number = self.number
                print(contact_number)
                update = 1
                state = "lang"
                new_state = state
                print("New chat created successfully.")
            except Exception as e:
                print(f"Error creating new chat: {e}")
                return "Error creating new chat."

        else:
            try:
                chat_lang = self.chat.get_chat_lang(self.number)
                state = record.get("state")
                new_state = state
                update = 0

                if text == "Restart":
                    if self.restart_chatbot(self.number):
                        return "Chat has been Restarted"
        
            # node_change_list= self.keyword_state_change(text,state,update,new_state)
            # if node_change_list !=False:
            #     state=node_change_list[0]
            #     update=node_change_list[1]
            #     new_state=node_change_list[2]


                
                print("Before updating state in processing:", state)
                if state == "lang":
                    try:
                        # text = text.lower()  # Remove this line since it's already converted to lowercase earlier
                        if text.lower() not in ["english", "tamil", "hindi", "telugu", "malayalam", "kannada"]:
                            raise Exception

                        # Update the "language" column in the worksheet
                        self.chat.update_chat(self.number, "lang", "lang", text)
                        update = 1
                        chat_lang = text.lower()
                        state = "design"
                        print("Transitioning to 'design' state")
                        new_state = state
                    except Exception as e:
                        print("Error occurred")
                        warning_msg = self.text_translate(chat_lang, "Please enter a valid input")
                        err_msg = f"{warning_msg}\n\n{intent[chat_lang][state]['question']}"
                        self.send_list(self.number, err_msg, intent[chat_lang][state]['list'])

                    print("After updating state in processing:", state)
                    
                elif state=="design":
                    #print("inside enroll")
                    try:
                        # text = text.lower()  # Remove this line since it's already converted to lowercase earlier
                        if text not in ["Inivitation", "Poster", "Social Media Post", "Advertisement", "Presentation"]:
                            raise Exception

                        # Update the "language" column in the worksheet
                        update = 1
                        chat_lang = text.lower()
                        state = "output_type"
                        print("Transitioning to 'output_type' state")
                        new_state = state
                    except Exception as e:
                        print("Error occurred")
                        warning_msg = self.text_translate(chat_lang, "Please enter a valid input")
                        err_msg = f"{warning_msg}\n\n{intent[chat_lang][state]['question']}"
                        self.send_list(self.number, err_msg, intent[chat_lang][state]['list'])
                    print("After updating state in processing:", state)

                elif state=="output_type":
                    #print("inside enroll")
                    try:
                        chat_lang = chat_lang.lower()                   
                        if text not in ["Image", "GIF", "Short Video", "Long Video"]:
                            raise Exception
                            
                            
                        update=1
                        self.chat.update_last_activity(self.number)
                        #chat_lang = text.lower()
                        # state=f"design.{state}"
                        state="function"
                        new_state = state
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
                            state="end"
                            order=1
                            new_state=state
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

            except Exception as e:
                print(f"Error in processing: {e}")
                return "Error in processing."

            

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