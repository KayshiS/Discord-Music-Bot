Discord Music Bot Setup and Usage Guide

SETUP

Pull repository locally, make sure to populate .env file with Discord Developer Bot Token and YouTube Data API v3 Key when they are available.
Create a bot through Discord's advanced tab and enabling Developer tools. Then, log on to dev portal on web browser and create a bot with a suitable name for the music functionalities. Then, go to the OAuth2 tab and use the client id of the bot to copy the invite url for the new discord bot. The invite url is in the Installation tab. Use the url in a browser and invite to a guild (server) as necessary. 

USAGE

After the music bot is in the server, make sure to grab the Discord Developer Bot Token from the Bot tab and use it in the .env file. Similarly, retrieve a YouTube Data API v3 key from the Google developer portal. After ensuring that the token and key are in the .env file, run the Python bot script. 

COMMANDS

When in a voice channel in a server, use the following command set to use the discord bot.


$play - play audio query

$queue - queue audio

$stop - stop audio

$info - list commands

Note that the play and queue commands should have search terms for the Data API to query. These search terms are analogous to YouTube searches.
