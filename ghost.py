import discord, os, keep_alive

client = discord.Client()

EVIDENCE = {
    'emf': 'EMF Level 5',
    'sb': 'Spirit Box',
    'ft': 'Freezing Temps',
    'fp': 'Fingerprints',
    'go': 'Ghost Orb',
    'gw': 'Ghost Writing'
}

GHOSTS = {
    'Spirit': ['• Smudge Dicks stop it from hunting'],
    'Wraith': ['• No footprints with UV', '• No likey the Salt (*gimme some sugar*)'],
    'Phantom': ['• Sanity drops by a lot if you look at it (*cuz it be ugly*)', '• Disappears if you take a photo (*cuz it be ugly*)'],
    'Poltergeist': ['• Throws a lotta shit around (*Kobe!*)', '• Can\'t do nuthin in an empty room'],
    'Banshee': ['• Targets only 1 homie at a time (*one of us ain\'t gon\' be a virgin no more*)', '• Less aggressive near a Crucifix'],
    'Jinn': ['• Travels fast if a homie is far away', '• Turning off power prevents it from going zoom zoom'],
    'Mare': ['• Increased chance to attack in the dark (*late night ghost emoji*)', '• Less chance to attack if light on (*clap on*)'],
    'Revenant': ['• Can\'t be outrun', '• Hiding from it makes it slow (*don\'t come outta the closet yet*)'],
    'Shade': ['• Hard to find', '• Won\'t hunt if too many homies (*no gangbangs today*)'],
    'Demon': ['• Aggressive motherfucker (hunts a lot)', '• Ouija Board doesn\'t lower sanity'],
    'Yurei': ['• Stronger effect on sanity', '• Smudging the room stops it from wandering'],
    'Oni': ['• More active if more homies (*party!*)']
}

GHOSTDATA = {
    ('sb', 'fp', 'gw'): 'Spirit',
    ('fp', 'ft', 'sb'): 'Wraith',
    ('emf', 'go', 'ft'): 'Phantom',
    ('sb', 'fp', 'go'): 'Poltergeist',
    ('emf', 'fp', 'ft'): 'Banshee',
    ('sb', 'go', 'emf'): 'Jinn',
    ('sb', 'go', 'ft'): 'Mare',
    ('emf', 'fp', 'gw'): 'Revenant',
    ('emf', 'go', 'gw'): 'Shade',
    ('sb', 'gw', 'ft'): 'Demon',
    ('go', 'gw', 'ft'): 'Yurei',
    ('emf', 'sb', 'gw'): 'Oni'
}

messages_to_delete = [];

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Game(name='Type `help for help'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('`help') or message.content == '`help':
        await message.channel.send(embed=displayHelp())

    elif message.content.startswith('`'):
        messages_to_delete.append(message)
        if message.content == '`':
            m = await message.channel.send(prettyPrint(GHOSTDATA))
            messages_to_delete.append(m)
            return
        if message.content == '`reset':
            for message in messages_to_delete:
                try:
                  await message.delete()
                except:
                  continue
            messages_to_delete.clear()
            return
        userInput = message.content[1:].lower().split(' ')
        if len(userInput) > 3:
            await message.channel.send('Too much evidence dummy')
            return
        possibilities = GHOSTDATA.copy()
        for evidence in userInput:
            if evidence not in EVIDENCE:
                m = await message.channel.send(f'{evidence} is not valid evidence dummy')
                messages_to_delete.append(m)
                return
            else:
                for ghostEvidence in possibilities.copy():
                    if evidence not in ghostEvidence:
                        del possibilities[ghostEvidence]
                for ghostEvidence in possibilities.copy():
                    remainingEvidence = getRemainingEvidence(evidence, ghostEvidence)
                    possibilities[remainingEvidence] = possibilities.pop(ghostEvidence)
                    
        m = await message.channel.send(embed=prettyPrintEmbedded(possibilities))
        messages_to_delete.append(m)

def displayHelp():
    text = '''Commands start with a backtick (\`), the key to the left of the 1.
    Separate evidence with a space.
    \`emf
    \`go gw
    \`sb gw ft
    \` (to see all ghosts)
    \`reset to delete all bot-related messages
    '''
    embed = discord.Embed(title='For Dummies', color = 0x00ff00)
    embed.add_field(name='To hunt ghosts professionally like Big Tasty', value=text, inline=False)
    return embed

def getRemainingEvidence(evidence, ghostEvidence):
    return tuple(x for x in ghostEvidence if x != evidence)

def prettyPrintEmbedded(possibilities):
    embed = discord.Embed(title='Results from Professional Ghost Hunter Big Tasty', color = 0x0000ff)
    if len(possibilities) == 0:
        s = 'You messed up. Or there\'s a bug. But most likely the first one.'
        embed.add_field(name='No results', value=s, inline=False)
        return embed
    else:
        s = ''
    for ghostEvidence in possibilities:
        s += '__**'
        for ghostEvidenceAbbr in ghostEvidence:
            s += EVIDENCE[ghostEvidenceAbbr] + ', '
        s += '-> ' + possibilities[ghostEvidence] + '**__\n'
        s += '\n'.join(GHOSTS[possibilities[ghostEvidence]])
        s += '\n'
    embed.add_field(name='Possibilities', value=s, inline=False)
    return embed

def prettyPrint(possibilities):
    s = ''
    for ghostEvidence in possibilities:
        s += '__**'
        for ghostEvidenceAbbr in ghostEvidence:
            s += EVIDENCE[ghostEvidenceAbbr] + ', '
        s += '-> ' + possibilities[ghostEvidence] + '**__\n'
        s += '\n'.join(GHOSTS[possibilities[ghostEvidence]])
        s += '\n'
    return s

keep_alive.keep_alive()

client.run(os.getenv('CLIENT_TOKEN'))
