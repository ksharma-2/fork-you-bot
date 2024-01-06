from typing import Union

import discord
import pymongo
from utils import UserMessage


class MongoDbHandler:

    def __init__(self, connection_string: str, password: str):
        self.conn_str = connection_string.replace('<password>', password)
        self.client = pymongo.MongoClient(self.conn_str)
        self.db = self.client["db"]

    def updateUserScore(self, message: UserMessage) -> bool:
        try:
            existsUser = self.db.users.find_one({
                "author": message.author,
                "server": message.server
            })
            if existsUser:
                if "tags_count" not in existsUser:
                    existsUser["tags_count"] = {}
                tcd = existsUser["tags_count"]
                for tag, count in message.tags_count.items():
                    if tag in tcd:
                        tcd[tag] += count
                    else:
                        tcd[tag] = count
                self.db.users.update_one({
                    "author": existsUser['author'],
                    "server": existsUser['server']
                }, {
                    "$set": {"score": existsUser['score'] + message.score, "tags_count": tcd}
                })
            else:
                self.db.users.insert_one({
                    "author": message.author,
                    "server": message.server,
                    "score": message.score,
                    "tags_count": message.tags_count
                })
            return True
        except Exception as e:
            print(e)
            return False

    def getUserDetails(self, server_id, user_id) -> Union[dict, None]:
        try:
            return self.db.users.find_one({
                "server": server_id,
                "author": user_id
            })
        except Exception as e:
            print(e)
            return None

    def getTopOffensive(self, client: discord.Client, guild_id: int) -> list:
        guild = client.get_guild(guild_id)
        res = []
        for member in guild.members:
            data = self.getUserDetails(guild_id, member.id)
            if not data : 
                continue
            df = {
                    "name": member.display_name,
                    "score": data["score"],
                    "tags_count": data["tags_count"],
                }
            df["image_url"] = member.display_avatar.url
            res.append(df)
        res = sorted(res, key=lambda x: -x["score"])
        return res
