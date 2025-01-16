import discord
from discord.ext import commands
import os
import nacl
from dotenv import load_dotenv
from queue import Queue
from googleapiclient.discovery import build
from yt_dlp import YoutubeDL
import time
import googleapiclient.http
import asyncio
import re

q = Queue()
finished = 0

load_dotenv()

token = os.getenv("TOKEN")
key = os.getenv("Y2BE")

service = build('youtube', 'v3', developerKey=key)

collection = service.search()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True          # Enable privileged intent for member updates
intents.presences = True        # Enable privileged intent for presence updates

bot = commands.Bot(command_prefix='$', intents=intents)

ffmpeg_options = {'options': "-vn"}

def audio_dl(url):

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': './audio',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality':'192'
        }]
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    
    return 'audio.mp3'


@bot.command()
async def queue(ctx, *, arg):
    global q
    print(arg)
    
    arg = '+'.join(arg.split())
    
    request = collection.list(
        part="snippet",
        maxResults=1,
        q=arg,
        fields='items/id/videoId'
    )

    try:
        

        if not ctx.voice_client == None and ctx.voice_client.is_connected():
        
            response = request.execute()
            print(response)
            vid_id = response["items"][0]["id"]['videoId']

            url = 'https://www.youtube.com/watch?v=' + str(vid_id)

            q.put(url)
            print(list(q.queue))
        
        else:

            channel = ctx.author.voice.channel
            await channel.connect()

            if not ctx.voice_client == None and ctx.voice_client.is_connected():
                response = request.execute()
                print(response)
                vid_id = response["items"][0]["id"]['videoId']

                url = 'https://www.youtube.com/watch?v=' + str(vid_id)

                q.put(url)
                print(list(q.queue))
            
            else:
                await ctx.send('Error connecting')
            

    except Exception as e:

        await ctx.send(f"Caugh exception: {e}")


def after_song(ctx, source):
    global finished

    #source.cleanup()
    c = ctx.voice_client
    
    
    if c.is_playing():
        c.stop()
    
    if os.path.exists('./audio.mp3'):
        os.remove('audio.mp3')
        
    finished = 0
    

@bot.command()
async def play(ctx, *, arg):
    global q, finished

    x = re.findall("^https://www.youtube.com/watch?v=", arg)

    if x:
        arg = x[0]
        print('link')
        try:
            
            
            channel = ctx.author.voice.channel

            if ctx.voice_client == None or not ctx.voice_client.is_connected():

                await channel.connect()
                await ctx.send(f'Connected to {channel}')
                print('\n')
            
            finished = 0
            print(list(q.queue))
            while q.qsize() > 0:
                
                if finished == 0:
                    source = discord.FFmpegPCMAudio(audio_dl(q.get()), **ffmpeg_options, executable = 'ffmpeg')
                    
                    ctx.voice_client.play(source, after = lambda x: after_song(ctx))
                    finished = 1
                
                else:
                    await asyncio.sleep(0.01)
                
                
            
            await ctx.send('Done queue')
            
            await ctx.send('done')
            await ctx.send('Queue Finished! use !queue to add more videos')
        
            # Play music
            

        except Exception as e:
            print('Error response status code : ', e)
            url = "Error"

    else:

        arg = '+'.join(arg.split())
        arg = arg + '+lyrics'
        request = collection.list(
            part="snippet",
            maxResults=1,
            q=arg,
            fields='items/id/videoId'
        )

        guild = ctx.message.guild

        try:
            
            response = request.execute()
            
            vid_id = response["items"][0]["id"]['videoId']

            url = 'https://www.youtube.com/watch?v=' + str(vid_id)
            print(url, '\n')

            q.put(url)
            
            channel = ctx.author.voice.channel

            if ctx.voice_client == None or not ctx.voice_client.is_connected():

                await channel.connect()
                await ctx.send(f'Connected to {channel}')
                print('\n')
            
            finished = 0
            print(list(q.queue))
            while q.qsize() > 0:
                
                if finished == 0:
                    source = discord.FFmpegPCMAudio(audio_dl(q.get()), **ffmpeg_options, executable = 'ffmpeg')
                    ctx.voice_client.play(source, after = lambda x: after_song(ctx, source))
                    finished = 1
                
                else:
                    await asyncio.sleep(0.01)
                
            await ctx.send('Queue finished, use !queue to add more videos')
        
            # Play music
            

        except Exception as e:
            print('Error response status code : ', e)
            url = "Error"
    
@bot.command()
async def info(ctx):

    message = (
        '*----------------------------* \n' +
        '* $play - play audio query \n' +
        '* $queue - queue audio \n' +
        '* $stop - stop audio \n' +
        '* $info - list commands \n' +
        '*----------------------------* \n'
    )

    await ctx.send(message)



@bot.command()
async def stop(ctx):

    c = ctx.voice_client

    try:

        if ctx.voice_client == None or c.is_connected():
            
            await c.disconnect()
            
            await ctx.send('Bot disconnected')

            try:

                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                await bot.close()

            except Exception as e:
                ctx.send('Bot disconnected')

        else:
            
            await ctx.send('Bot not connected')
            
            await bot.close()
        
    except:
        await ctx.send("Error disconnecting bot")
        #await bot.close()



bot.run(token)




