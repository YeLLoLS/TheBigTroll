import os
import discord
import csv
import random
import asyncio

phrases = []
with open("ganduri.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='/')
    for row in csv_reader:
        phrases.append(row[1])


cuvinte_restrictionate = ['tigan', 'țigan', 'cigan', 'nigg', 'tzigan', 'țzigan', 'nig', 'n1g', 'fut', 'muie', 'muje', 'mu13', 'mui3', 'mu1e']

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} logged in now!")


@client.event
async def on_message(message):    
    if message.content == '$112':
      embed = discord.Embed(title="Comenzi utile pentru a-ți Alina suferința!")
      embed.add_field(name="$alin_hainoroc", value="Lasă-l pe Alin să te salute!")
      embed.add_field(name="$alin_ganduri", value="Lasă-l pe Alin să agațe în locul tău sau invață de la EL!")
      embed.add_field(name="$alin_ghiceste", value="Pierzi la barbut și devin-o sclavul lui Alin!")
      await message.channel.send(content=None, embed=embed)

    elif message.content == "$alin_hainoroc":
        init_msg = str(message.author)
        final_msg = init_msg[:-5]
        await message.channel.send(f"Hai noroc! Te rog să mă lași să îți Alin suferința, domnule {final_msg}!")
        
    elif message.content == "$alin_ganduri":
        response = phrases[random.randint(0, len(phrases) - 1)]
        await message.channel.send(response)

    elif any(x in message.content for x in cuvinte_restrictionate):
      await message.delete()
    
    elif message.content == '$alin_ghiceste':
            await message.channel.send('Te provoc să ghicești un număr între 1 și 10. Dacă nu ghicești ești sclavul meu.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await client.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'La cât de încet ești, va trece viața pe lângă tine... Răspunsul corect era {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('Mânca-ți-aș, ești mai ceva decât o ghicitoare!')
            else:
                await message.channel.send(f'Boss-ule, te aștept pe plantație. Răspunsul era {answer}, doar ca să mori de ciudă.')


my_secret = os.environ['TOKEN']
client.run(my_secret)