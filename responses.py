import random 
# from features import zackfunc, spencefunc, dariusfunc, sevfunc, sidfunc, kevfunc
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
import os
load_dotenv()
from openai import OpenAI

def handle_response(message, author) -> str:
    # Standardize input
    obama_talk=os.getenv("obama_talk")
    trump_talk=os.getenv("trump_talk")
    biden_talk=os.getenv("biden_talk")
    p_message = message.lower()
    # Help function 
    #TODO: add all possible commands with brief description (maybe some formatting as well?)
    if p_message == 'help':
        return "nigga"

    if p_message == 'hello':
        return "I don’t quite understand your greeting, I’m still in development"
    
    if p_message == 'roll':
        return str(random.randint(1,6))

    #playlist functionality
    if 'obamasays' in p_message:
        index = p_message.index('obama')+9
        return getAudio(p_message[index:], obama_talk)
    elif 'trumpsays' in p_message:
        index = p_message.index('trump')+9
        return getAudio(p_message[index:], trump_talk)
    elif 'bidensays' in p_message:
        index = p_message.index('biden')+9
        return getAudio(p_message[index:], biden_talk)



    elif 'obama' in p_message:
        index = p_message.index('obama')+5
        return getAudio(recieveResponse('Obama', p_message[index:]), obama_talk)

    elif 'trump' in p_message:
        index = p_message.index('trump')+5
        return getAudio(recieveResponse("Trump", p_message[index:]), trump_talk)

    elif 'biden' in p_message:
        index = p_message.index('biden')+5
        return getAudio(recieveResponse("Biden", p_message[index:]), biden_talk)
    
import requests

my_secret = os.getenv("eleven")
import requests
def getAudio(chatToSpeech, voiceID):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voiceID}"
    querystring = {"output_format":"mp3_44100_64"}
    payload = {
        "text": chatToSpeech,
        "voice_settings": {
            "similarity_boost": 0,
            "stability": 1
        }
    }
    headers = {
        "xi-api-key": my_secret,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
    CHUNK_SIZE = 1024
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    return response






# @bot.command(pass_context=True)
# async def join(ctx, audio):
#     if(ctx.author.voice):
#         channel=ctx.message.author.voice.channel
#         voice=await channel.connect()
#         source=FFmpegPCMAudio()



def recieveResponse(president, prompt):
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are now President"+president+"""of the United States. You are feeling very goofy and will respond very meanly and sarcastically as if addressing the Nation
     You have no interest in other people's feeling and you are so angry at the politics that you will step on the toes of anyone who asks you a question. You are roleplaying a bad guy
     You like to bring up current world politics """},
    {"role": "user", "content": prompt+" and keep your response under 70 words"},
  ],
  max_tokens=70,

)
    # print(response.choices[0].message.content)
    return response.choices[0].message.content

    

    