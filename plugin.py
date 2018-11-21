from slackbot.bot import respond_to, listen_to

from models import Memo


@respond_to(r'parrot\s+(.+)')
def parrot(message, word):
    message.reply(word)


@listen_to(r'HAHAHA')
def what_is_funny(message):
    message.send('What is funny?')


@respond_to(r'memo\s+save\s+(\S+)\s+(\S.*)')
def memo_save(message, name, text):
    memo, created = Memo.get_or_create(name=name, text=text)
    memo.save()
    message.reply(f'I remembered a memo "{name}"')


@respond_to(r'memo\s+show\s+(\S+)')
def memo_show(message, name):
    memo = Memo.get_or_none(name=name)
    if memo:
        message.reply(f'memo "{name}" is below\n```\n{memo.text}\n```\n')
    else:
        message.reply(f'memo "{name}" ... hmm ..., I don\'t know ¯\\_(ツ)_/¯')
