import discord
import os
import csv
import json
from discord.ext import commands
from functions import update_data, add_experience, level_up
import random
import asyncio
from datetime import datetime, timedelta

phrases = []
with open("ganduri.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='/')
    for row in csv_reader:
        phrases.append(row[1])


cuvinte_restrictionate = ['c1gan','cig4n''c1g4n','țig4n','ț1g4n','t1g4n','tig4n', 'țig4n', 'cig4n','t1gan','tigan', 'țigan', 'cigan', 'nigg', 'tzigan', 'țzigan', 'nig', 'n1g', 'fut', 'muie', 'muje', 'mu13', 'mui3', 'mu1e']

bot = commands.Bot(command_prefix='$')

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}

@bot.event
async def on_ready():
    print(f"{bot.user} logged in now!")
    await bot.change_presence(activity=discord.Game(name="Barbut e veata mea. Răspund doar celor care aruncă cu $112!"))

@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@bot.event
async def on_message(message):

    if message.author.bot == False:
      
        if any(x in message.content for x in cuvinte_restrictionate):
            await message.delete()
        global author_msg_counts

        author_id = message.author.id
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
            author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
            msg_time for msg_time in author_msg_times[author_id]
            if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
            author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.

        if len(author_msg_times[author_id]) > max_msg_per_window:
            await message.channel.purge(after=datetime.now() - timedelta(seconds=7), check = lambda x: x.author.id == message.author.id, oldest_first=False) #purges the channel
            muted_role = discord.utils.get(message.guild.roles, name='STFU')
            await message.author.add_roles(muted_role)
            await message.channel.send('Taci, be-me-ai bota!')
            await asyncio.sleep(10)
            await message.author.remove_roles(muted_role)
            await message.channel.send('Acum că te-ai săturat, sper că nu mai cerșești de mâncare.')
        with open('users.json', 'r') as f:
            users = json.load(f)

            await update_data(users, message.author)
            await add_experience(users, message.author, 5)
            await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

        await bot.process_commands(message)
    else:
      return

@bot.command(aliases=['112'])
async def ajutor(ctx):
    embed = discord.Embed(title="Comenzi utile pentru a-ți Alina suferința!")
    embed.add_field(name="$alin_hainoroc", value="Lasă-l pe Alin să te salute!")
    embed.add_field(name="$alin_ganduri", value="Lasă-l pe Alin să agațe în locul tău sau invață de la EL!")
    embed.add_field(name="$alin_ghiceste", value="Pierzi la barbut și devin-o sclavul lui Alin!")
    await ctx.send(content=None, embed=embed)

@bot.command()
async def alin_hainoroc(ctx):
    init_msg = str(ctx.author)
    final_msg = init_msg[:-5]
    await ctx.send(f"Hai noroc! Te rog să mă lași să îți Alin suferința, domnule {final_msg}!")

@bot.command()
async def alin_ganduri(ctx):
    response = phrases[random.randint(0, len(phrases) - 1)]
    await ctx.send(response)

@bot.command()
async def alin_ghiceste(ctx):
    await ctx.send('Te provoc să ghicești un număr între 1 și 10. Dacă nu ghicești ești sclavul meu.')

    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()
    
    answer = random.randint(1, 10)

    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.send(f'La cât de încet ești, va trece viața pe lângă tine... Răspunsul corect era {answer}.')

    if int(guess.content) == answer:
        await ctx.send('Mânca-ți-aș, ești mai ceva decât o ghicitoare!')
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, ctx.author)
        await add_experience(users, ctx.author, 75)
        await level_up(users, ctx.author, ctx)

        with open('users.json', 'w') as f:
            json.dump(users, f)
    else:
        await ctx.send(f'Boss-ule, te aștept pe plantație. Răspunsul era {answer}, doar ca să mori de ciudă.')

@bot.command()
async def create_role(ctx, nume: str, permisie: int):
    if ctx.message.author == 'YeLLo#6227':
        guild = ctx.guild
        permissions = discord.Permissions(permissions = permisie)
        await guild.create_role(name=nume, colour=discord.Colour(0xFFC0CB), permissions=permissions)

@bot.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        autor_mesaj = ctx.message.author
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(autor_mesaj)]['level']
        if int(lvl) < 10:
            await ctx.send(f'Du-te la sală, trage de fiare, bagă pastile să te faci mare că abia ai lvl {lvl}!')
        else:
            await ctx.send(f'Ai tu lvl {lvl}, dar dacă te bat o dată nimic nu îţi mai trebuie!')
    else:
        autor_mesaj = member
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(autor_mesaj)]['level']
        await ctx.send(f'Nu e frumos să tragi cu ochiul la alții, dar ia de aici bossule: {member} are level {lvl}!') 
 

my_secret = os.environ['TOKEN']
bot.run(my_secret)