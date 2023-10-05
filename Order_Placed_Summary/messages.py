import requests
import json
import os
import gridfs
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from dotenv import load_dotenv



""" 
Uncomment the below line for production  for pythonanywhere production , Replace <loc> with location of folder in pythonanywhere
And Comment  the line : load_dotenv()
and  vice vera for localhost
"""
#load_dotenv(os.path.join("/home/<loc>", '.env'))

load_dotenv()

API_URL=os.getenv("API_URL")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
IMAGES_DIR=os.getenv("IMAGES_DIR")
VIDEO_DIR=os.getenv("VIDEO_DIR")

count = 0

def send_message(contact_number, message):
	headers = {
					'Authorization': ACCESS_TOKEN,
				}
	payload={'messageText': message}

	url = f"{API_URL}/api/v1/sendSessionMessage/"+ f'{contact_number}'
	response = requests.post(url=url, headers=headers,data=payload)
	return response.status_code

def send_image_message(contact_number,image, caption):
    url = f"{API_URL}/api/v1/sendSessionFile/{contact_number}?caption={caption}"

    payload = {}
    files=[
    ('file',('file',open(image,'rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': ACCESS_TOKEN
    }

    response = requests.post(url, headers=headers, json=payload, files=files)
    print(response)
    print(response.json())

# def send_video_message(contact_number, video_url, caption):
#     url = f"{API_URL}/api/v1/sendSessionFile/{contact_number}?caption={caption}"

#     payload = {}
#     files = [
#         ('file', ('file.mp4', requests.get(video_url).content, 'video/mp4'))  # Download the video and specify the correct content type
#     ]

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     response = requests.post(url, headers=headers, json=payload, files=files)
#     print(response)
#     print(response.json())

def send_video_message(contact_number, video, caption):
    url = f"{API_URL}/api/v1/sendSessionFile/{contact_number}?caption={caption}"

    payload = {}
    files = [
        ('file', ('video.mp4', open(video, 'rb'), 'video/mp4'))
    ]
    headers = {
        'Authorization': ACCESS_TOKEN
    }

    response = requests.post(url, headers=headers, json=payload, files=files)
    print(response)
    print(response.json())
    
##-------------------------------- Customized image message sending -----------------------------------------------------------------------------   ##

def send_images(contact_number,option):
    dir=IMAGES_DIR
    if option =="Shirt":
        image1=f'{dir}/s_image1.png'
        image2=f'{dir}/s_image2.png'
        

    else:
        image1=f'{dir}/ts_image1.jpg'
        image2=f'{dir}/ts_image2.jpg'
       
        
    send_image_message(contact_number,image1, "Image1")
    send_image_message(contact_number,image2, "Image2")

## ------------------------------------- --------------------------------------------------------------------------------------------------------##         
        
##-------------------------------- Customized video message sending -----------------------------------------------------------------------------   ##

def send_videos(contact_number):
    # dir="C:/Users/Akshaya Micheal/Downloads/personal-bot-new/video"
    # video=f'{dir}/sample-5s.mp4'        
    # send_video_message(contact_number,video, "Demo")
    
    # contact_number = "user123"
    # video_path = "path_to_your_video.mp4"
    # dir="C:/Users/Akshaya Micheal/Downloads/personal-bot-new/video"
    dir="D:/New project/A/Python/Latest File of Personal Bot/personal-bot/video"
    video_path=f'{dir}/sample-5s.mp4'
    caption = "Check out this video!"
    send_video_message(contact_number, video_path, caption)

## ------------------------------------- --------------------------------------------------------------------------------------------------------##         
         

def send_reply_button(contact_number, message, buttons):
    payload = {
    
    "body": message,
    "buttons": buttons
    }

    url = f"{API_URL}/api/v1/sendInteractiveButtonsMessage?whatsappNumber="+f"{contact_number}"
    headers = {
                'Authorization': ACCESS_TOKEN,
                'Content-Type': 'application/json'
            }
    response = requests.request("POST", url, headers=headers, json=payload)
    return response.status_code

def send_list(contact_number, message, sections):
    url = f"{API_URL}/api/v1/sendInteractiveListMessage?whatsappNumber={contact_number}"
    payload = {
         "body": message,
         "buttonText": "Select",
         "sections": sections
    }

    headers = {
                'Authorization': ACCESS_TOKEN,
                'Content-Type': 'application/json'
            }
    response = requests.request("POST", url, headers=headers, json=payload)
    return response.status_code

def get_media(filename):
    url = f"{API_URL}/api/v1/getMedia"

    payload = {'fileName': filename}
    
    headers = {
    'Authorization': ACCESS_TOKEN
    }

    response = requests.get(url, headers=headers, data=payload)
    return response

#----------------------------------------------------------- Image uploading on server -------------------------------------------------------#
def upload_image(filename, loc):
    response= get_media(filename)
    filename=filename.split("/")[-1]
    if response.status_code==200:
        #file=fs.put(response.content, filename=filename)
        
        with open(f'{loc}/{filename}', "wb") as f:
                f.write(response.content)
       
        #print(file)
        print("Upload Complete")
        return f"{loc}/{filename}"
    
    return False

# ----------------------------------------------------------Video send for New User-------------------------------------------- #    

# def send_video(contact_number, video_url, caption=""):
#         payload = {
#             "url": video_url,
#             "caption": caption
#         }
        
#         headers = {
#             "Authorization": ACCESS_TOKEN
#         }

#         url = f"{API_URL}/api/v1/sendSessionVideo/{contact_number}"
#         response = requests.post(url, headers=headers, json=payload)
#         print(f"Sending video to user {contact_number}: {video_url}")
#         print(f"Caption: {caption}")

#         return response.status_code
        
# def send_whatsapp_message(order_id, API_URL, ACCESS_TOKEN):
#     payload = {
#         "phone": 'whatsapp:7892409211',  # Replace with recipient's WhatsApp number
#         "body": f"New order received! Order ID: {order_id}"
#     }

#     headers = {
#         "Authorization": ACCESS_TOKEN
#     }

#     url = f"{API_URL}/api/v1/sendMessage"
#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(f"Failed to send WhatsApp message. Status code: {response.status_code}")
#         print(response.text)

# -------------------------------------Send Mail-------------------------------------------------#

def send_email(subject, message_body, to_email, attachments=None):
    from_email = 'arunacjeyakumar@gmail.com'
    password = 'Mithun@16'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_body, 'plain'))

    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {attachment}')
                msg.attach(part)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)  # Replace with your SMTP server details
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

