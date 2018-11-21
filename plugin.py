from slackbot.bot import respond_to, listen_to


@respond_to(r'parrot\s+(.+)')
def parrot(message, word):
    message.reply(word)


@listen_to(r'HAHAHA')
def what_is_funny(message):
    message.send('What is funny?')
