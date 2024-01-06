# Hate Speech Monitor Backend

The hate-speech detection bot and server to get details. 

The bot provides 2 commands : 
1. ``/sync_commands`` : To sync slash commands to server during development.
2. ``/get_top`` : Get a sorted list of offenders and their offense scores.

The flask API provides 2 endpoints : 
1. ``/getGuilds`` : Get a list of guilds where the bot is active.
2. ``/guild/getTop?guild=<guild_id>`` : Get the sorted list of offender from the guild.

## Note
1. Refer to the ``.env.sample`` file to create a populated ``.env`` file to make the project work. 

## How to run

The app can be launched using the command : ``python bot/main.py`` from the root of the repository.

## Screenshots

Increases offense rating on negative comments, but keeps them same if comment is not offensive.

![img1](https://raw.githubusercontent.com/Hate-Speech-Monitor/.github/main/img/NLP_Screenshot_4.png)
![img2](https://raw.githubusercontent.com/Hate-Speech-Monitor/.github/main/img/NLP_Screenshot_5.png)
