import os
import threading

import discord
import flask
from discord import app_commands
from dotenv import load_dotenv
from flask import request
from flask_cors import CORS
from utils import get_message_details

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

app = flask.Flask(__name__)
CORS(app)


@client.event
async def on_ready():
    print("Bot Ready!")

def start_server():
    print("Starting server")
    app.run(debug=False)

if __name__ == "__main__":
    # DB = MongoDbHandler(os.environ["DB_URL"], os.environ["DB_PASSWORD"])
    # thread = threading.Thread(target=start_server, args=[])
    # thread.start()
    client.run(os.environ["DISCORD_CLIENT_SECRET"])