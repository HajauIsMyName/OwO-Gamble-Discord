import discord
import logging
import json
import os
import random
import asyncio
import re
import aiohttp

from logging.config import dictConfig
from datetime import datetime
from discord.ext import commands


class CustomFormatter(logging.Formatter):
    def __init__(self):
        self.GREY = "\x1b[38;5;240m"
        self.YELLOW = "\x1b[0;33m"
        self.CYAN = "\x1b[1;94m"
        self.RED = "\x1b[1;31m"
        self.GREEN = "\x1b[1;32m"
        self.BRIGHT_RED = "\x1b[1;41m"
        self.RESET = "\x1b[0m"
        self.FORMAT = "\x1b[0;43m%(asctime)s\x1b[0m  - {}%(levelname)s{} - %(message)s"

        self.FORMATS = {
            logging.DEBUG: self.FORMAT.format(self.GREY, self.RESET) + "(%(filename)s:%(lineno)d)",
            logging.INFO: self.FORMAT.format(self.CYAN, self.RESET),
            logging.WARNING: self.FORMAT.format(self.YELLOW, self.RESET),
            logging.ERROR: self.FORMAT.format(self.RED, self.RESET) + "(%(filename)s:%(lineno)d)",
            logging.CRITICAL: self.FORMAT.format(self.BRIGHT_RED, self.RESET)
            + "(%(filename)s:%(lineno)d)",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%d %b %Y %H:%M:%S")
        return formatter.format(record)

    def loggerStatus(self, amount=0):
        if amount >= 0:
            print(
                f"\x1b[43m{datetime.today().strftime('%d %b %Y %H:%M:%S')}\x1b[0m  - {self.GREEN}WON{self.RESET} - {amount:,} cowoncy")

        else:
            print(
                f"\x1b[43m{datetime.today().strftime('%d %b %Y %H:%M:%S')}\x1b[0m  - {self.RED}LOST{self.RESET} - {abs(amount):,} cowoncy")

    def loggerCash(self, cash=0):
        print(f"\x1b[43m{datetime.today().strftime('%d %b %Y %H:%M:%S')}\x1b[0m  - {self.CYAN}CASH{self.RESET} - You currently have {cash:,} cowoncy")


def returnJson(var=""):
    with open("conf.json", "r") as file:
        data = json.load(file)
        return data[var]


client = commands.Bot(command_prefix="hajauneverdie", help_command=None)
cmds = random.choice(["heads", "tails"])
bet = returnJson("bet")


@client.event
async def on_ready():
    channel = client.get_channel(returnJson("channel"))
    bet = returnJson("bet")

    os.system("cls" if os.name == "nt" else "clear")
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------" * 5)

    while True:
        await channel.send(f"owocf {bet} {cmds}")
        logger.info(f"Sent {bet:,} cowoncy to {cmds}")
        await asyncio.sleep(7)

        await channel.send("owocash")
        logger.info("Checked cash")
        await asyncio.sleep(10)


@client.event
async def on_message(message):
    global cmds, bet

    await asyncio.sleep(5)

    if message.author == client.get_user(408785106942164992):
        if "⚠" in message.content:
            link = returnJson("webhook")["link"]
            ping = returnJson("webhook")["ping"]

            if link:
                async with aiohttp.ClientSession() as session:
                    webhook = discord.Webhook.from_url(
                        link, adapter=discord.AsyncWebhookAdapter(session))
                    await webhook.send(f"<@{ping}> Verification Found!")

            logger.critical("Detected Verification!")
            await client.close()

        elif "and you won" in message.content:
            CustomFormatter().loggerStatus(bet)
            bet = returnJson("bet")

        elif "and you lost it all..." in message.content:
            CustomFormatter().loggerStatus(-bet)

            bet = returnJson("bet") if bet > 128000 else bet * 2
            cmds = "tails" if cmds == "heads" else "heads"

        elif "currently" in message.content:
            currentCash = "".join(re.findall(
                "[0-9]+", message.content[message.content.find("have")::]))
            CustomFormatter().loggerCash(int(currentCash))

    elif message.author == client.user:
        if message.content == "stop":
            logger.info("Stopped")
            await client.close()

dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
})
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


if __name__ == "__main__":
    try:
        token = returnJson("token")
        client.run(token)

    except:
        pass
