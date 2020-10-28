import os 
from dotenv import load_dotenv
from discord.ext import commands
import discord
import asyncio
import logging

MINUTES_BETWEEN_ALERTS = 30

def startBot():
    bot = commands.Bot(command_prefix="!")

    @bot.command(name="hydrated",help="Removes you from the role to alert you to drink water.")
    async def hydrationSuccess(ctx):
        logger.info(f"User {ctx.author.display_name} in guild {ctx.author.guild} says that they are hydrated. Attempting to remove from ThirstyBois")
        role = discord.utils.find(lambda x: x.name == "ThirstyBois", ctx.author.roles)
        if role:
            logger.info("User is part of ThirstyBois. Removing")
            member = ctx.author
            role = discord.utils.get(member.guild.roles, name="ThirstyBois")
            await member.remove_roles(role)
            await ctx.send(f"Removed {member.display_name} from the ThirstyBois. Hydration achieved")
        else:
            logger.info("User is not part of ThirstyBois")
            member = ctx.author
            await ctx.send(f"Bruh. You aint a thirsty boi {member.display_name}. Come to the hydration station by entering !thirstyboi")

    @bot.command(name="thirstyboi",help="Adds you to the role 'ThirstyBois' so that you can be reminded to drink water and stretch")
    async def thirstyBoi(ctx):
        logger.info(f'Got message from {ctx.author} in guild {ctx.guild}. They are thirsty')
        role = discord.utils.find(lambda x: x.name == "ThirstyBois", ctx.author.roles)
        if role:
            await ctx.send("You are already a thirsty boi. Stay thirsty bb")
            logger.info("Already a thirsty boi")
        else:
            member = ctx.author
            role = discord.utils.get(member.guild.roles, name="ThirstyBois")
            await member.add_roles(role)
            await ctx.send(f"Added {member.display_name} to ThirstyBois. Now part of the hydration station")
            logger.info("User added to ThirstyBois")
    
    @bot.event
    async def on_guild_join(guild):
        logger.info(f"Joined guild {guild.name}")
        general = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
        role = discord.utils.find(lambda x: x.name == "ThirstyBois", guild.roles)
        if role:
            logger.info("ThirstyBois already exists in guild")
            await general.send("Hello! Seems like you already have the role ThirstyBois. YEET!")
        else:
            logger.info("ThirstBois does not exist in guild. Creating it.")
            color = discord.Color.blue()
            await guild.create_role(name="ThirstyBois",colour=color,mentionable=True)
            await general.send("Hello! Created the role ThirstyBois for water reminders.")
            logger.info("Created it")

    @bot.event
    async def on_ready():
        logger.info("Starting the timed alerts")
        while True:
            for guild in bot.guilds:
                logger.info(f"Alerting the thirsty bois in the {guild.name} guild")
                thirsty_bois = []
                role = discord.utils.get(guild.roles, name="ThirstyBois")
                ment = role.mention
                general = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
                await general.send(f"{ment} Time to hydrate that body!!! Get up and stretch if you can as well!")
            logger.info(f"Done. Sleeping for {MINUTES_BETWEEN_ALERTS}")
            await asyncio.sleep(MINUTES_BETWEEN_ALERTS * 60) 
    
    
    bot.run(TOKEN)

if __name__ == "__main__":
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discord.log',encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    startBot()
