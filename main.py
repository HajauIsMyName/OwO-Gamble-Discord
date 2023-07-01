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

    def loggerStatus(self, status: str = None, amount: int = 0):
        if status.lower() == "won":
            print(
                f"\x1b[43m{datetime.today().strftime('%d %b %Y %H:%M:%S')}\x1b[0m  - {self.GREEN}WON{self.RESET} - {amount:,} cowoncy")

        elif status.lower() == "lost":
            print(
                f"\x1b[43m{datetime.today().strftime('%d %b %Y %H:%M:%S')}\x1b[0m  - {self.RED}LOST{self.RESET} - {abs(amount):,} cowoncy")

        elif status.lower() == "cash":
            print(
                f"\x1b[43m{datetime.today().strftime('%d %b %Y %H:%M:%S')}\x1b[0m  - {self.CYAN}CASH{self.RESET} - You currently have {amount:,} cowoncy")


class Data:
    def __init__(self):
        with open("conf.json", "r") as file:
            self.data = json.load(file)
            self.token = str(self.data["token"])
            self.channel = int(self.data["channel"])
            self.bet = int(self.data["bet"])
            self.webhook = self.data["webhook"]


class Client(discord.Client, Data):
    def __init__(self, *args, **kwargs):
        discord.Client.__init__(self, *args, **kwargs)
        Data.__init__(self)

        self.total_win = 0
        self.total_lost = 0
        self.botID = 408785106942164992
        self.cmds = random.choice(["heads", "tails"])

    async def on_ready(self):
        channel = self.get_channel(self.channel)

        os.system("cls" if os.name == "nt" else "clear")
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------" * 5)

        while True:
            await channel.send(f"owocf {self.bet} {self.cmds}")
            logger.info(f"Sent {self.bet:,} cowoncy to {self.cmds}")
            await asyncio.sleep(7)

            await channel.send("owocash")
            logger.info("Checked cash")
            await asyncio.sleep(10)

    async def on_message(self, message):
        Format = CustomFormatter()
        await asyncio.sleep(5)

        if message.author == self.get_user(self.botID):
            if "⚠" in message.content:
                if not self.webhook["link"] == "":
                    async with aiohttp.ClientSession() as session:
                        webhook = discord.Webhook.from_url(
                            self.webhook["link"], adapter=discord.AsyncWebhookAdapter(session))
                        await webhook.send(f"<@{self.webhook['ping']}> Verification Found!")

                logger.critical("Detected Verification!")
                await self.close()

            elif "and you won" in message.content:
                Format.loggerStatus("won", self.bet)
                self.bet = self.bet

            elif "and you lost it all..." in message.content:
                Format.loggerStatus("lost", -self.bet)

                self.bet *= 2
                self.cmds = "tails" if self.cmds == "heads" else "heads"

            elif "currently" in message.content:
                currentCash = "".join(re.findall(
                    "[0-9]+", message.content[message.content.find("have")::]))
                Format.loggerStatus("cash", int(currentCash))

        elif message.author == self.user:
            if message.content == "stop":
                logger.info("Stopped")
                await self.close()


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
    client = Client(
        guild_subscription_options=discord.GuildSubscriptionOptions.off())

    try:
        client.run(client.token)

    except:
        pass
