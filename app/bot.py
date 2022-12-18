import discord
from discord.ext import commands
from discord.ui import Button, View
from secretToken import discordToken
from scrape import getEnrollInfo, getYear, checkSpace
import asyncio

bot=commands.Bot(command_prefix='!', intents=discord.Intents.all())

year = getYear()
flag = True

@bot.event
async def on_ready():
    print('Connecting ')
    print(f"Connecting to {bot.user.name} BOT")
    print('Connection Success')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.event
async def on_message(message):
    if message.content.startswith('!help'):
        await message.channel.send(f"Commands:\n```!help: List of commands\n!add: Add class code to queue\n!delete: Remove class code from queue\n!queue: Show class codes in queue\n!clear_all: Clear all classes in queue\n!watch: Monitor classes in queue```")
    if message.content.startswith('!add'):
        class_code = message.content[5:]
        if class_code.isdigit() and len(class_code) == 5:
            opened_file = open("classes.txt", "a")
            opened_file.write(f"{class_code}\n")
            opened_file.close()
            await message.channel.send(f"Succesfully added {message.content[5:]} to queue")
        else:
            await message.channel.send(f"Invalid Course Code")
    if message.content.startswith('!delete'):
        class_code = f"{message.content[8:]}\n"
        opened_file = open("classes.txt", "r")
        codes = opened_file.readlines()
        opened_file.close()
        if class_code in codes:
            codes.remove(class_code)
            await message.channel.send(f"Succesfully removed {class_code} from queue")
            opened_to_write = open("classes.txt", "w")
            for i in codes:
                opened_to_write.write(i)
            opened_to_write.close()
        else:
            await message.channel.send(f"The class code is not in queue")

    if message.content.startswith('!queue'):
        opened_file = open("classes.txt", "r")
        codes = opened_file.readlines()
        await message.channel.send(f"Class codes in queue:")
        for i in codes:
            await message.channel.send(f"{i}")
        opened_file.close()
    
    if message.content.startswith('!clear_all'):
        opened_to_write = open("classes.txt", "w")
        opened_to_write.write()
        opened_to_write.close()
        await message.channel.send(f"Queue has been cleared")

    if message.content.startswith('!watch'):
        opened_file = open("classes.txt", "r")
        codes = opened_file.readlines()
        opened_file.close()
        await message.channel.send(f"Watching initiated for following classes:")
        for i in codes:
            await message.channel.send(f"{i}")
        global flag
        button1 = Button(label="Stop Watching", style= discord.ButtonStyle.blurple, custom_id="1")
        async def button_action(interaction):
            message.content = "!stop"
            await interaction.response.defer()
        button1.callback = button_action
        view = View()
        view.add_item(button1)
        await message.channel.send(view=view)
        while flag:
            if message.content.startswith('!stop'):
                await message.channel.send(f"Force stopping watch")
                flag = False
            for i in codes:
                code = i.strip("\n")
                x = getEnrollInfo(year, code)
                spot = checkSpace(x)
                if spot:
                    await message.channel.send(f"Spot found for class code {code}. Stopping watch")
                    flag = False
            await asyncio.sleep(5)

if __name__ == "__main__":
    bot.run(discordToken)