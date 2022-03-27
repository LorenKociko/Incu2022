from flask import Flask, request
import requests
import json

############## Bot details ##############

bot_name = 'RedditNews@webex.bot'
token = 'OTYzYTY4MmMtM2RmMS00MDQ3LTgxZDEtNGJiYTE5MDlmODU5NmI0MzQ0MmUtNWU1_P0A1_262cf59f-1417-4dce-b04b-539e93368fe3'
header = {"content-type": "application/json; charset=utf-8", "authorization": "Bearer " + token}


def renewToken():
    CLIENT_ID= '1GVCtQUb6rHZ7N_TxwHsMg'
    SECRET_KEY='UOOwONrhkiBmGihZ-f6SVlRdvDz1sg'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    with open('account.txt','r') as f:
        pw = f.read()
    data ={
        'grant_type':'password',
        'username':'RedditNewsCisco',
        'password': pw
    }
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers = headers )
    TOKEN = res.json()['access_token']
    headers['Authorization']= f'bearer {TOKEN}'
    return headers
headers = renewToken()

############## Flask Application ##############
app = Flask(__name__)


def generatePrint(data):
    msg = f"# r/{data.json()['data']['children'][0]['data']['subreddit']}\n---\n---\n"
    for post in data.json()['data']['children']:
        msg+=f"### {post['data']['title']}\n>{post['data']['url']}\n\n---\n"
    return msg


@app.route("/", methods=["GET", "POST"])
def sendMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages'
    msg = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]
    message = getMessage()
    message_parts = message.split()
    if (sender != bot_name) and message_parts[0][0]=='*':
        command = message_parts[0].lower()
        if (command == "*news"):
            data = requests.get('https://oauth.reddit.com/r/worldnews/top', headers=headers)    
            msg["markdown"] = generatePrint(data)
        elif (command == "*peek"):
            if len(message_parts)==2:
                subreddit = message_parts[1]
                data = requests.get(f'https://oauth.reddit.com/r/{subreddit}/top', headers=headers)   
                if len(data.json())>2:
                        msg["markdown"] = "The subreddit doesn't exist!"
                else:
                    if not data.json()['data']['children']:
                        msg["markdown"] = "The subreddit doesn't exist!"
                    else:
                        msg["markdown"] = generatePrint(data)
            else:
                msg["markdown"] = 'The command is wrong, use *help for help'
        elif (command == "*help"):
            msg["markdown"] = "# RedditNews Help\n---\n### You can use the following commands:\n## *news \n>returns the latest news\n## *help \n>show the help menu \n## *peek  \n>peeks on other subreddits \n>>eg. *peek [SUBREDDIT_NAME]\n ## *about \n>more infos about this bot"
        elif (command == "*about"):
            msg["markdown"] = "# RedditNews About\n---\n### This bot was created by **Loren Kociko** for the needs of the Cisco Incubator 9.0 - Automation track. \n >https://www.linkedin.com/in/loren-kociko \n >https://github.com/LorenKociko \n>https://lorenkociko.com/"
        else:
            msg["markdown"] = "Sorry! I didn't recognize that command. Type ***help** to see the list of available commands."
        requests.post(url,data=json.dumps(msg), headers=header, verify=True)

def getMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers=header, verify=True)
    message = get_msgs.json()['text']
    return message

app.run(debug = True)
