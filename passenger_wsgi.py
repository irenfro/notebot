#	Used this for stack trace when I cant view the Passenger error logs	
#	try:
#	except Exception as e:
#		error_log(traceback.format_exc())

 #!/usr/bin/python
import sys, os, json, datetime

# Run our local virtualenv python interpreter; all custom modules must be below here
INTERP = os.path.join(os.environ['HOME'], 'ir.thirty2k.com', 'bin', 'python')
if sys.executable != INTERP:
	os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

import requests
from backend import Help, newNote, printNotes, append, delete, clear, display
from flask import Flask, request
import flask
import traceback
application = Flask(__name__)

#A way to error log for Passenger
def error_log(str):
	file = open("error.log", "a")
	file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': ')
	file.write(str + "\n")
	file.close()

#Server/firstbot/webhook this is the address at which the code will run on a GET request 
#My current server ir.thirty2k.com
@application.route('/firstbot/webhook', methods=['GET'])
def verify():
	#Verify that the traffic we are receiving is from our Facebook page 
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if request.args.get("hub.verify_token") == "}rq9EsNbzRXCZq":
			return request.args.get("hub.challenge"), 200
		return "Verification token mismatch", 404
	return "Hello World!", 200

#Server/firstbot/webhook this is the address at which the code will run on a POST request 
#My current server ir.thirty2k.com
@application.route('/firstbot/webhook', methods=['POST'])
def webhook():
	try:
		#Checking to see if the request that we received has json in it
		if not request.is_json:
			#Log to our error file that we did not see json
			error_log("Did not receive json, request: " + str(request))
			return "Did not receive json", 404	
		#Get the json from the POST request	
		post_body = request.get_json()
		#Log the json that we received
		error_log(str(post_body))
		#Make sure this is a page subscription
		if post_body["object"] == "page":
			#Iterate over the events
			for entry in post_body["entry"]:
				#Iterate over the messages
				for message_event in entry["messaging"]:
					#There is a new message
					if message_event.get("message"):
						#The Facebook ID of whoever is sending us a message
						sender = message_event["sender"]["id"]
						#Our Facebook ID
						recip = message_event["recipient"]["id"]
						if message_event["message"].get("attachments"):
							for attach in message_event["message"]["attachments"]:
								attach_type = attach["type"]
								url = attach["payload"]["url"]
								error_log("There was an attachment in the message.  It was a "+attach_type+" and the url is: "+url)
								text = "I do not like "+attach_type+" messages"	
						else:
							#The message content
							#text = "Simon says: "+message_event["message"]["text"]
							text = back(str(message_event["message"]["text"]))
						#Check and make sure that we have good data
						if not check_data(sender, recip, text):
							continue
						error_log("sender: "+str(sender)+" recip: "+str(recip))
						#Log what we are sending to who
						error_log("sending "+text+" to "+str(sender))
						#Send the message
						send_message(sender, text)
						#Try to get User information.  Only do this once.  So check if we have seen them before calling again
						#get_user_info(sender)
					#Confirmation that our message was delivered 
					#Not needed if message_deliveries is not selected for webhooks
					if message_event.get("delivery"):
						pass
					#Optin confirmation
					#Not needed is messaginf_optin is not selected for webhooks
					if message_event.get("optin"):
						pass
					#User clicked or tapped the postback button from an earlier message, such as a Postback button, Getting Started button, a Menu Button or a Structured Message button
					#Not needed if messaging_postbacks is not slected for webhooks
					if message_event.get("postback"):
	                                        pass
        except Exception as e:
		error_log(traceback.format_exc())
	
	return "Read the data", 200

def back(command):
        command = command.lower()
	if (command == "help"):
            	return Help()
        elif ("new note" in command and len(command.split()) == 3):
            	return newNote(command)
        elif ("list" in command):
            	return printNotes(command)
        elif ("append" in command):
            	return append(command)
        elif ("display" in command):
            	return display(command)
        elif ("delete" in command):
           	return delete(command)
        elif ("clear" in command):
            	return clear(command)
        else:
            	return "Invalid command, type help for a list of commands"

def send_message(rid, message_text):
	#Page Access Token
	params = {
		"access_token" : "EAADgLfVtZAJYBAAZB1cmPUJNbZBXj8nqUtZAJISUPEh2VtraLdKOn5y5qAMCym9krpgn9awC45MnLPxgZCK0k1ZB6ZApxTbOLIoWhI4HzzUgFIquX3kleahxqBu2sCUfVXLl4PBMd99pXLjoaD2J2vTauLA44UqxZCRL1GVD4CKspAZDZD"
	}
	#Encode the data into json
	data = json.dumps({
		"recipient": {
			"id" : rid
		},
		"message": {
			"text": message_text
		}
	})
	#Add the the conent type and length 
	headers = {
		"Content-Type" : "application/json",
		"Content-Length" : len(data)
	}
	#API URL and combine the params, headers and data
	#Make the request
	response = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
	#Log the return status code
	error_log("Status Code: "+str(response.status_code))
	#Log the returned response text
	error_log("Response Text: "+response.text)
	return

#Check all of the information that is passed in and make sure that it is valid
def check_data(send_id, recip_id, text):
	#Make sure that the ID is a valid ID
	if not send_id.isnumeric():
		error_log("skipping non-numeric sender: "+str(sender))
		return False
	#Make sure that we dont send messages to ourselves
	if send_id == 1767288733508259:
		error_log("skipping self-message")
		return False
	#Make sure that it is not an empty message
	if len(text) <= 0:
		error_log("skipping empty text: "+text)
		return False
	if send_id == recip_id:
		error_log("The sender's ID is the same as the recipient's ID.  Sender ID: "+str(sender)+" Recipient ID: "+str(recip_id))
		return False
	return True


#A method that sends a get request for the user profile api of facebook and then logs the response
def get_user_info(send_id):
	url = "https://graph.facebook.com/v2.6/"+str(send_id)
	fields = ["first_name", "last_name", "profile_pic", "locale", "timezone", "gender"]
	params = {
		"fields" : ','.join(fields),
		"access_token" : "EAADgLfVtZAJYBAAZB1cmPUJNbZBXj8nqUtZAJISUPEh2VtraLdKOn5y5qAMCym9krpgn9awC45MnLPxgZCK0k1ZB6ZApxTbOLIoWhI4HzzUgFIquX3kleahxqBu2sCUfVXLl4PBMd99pXLjoaD2J2vTauLA44UqxZCRL1GVD4CKspAZDZD"
	}
	response = requests.get(url, params=params)
	error_log("Getting user information")
	error_log("Status code: "+str(response.status_code))
	if not response.status_code == 200:
		error_log("Response Text: "+response.text)
		return
	r = response.json()
	for params in fields:
		error.log(params + str(r[params]))	
	return r
