# Keyword options on selection of list or button 
lang_list=["english", "tamil", "hindi", "telugu", "malayalam", "kannada"]

enroll_list={"english":["first time enroll", "enrolled & subscribed", "enrolled not subscribed"],
             "tamil":["முதல் பதிவு", "சந்தா","குழுசேரவில்லை"]}

political_party_list={"english":["DMK","ADMK","PMK","BJP","Congress","ntk","Communist","AMMK","DMDK"],
                 "tamil":["தி.மு.க","அ.தி.மு.க","பா.ம.க", "பா.ஜ.க","காங்கிரஸ்","என்டிகே","கம்யூனிஸ்ட்","அமமுக","தே.மு.தி.க"]}

design_list = {"english":["social media post","banner"],
               "tamil":["சமூக ஊடக இடுகை", "பதாகை"]}

post_size_list = {"english":["whatsapp","facebook","instagram"],
                  "tamil":["பகிரி","இன்ஸ்டாகிராம்", "முகநூல்"]}

post_type_list={"english":["image", "video"],
                "tamil":["படம்", "வீடியோ"]}

post_design_list={"english":["birthday post", "regular wishes post","congratulation post","welcome post", "achievement post","protest post", "self quote post","quotes post","work update post"],
                  "tamil":["பிறந்தநாள் இடுகை","வழக்கமான வாழ்த்து இடுகை","வாழ்த்து இடுகை", "வரவேற்பு இடுகை", "சாதனை இடுகை", "எதிர்ப்பு இடுகை", "சுய மேற்கோள் இடுகை","மேற்கோள் இடுகை","பணி புதுப்பிப்பு இடுகை" ]}

wish_list={"english":["good morning","good evening","good night", "function wise"],
           "tamil":["காலை வணக்கம்", "மாலை வணக்கம்", "இனிய இரவு","செயல்பாடு வாரியாக"]}

work_list ={"english":["daily","weekly","monthly"],
            "tamil":["தினசரி", "வாரந்தோறும்", "மாதாந்திர"]}


# A function changing when a particular keyword strikes

# def keyword_node(text):
#         state="None"


#         if text in ["birthday","Birth day","birthday poster","birthday design","birthday card","birthday wish","birth day wish","birth day poster","son birthday","baby birthday","பிறந்த நாள்", "பிறந்த நாள்", "பிறந்தநாள் போஸ்டர்", "பிறந்தநாள் வடிவமைப்பு", "பிறந்தநாள் அட்டை", "பிறந்தநாள் வாழ்த்துக்கள்", "பிறந்த நாள் வாழ்த்துக்கள்", "பிறந்தநாள் போஸ்டர்", "மகன் பிறந்த நாள்", "குழந்தை பிறந்த நாள்"]:
#             # # Define the query to find the document(s) you want to update
#             # print(text)
#             # query = {"post_design": text}  # Replace with your actual query criteria
#             # print(query)

#             # # Define the update operation to set the post_design field to "Birthday Post"
#             # update = {"$set": {"post_design": "Birthday Post"}}

#             # # Use the update_one() method to update a single document that matches the query
#             # result = collection.update_one(query, update)

#             # # Check if the update was successful
#             # if result.modified_count > 0:
#             #     print("Document updated successfully.")
#             # else:
#             #     print("No documents matched the query.")
#             state="post_name"
        
#         # if text in ["birthday", "Birth day", "birthday poster", "birthday design", "birthday card", "birthday wish", "birth day wish", "birth day poster", "son birthday", "baby birthday"]:
#         #     state="post_name"
            
#         elif text in ["wish","good morning", "good evening", "good night", "வாழ்த்துக்கள்", "காலை வணக்கம்", "மாலை வணக்கம்", "இரவு வணக்கம்"]:
#             state="wish"

#         elif text in ["congratulation","congratulations","congrats","congrat","thank","thanks","வாழ்த்துக்கள்", "வாழ்த்துக்கள்", "வாழ்த்துக்கள்", "வாழ்த்துக்கள்", "நன்றி", "நன்றி"]:
#             state="post_name"

#         elif text in ["welcome","arriving","arrive","வரவேற்கிறேன்","வருகிறேன்","வந்தேன்"]:
#             state="post_name"

#         elif text in ["achievement","achieve","சாதனை","சாதனை"]:
#             state="post_name"

#         elif text in ["quote","self quote","my mind","my thoughts","vision","message","மேற்கோள்", "சுய மேற்கோள்", "என் மனம்", "என் எண்ணங்கள்", "பார்வை", "செய்தி"]:
#             state="self_quote"

#         elif text in ["work","வேலை"]:
#             state="work"
        
#         elif text in ["image design", "image edit", "poster"]:
#             state="post_size"
            
#         elif text in ["facebook status"]:
#             state="post_type"
            
#         elif text in ["instagram post"]:
#             state="post_type"
            
#         elif text in ["banner"]:
#             state="banner_size"
            
#         elif text in ["Pdf", "PDF", "pdf"]:
#             # state="send_pdf"
#             contact_number = self.number
#             print(contact_number)
#             self.send_pdf(contact_number)

#         return state