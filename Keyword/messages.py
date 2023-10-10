import requests
import json
import os
import gridfs
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

def get_media(filename):
    url = f"{API_URL}/api/v1/getMedia"

    payload = {'fileName': filename}
    
    headers = {
    'Authorization': ACCESS_TOKEN
    }

    response = requests.get(url, headers=headers, data=payload)
    return response

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

def send_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/Keyword/image"
    image_path=f'{dir}/bday.jpg'
    caption = "Check out this image!"
    send_image_message(contact_number, image_path, caption)
    

def send_audio_message(contact_number, audio, caption):
    url = f"{API_URL}/api/v1/sendSessionFile/{contact_number}?caption={caption}"

    # Prepare the payload and specify the file as 'audio/mpeg'
    payload = {}
    files = [
        ('file', ('audio.mp3', open(audio, 'rb'), 'audio/mpeg'))
    ]

    headers = {
        'Authorization': ACCESS_TOKEN
    }

    # Send the audio file using a POST request
    response = requests.post(url, headers=headers, json=payload, files=files)

    # Print the response and its JSON content
    print(response)
    print(response.json())


def send_audio(contact_number):
    dir = "C:/Users/Akshaya Micheal/Downloads/Keyword/audio"  # Replace with the directory containing your audio file
    audio_path = f'{dir}/sound.mp3'  # Replace with the audio file name
    caption = "Check out this audio message!"
    send_audio_message(contact_number, audio_path, caption)


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
    
