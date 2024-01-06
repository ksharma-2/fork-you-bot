from typing import Union

import discord
from hatespeech import evaluate


class UserMessage:
    def __init__(self):
        self.content: str = ""
        self.author: int = 0
        self.server: Union[int,  None] = None
        self.score: int = 0
        self.tags_count: dict = {}

    def getOffensiveInfo(self):
        self.score, tags = evaluate(self.content)
        for tag in tags:
            if tag[0] in self.tags_count:
                self.tags_count[tag[0]] += 1
            else:
                self.tags_count[tag[0]] = 1


def get_message_details(message: discord.Message) -> UserMessage:
    d = UserMessage()
    d.content = message.content
    d.author = message.author.id
    if message.guild:
        d.server = message.guild.id
    d.getOffensiveInfo()
    return d


# def create_offensive_users_prompt(users: list) -> discord.Embed:
#     res = discord.Embed(
#         title="Top Offenders of Server",
#         color=discord.Color.red()
#     )
#     names = [str(user["name"]) for user in users]
#     scores = [str(user["score"]) for user in users]
#     res.add_field(name="Name", value="\n".join(names), inline=True)
#     res.add_field(name="Score", value="\n".join(scores), inline=True)
#     return res
