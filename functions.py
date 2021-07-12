async def update_data(users, user):
    if not f'{user}' in users:
        users[f'{user}'] = {}
        users[f'{user}']['experience'] = 0
        users[f'{user}']['level'] = 1


async def add_experience(users, user, exp):
    users[f'{user}']['experience'] += exp


async def level_up(users, user, message):
    experience = users[f'{user}']['experience']
    lvl_start = users[f'{user}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} bravo barosane, ai facut level {lvl_end}! Mergi în muşchi, să fii mândru de tine!')
        users[f'{user}']['level'] = lvl_end