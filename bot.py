import discord
from discord.ext import commands, tasks
# from discord import ffmeg
from dotenv import load_dotenv
import os
import responses
from openai import OpenAI
import io
import asyncio

# import requests
# import re
# import json


# client=discord.Client()
# key=os.getenv("TOKEN")

def run_discord_bot():
    # Bot token import from .env, fix weird intents issue
    load_dotenv()
    my_secret = os.getenv("TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
    
    @bot.event
    async def send_message(message, user_message, is_private):
    # Handle response and send in PM or channel
    #   response=None
      try:
          response = responses.handle_response(user_message, message.author)
          if response:
            await join(message, response)
      except Exception as e: 
          print(e)


    # Message classification
    @bot.event
    async def on_message(message):
        # Avoid infinite loops
        if message.author == bot.user:
            return 
        # Grab author, content, channel
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f"{username} said: '{user_message}' ({channel})")

    #     # Determine if response will be in private message or channel it was received in
        if(user_message[0]=="!"):
            user_message = user_message[1:]

        # while(True):
        #    await message.channel.send("nigger")
        await send_message(message, user_message, is_private=False)
        # print(audio)
        

        # join(message, await send_message(message, user_message, is_private=False))

    async def join(message, audio):
        if message.author.voice and message.author.voice.channel:
            print("got here")
            channel = message.author.voice.channel
            voice_channel = await channel.connect()

            audio_source = discord.FFmpegPCMAudio("output.mp3")
            voice_channel.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)

            while voice_channel.is_playing():
                    await asyncio.sleep(1)
            await voice_channel.disconnect()
        else:
            await message.channel.send("You need to be in a voice channel to use this command.")




    
    ## remember source/activate.venv
    bot.run(my_secret)