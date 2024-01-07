import os
import threading

import discord
import flask
import sys
from discord import app_commands
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta
from flask import request
from flask_cors import CORS
from utils import get_message_details
from db import MongoDbHandler
from moderator.moderator import addToContextStream, startContextStream

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guild = discord.Guild

ids = dict()
checkID = set()

app = flask.Flask(__name__)
CORS(app)

@client.event
async def on_message(message):
    message_content = message.content
    message_author = message.author
    channel_id = message.channel.id
    message_id = message.id
    message_author_id = message.author.id
    message_server = message.guild.id
    
    if not (channel_id in checkID):
        checkID.add(channel_id)
        contextID = startContextStream()
        ids[channel_id] = contextID
        
    contextID = ids[channel_id]
        
    isFlagged, reasonForFlag = addToContextStream(contextID, message_id, message_content)
                        
    if isFlagged:
        title = "Your Message was Flagged!"
        description = "The following message '" + str(message_content) + "' was flagged \n Reason for flag: " + ", ".join(reasonForFlag)
        embed = discord.Embed(title = title, description = description)
        await message_author.send(embed=embed)
        # await message_author.send("Your Message was Flagged!\n The following message '" + str(message_content) +  "' was flagged \n Reason for flag: " + ", ".join(reasonForFlag))
        await message.delete()
        is_successful = DB.updateUserScore(message_author_id, message_server)
        if is_successful:
            print("Updated user info")
        else:
            print("User update failed")

        user_details = DB.getUserDetails(message_server,message_author_id)
        if (user_details['score'] + 1 > 11):
            await message_author.kick()
        if (user_details['score'] + 1 > 10):
            await message_author.timeout(timedelta(minutes=15))
        if (user_details['score'] + 1 > 5):
            await message_author.timeout(timedelta(minutes=5))
        # print(user_details)
        # print(message_author)

@client.event
async def on_ready():
    print("Bot Ready!")

def start_server():
    print("Starting server")
    app.run(debug=False)

if __name__ == "__main__":
    DB = MongoDbHandler(os.environ["DB_URL"], os.environ["DB_PASSWORD"])
    thread = threading.Thread(target=start_server, args=[])
    thread.start()
    client.run(os.environ["DISCORD_CLIENT_SECRET"])