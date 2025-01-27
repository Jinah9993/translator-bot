import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai.api_key = OPENAI_API_KEY


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    
    if message.author.bot:
        return

    
    if message.content.startswith("."):
        
        user_message = message.content[1:].strip()

        try:
            
            if all("\uac00" <= char <= "\ud7a3" or "\u3130" <= char <= "\u318F" for char in user_message if char.strip()):
                direction = "to English"  
            else:
                direction = "to Korean"  

            prompt = f"Translate the following text {direction}: '{user_message}'"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # gpt-4
                messages=[
                    {"role": "system", "content": "You are a helpful translator."},
                    {"role": "user", "content": prompt},
                ],
            )
            translated_text = response["choices"][0]["message"]["content"].strip()

            
            embed = discord.Embed(
                #title="Translation: ",
                description=f"**{message.author.display_name} said:** {user_message}\n\n**Translated:** {translated_text}",
                color=discord.Color.blue()
            )
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
            )

            
            await message.channel.send(embed=embed)

            
            await message.delete()

        except Exception as e:
            print(f"Error: {e}")
            await message.channel.send("Sorry, something went wrong with the translation.")


bot.run(DISCORD_TOKEN)
