import discord
import logging
import yaml
from otherdave.commands import haiku
from otherdave.commands.drunkdraw import drunkdraw
from otherdave.commands.mimic import *
from otherdave.commands.prompt import prompt
from otherdave.commands.respect import respect
from otherdave.util.dlog import dlog
from otherdave.util.triggers import *

# Configure client
with open("./conf.yaml") as conf:
    config = yaml.load(conf, Loader=yaml.BaseLoader)
client = discord.Client()
async def ping(client, message, args):
    await message.channel.send("pong")
async def version(client, message, args):
    await message.channel.send("OtherDave is running version " + str(config["version"]))

functions = {
    "drunkdraw": drunkdraw,
    "haiku": haiku.critique,
    "mimic": mimic,
    "ping": ping,
    "prompt": prompt,
    "respect": respect,
    "version": version
}

# Set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="./logs/otherdave.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

# Configure events
@client.event
async def on_ready():
    logger.debug("Logged in as {0.user}".format(client))
    await dlog(client, "Hi, I'm OtherDave and I'm BACK FOR BUSINESS.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content
    if content.startswith("!"):
        command, *args = content.lstrip("!").split(" ")
        logger.info(command + " - user: " + message.author.name)
        if command in functions:
            await functions[command](client, message, args)
        else:
            await message.channel.send("I'm sorry Dave, I'm afraid I can't do that.")

    else:
        await haiku.detect(message)
        await react(message)
        await pedant(message)

        # otherdave is always listening...
        listen(message)

if __name__ == "__main__":
    tokenFile = open("bot.tkn", "r")
    token = tokenFile.read()
    client.run(token)