#----------------------------------------SEND IMAGES--------------------------------------------------------#

def send_images_one_by_one(contact_number):
    dir = "D:/New project/A/Python/Latest File of Personal Bot/personal-bot/images"
    image_files = ['ts_image1.jpg', 'ts_image2.jpg', 'ts_image3.jpg']

    for i, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(dir, image_file)
        caption = f"Image {i}/10"  # Create a caption for the image
        send_image_message(contact_number, image_path, caption)

        # Notify the user about the progress
        progress_msg = f"Image {i}/10 sent"
        send_message(contact_number, progress_msg)

        # Sleep for a short while to simulate the process
        time.sleep(1)
        
        
#-----------------------------------SEND ORDER IMAGES------------------------------------------------------------------#
# def send_order_images(contact_number, order_id):
#     # Send an image
#     dir =  "C:\\Users\\Ramesh\\Downloads\\personal-bot-main\\personal-bot-main\\order-images"  # replace with your images directory
#     image_path = f'{dir}/{order_id}.jpg'  # replace 'sample.jpg' with your image filename
#     caption = "Check out this image!"
#     send_image_message(contact_number, image_path, caption)  # assuming you have a function named send_image_message

def send_order_images(self):
    # Iterate over the orders
    for order in self.db.find():
        order_id = order['order_id']
        phone_number = order['phone_number']
        status = order.get('status', None)

        # Check if the status is 'not sent' and an image exists for this order_id
        if status == 'not sent':
            # Check if an image exists for this order_id in the local drive
            image_path = f'C:\\Users\\Ramesh\\Downloads\\personal-bot-main\\personal-bot-main\\order-images\\{order_id}.jpg'

            if os.path.isfile(image_path):
                # Send the image via MMS using the Twilio API
                caption = "Here is your image!"
                send_image_message(phone_number, image_path, caption)
                
                # Update the status to 'sent' in the order collection
                self.db.update_one({'order_id': order_id}, {'$set': {'status': 'sent'}})

#____________________________________________ORDER SUMMARY________________________________________________________

def format_order_summary(order):
        # Create a formatted order summary message
        order_summary = f"Order ID: {order['order_id']}\n"
        order_summary += f"Design: {order['design']}\n"
        order_summary += f"Output Type: {order['output_type']}\n"
        order_summary += f"Function: {order['function']}\n"
        order_summary += f"Created Date: {order['created_date']}\n"
        order_summary += f"Last Modified: {order['last_modified']}\n"
        order_summary += f"Phone Number: {order['phone_number']}\n"

        return order_summary
    
def get_orders_with_empty_summary(self):
    orders = self.db.find({"order_summary": ""})
    return orders

def send_order_summary(self, order):
    # Format the order details into an order summary message
    order_summary_message = self.format_order_summary(order)

    # Send the order summary message to the user's phoneNumber
    send_message(order["phone_number"], order_summary_message)

def update_order_summary_sent(self, order_id):
    self.db.update_one({"order_id": order_id}, {"$set": {"order_summary": "sent"}})