def send_videos(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/Keyword/video"
    video_path=f'{dir}/sample-5s.mp4'
    caption = "Check out this video!"
    # caption = "Check out this video! For more details visit our website.\n\n https://www.dexa.co.in/"
    send_video_message(contact_number, video_path, caption)


# def send_link_message(contact_number, link, caption):
#     # # Check if caption and link are not empty or whitespace
#     # if not caption.strip() or not link.strip():
#     #     print("Caption or link is empty.")
#     #     return
    
#     url = f"{API_URL}/api/v1/sendSessionMessage/{contact_number}"

#     payload = {
#         'text': f"{caption}\n{link}"
#     }

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     # Send the link message using a POST request
#     response = requests.post(url, headers=headers, json=payload)

#     # Print the response and its JSON content
#     print(response)
#     print(response.json())


# def send_video_link(contact_number):
#     link = "https://www.dexa.co.in/"  # Replace with the link you want to send
#     caption = "Check out this link!"
#     send_link_message(contact_number, link, caption)



# def send_link_message(contact_number, link, caption):
#     url = f"{API_URL}/api/v1/sendSessionMessage/{contact_number}"

#     payload = {
#         'text': f"{caption}\n{link}"
#     }

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     print(response.status_code)
#     print(response.json())

# def send_video_link(contact_number):
#     link = "https://www.dexa.co.in/"
#     caption = "Check out this link!"
#     send_link_message(contact_number, link, caption)

# Example usage:
# send_video_link("recipient_contact_number")



# def send_text_message(contact_number, text_message):
#     url = f"{API_URL}/sendMessage"

#     headers = {
#         'Authorization': f'Bearer {ACCESS_TOKEN}'
#     }

#     payload = {
#         'phone': contact_number,  # The recipient's phone number in international format
#         'body': text_message
#     }

#     # Send the WhatsApp message using a POST request to the Wati API
#     response = requests.post(url, headers=headers, json=payload)

#     # Handle the response from the Wati API
#     print(response)
#     print(response.json())

# # # Call the function to send the WhatsApp message
# # send_whatsapp_message("recipient_number", "Hello, this is a test message.")



# def send_text_message(contact_number, text_message):
#     url = f"{API_URL}/api/v1/sendSessionMessage/{contact_number}"

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     payload = {
#         'text': text_message
#     }
#     # Send the text message using a POST request
#     response = requests.post(url, headers=headers, json=payload)

#     # Print the response and its JSON content
#     print(response)
#     print(response.json())


# def send_text(contact_number):
#     text_message = "https://www.dexa.co.in/"
#     send_text_message(contact_number, text_message)

def send_link_message(contact_number, link, caption):
    url = f"{API_URL}/api/v1/sendSessionMessage/{contact_number}"
    print(f"Link: {link}")
    print(f"Caption: {caption}")

    if caption and link:
        text_message = f"{caption}\n{link}"
    else:
        text_message = "Check out this link: " + link

    print(f"Text message: {text_message}")

    payload = {
        'text': text_message
    }
    print(f"Payload: {payload}")

    headers = {
        'Authorization': ACCESS_TOKEN
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  
        print(response)
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def send_video_link(contact_number):
    link = "https://www.dexa.co.in/"
    caption = "Check out this link!"
    send_link_message(contact_number, link, caption)


def send_message_link(contact_number, link_message):
    headers = {
        'Authorization': ACCESS_TOKEN,
    }

    # Include the link in the message
    message_with_link = f"{link_message} - https://www.dexa.co.in/"

    print(f"Sending message: {message_with_link}")

    payload = {'messageText': message_with_link}

    url = f"{API_URL}/api/v1/sendSessionMessage/{contact_number}"

    response = requests.post(url=url, headers=headers, data=payload)

    return response.status_code

    
    

# def send_text_message(contact_number, text):
#     url = f"{API_URL}/api/v1/sendSessionText/{contact_number}"

#     # No payload data other than the text message
#     payload = {}

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     response = requests.post(url, headers=headers, json=payload, data={'text': text})
#     print(response)
#     print(response.json())

# def send_text(contact_number):
#     text_message = "Hello, this is a text message!"
#     send_text_message(contact_number, text_message)

# def send_text_message(contact_number, text):
#     url = f"{API_URL}/api/v1/sendSessionText/{contact_number}"

#     # Create an empty payload (just the recipient's contact number)
#     payload = {
#         "text": ""
#     }

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     # Include the message text in the JSON payload
#     payload["text"] = text

#     response = requests.post(url, headers=headers, json=payload)
#     print(response)
#     print(response.json())

# def send_text(contact_number):
#     text_message = "Hello, this is a text message!"
#     send_text_message(contact_number, text_message)

# def send_text_message(contact_number, text):
#     url = f"{API_URL}/api/v1/sendSessionText/{contact_number}"

#     # No payload, the message will be sent in the URL query parameter
#     params = {
#         "text": text
#     }

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     response = requests.post(url, headers=headers, params=params)
#     print(response)
#     print(response.json())

# def send_text(contact_number):
#     text_message = "Hello, this is a text message with an empty payload!"
#     send_text_message(contact_number, text_message)

# def send_text_message(contact_number, text):
#     url = f"{API_URL}/api/v1/sendSessionText/{contact_number}"

#     # You can keep the payload empty in this case
#     payload = {}

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     # Send the text message directly in the POST request body
#     response = requests.post(url, headers=headers, data=text)
#     print(response)
#     print(response.json())

# def send_text(contact_number):
#     text_message = "Hello, this is a text message!"
#     send_text_message(contact_number, text_message)

# def send_text_message(contact_number, text):
#     url = f"{API_URL}/api/v1/sendSessionText/{contact_number}"

#     payload = {}

#     headers = {
#         'Authorization': ACCESS_TOKEN
#     }

#     response = requests.post(url, headers=headers, data=text)

#     if response.status_code == 200:
#         print("Message sent successfully.")
#     else:
#         print(f"Failed to send message. Status code: {response.status_code}")
#         print(response.text)

# def send_text(contact_number):
#     text_message = "Hello, this is a text message!"
#     send_text_message(contact_number, text_message)

  
# Function to send a PDF message
def send_pdf_message(contact_number, pdf_file, caption):
    url = f"{API_URL}/api/v1/sendSessionFile/{contact_number}?caption={caption}"

    # Prepare the payload and specify the file as 'application/pdf'
    payload = {}
    files = [
        ('file', ('file.pdf', open(pdf_file, 'rb'), 'application/pdf'))
    ]

    headers = {
        'Authorization': ACCESS_TOKEN
    }

    # Send the PDF file using a POST request
    response = requests.post(url, headers=headers, json=payload, files=files)

    # Print the response and its JSON content
    print(response)
    print(response.json())
    

def send_pdf(contact_number):
    dir = "D:/New Project/Python/Autobot Things/Keyword/pdf"  # Replace with the directory containing your PDF file
    pdf_path = f'{dir}/MAJD_2.pdf'  # Replace with the PDF file name
    caption = "PDF File"

    # Ensure the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"PDF file '{pdf_path}' not found.")
        return

    # Call the function to send the PDF
    send_pdf_message(contact_number, pdf_path, caption)

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

# ----------------------------------------------------------------------------------------------------------------------------------- #    

def send_bday_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/bpday_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_rwp_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_cong_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_welcome_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)
    
def send_achievement_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_protest_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_selfquote_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_quotes_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

def send_work_images(contact_number):
    dir="C:/Users/Akshaya Micheal/Downloads/political_bot(New)/rwp_images"
    image_path=f'{dir}/image1.jpg'
    caption = "Final Output!"
    send_image_message(contact_number, image_path, caption)

