import discord, asyncio, datetime
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_components import DiscordComponents, Button, ButtonStyle
from flask import Flask
from threading import Thread
import config

app = Flask('')

@app.route('/')
def home():
    return "Hello! Your bot is now online! Head over to <a href='https://uptimerobot.com'>https://uptimerobot.com</a> and create a monitor to make this bot online 24/7. For the minitor url, use the URL of this small window of replit (NOT YOUR BROWSER WINDOW)."

def run():
  app.run(host='0.0.0.0',port=8080)

def keepOnline():
    t = Thread(target=run)
    t.start()

def init(prefix, desc, status):
  bot = commands.Bot(
    command_prefix=prefix,
    description=desc,
    intents=discord.Intents.all(),
    help_command=None
  )
  DiscordComponents(bot)
  @bot.event
  async def on_ready():
      await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.playing, name=status))
      print(f'Logged in as {bot.user}')
  return bot



async def button_click(bot, interaction, TICKET_LOG, CATEGORY_ID, secs):
  if interaction.component.custom_id == "yes": 
    
    embed = discord.Embed(title="Closing Ticket...", description=f"Ticket will be closed in {secs} seconds", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.message.delete()
    msg = await interaction.channel.send(embed=embed)
    await asyncio.sleep(secs)

    user = interaction.guild.get_member(int(interaction.channel.topic))
    log = bot.get_channel(TICKET_LOG)
    embed = discord.Embed(title="Ticket closed", description=f"Ticket created by {user.mention} is closed by {interaction.user.mention}", color=0xE44D41)
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"User ID: {user.id}")
    await log.send(embed=embed)

    embed = discord.Embed(title="Ticket closed", description=f"Your ticket is now closed.", color=0xE44D41)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"You can always create a new ticket by clicking the button below.")
    await user.send(embed=embed, components=[[Button(style=ButtonStyle.grey, label="📩 Create Ticket", custom_id="createTicket")]])

    await interaction.channel.edit(topic=f"**Closed Ticket** ({interaction.user.id})")
    await interaction.channel.set_permissions(interaction.user, send_messages=False, read_messages=False, attach_files=False)
    await msg.delete()
    
    embed = discord.Embed(title="", description="Ticket is closed and no longer visible to the member.", color=0xE44D41)
    await interaction.channel.send(embed=embed)

    embed = discord.Embed(title="", description="```STAFF CONTROLS PANEL```", color=0xE44D41)
    await interaction.channel.send(embed=embed, components=[[Button(style=ButtonStyle.grey, label="✉️ Delete Ticket", custom_id="deleteTicket")]])

  if interaction.component.custom_id == "no": 
    embed = discord.Embed(title="Action Cancelled", description=f"Alright {interaction.user.mention}! I will not close the ticket!", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    msg = await interaction.channel.send(embed=embed)
    await interaction.message.delete()
    await asyncio.sleep(5)
    await msg.delete()

  if interaction.component.custom_id == "deleteTicket":
    embed = discord.Embed(title="Deleting Ticket...", description=f"Ticket will be deleted in {secs} seconds", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.message.delete()
    await interaction.channel.send(embed=embed)
    await asyncio.sleep(secs)
    await interaction.channel.delete()
    
  if interaction.component.custom_id == "closeTicket": 
    embed = discord.Embed(title="Are you sure about that?", description="This action is irreversible!", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.channel.send(embed=embed, components=[[Button(
            style=ButtonStyle.green,
            label="Yes",
            custom_id="yes"
        ),Button(
            style=ButtonStyle.red,
            label="No",
            custom_id="no"
        )]])
    await interaction.respond()

  if interaction.component.custom_id == "createTicket":
    guild = interaction.guild
    category = bot.get_channel(CATEGORY_ID)

    for channel in category.channels:
      if str(channel.topic) == str(interaction.user.id):
        await interaction.respond(content=f"You already had your ticket here at <#{channel.id}>.")
        raise Exception()

    chn = await guild.create_text_channel(f"{interaction.user.name}#{interaction.user.discriminator}", category=category)
    await chn.edit(topic=interaction.user.id)
    await chn.set_permissions(interaction.user, send_messages=True, read_messages=True, attach_files=True)
    log = bot.get_channel(TICKET_LOG)
    embed = discord.Embed(title="Ticket created", description=f"**{interaction.user.mention} created a new ticket!**", color=discord.Colour.green())
    embed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}", icon_url=interaction.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"User ID: {interaction.user.id}")
    await log.send(embed=embed, components=[[Button(
              style=ButtonStyle.URL,
              label="View ticket",
              url=f"https://discord.com/channels/{guild.id}/{chn.id}"
          )]])

    member = guild.get_member(int(interaction.user.id))
    roles = member.roles
    roles.reverse()

    embed = discord.Embed(title="New Ticket", description=f"Type your message here in this channel!", color=discord.Colour.gold())
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.add_field(name="User Mention", value=f"{interaction.user.mention}", inline=True)
    embed.add_field(name="User ID", value=f"{interaction.user.id}", inline=True)
    embed.add_field(name="Highest Role", value=f"{roles[0].mention}", inline=True)
    await chn.send(f"**{interaction.user.mention}, welcome!**", embed=embed, components=[[Button(
        style=ButtonStyle.grey,
        label="🔒 Close Ticket",
        custom_id="closeTicket"
    )]])
    
    await interaction.respond(content=f"Ticket created at <#{chn.id}>")

async def DM(ctx):

  embed = discord.Embed(title=config.TITLE,description=config.MSG,colour=0x2dc6f9)
  embed.set_footer(icon_url=ctx.guild.icon_url, text=f"{ctx.guild.name} • #{ctx.channel.name}")
  embed.set_thumbnail(url=ctx.guild.icon_url)
  await ctx.author.send(embed=embed, components=[[Button(style=ButtonStyle.grey, label="📩 Create Ticket", custom_id="createTicket")]])
  await ctx.message.delete()
  msg = await ctx.send(f"📩 {ctx.message.author.mention}, **check your DMs!**")
  await asyncio.sleep(7)
  await msg.delete()

async def closeTicket(bot, ctx):
  embed = discord.Embed(title="Are you sure about that?", description="This action is irreversible!", color=0xFF0000)
  embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=embed, components=[[Button(
          style=ButtonStyle.green,
          label="Yes",
          custom_id="yes"
      ),Button(
          style=ButtonStyle.red,
          label="No",
          custom_id="no"
      )]])

async def Embed(bot, ctx):
  embed = discord.Embed(title=config.TITLE,description=config.MSG,colour=0x2dc6f9)
  embed.set_footer(icon_url=ctx.guild.icon_url, text=f"{ctx.guild.name} • #{ctx.channel.name}")
  embed.set_thumbnail(url=ctx.guild.icon_url)
  await ctx.send(embed=embed, components=[[Button(style=ButtonStyle.grey, label="📩 Create Ticket", custom_id="createTicket")]])
  await ctx.message.delete()