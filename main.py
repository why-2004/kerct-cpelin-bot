import discord
import re
from eng_to_ipa import jonvert as convert

from discord.ext import commands
from dragonmapper import hanzi

from impostor import send_message_as_user

intents = discord.Intents.default()
intents.members = True

command_prefix = '!'
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command("help")

helptext='''Commands available:

eng2kerct: english to kerct spëliñ
eng2ipa: english to IPA
kerct2ipa: kerct spëliñ to IPA
ipa2kerct: IPA to kerct spëliñ
vowelnt: english to english (without vowels)
chi2ipa: chinese to IPA
help: this'''

kerct = {'m': 'm', 'n': 'n', 'ñ': 'ŋ', 'p': 'p', 't': 't', 'q': 'ʧ', 'k': 'k', 'b': 'b', 'd': 'd', 'j': 'ʤ', 'g': 'g',
         'f': 'f', 'č': 'θ', 'c': 's', 's': 'ʃ', 'h': 'h', 'v': 'v', 'ž': 'ð', 'z': 'z', 'x': 'ʒ', 'l': 'l', 'r': 'r',
         'y': 'j', 'w': 'w', 'a': 'a', 'ä': 'æ', 'e': 'ə', 'ë': 'ɛ', 'ē': 'ɜː', 'o': 'ɒ', 'i': 'ɪ', 'ī': 'iː',
         'u': 'ʊ', 'ū': 'uː', 'ö': 'ˈəʊ'}
ipa = {'m': 'm', 'n': 'n', 'ŋ': 'ñ', 'p': 'p', 't': 't', 'ʧ': 'q', 'k': 'k', 'b': 'b', 'd': 'd', 'ʤ': 'j', 'g': 'g',
       'f': 'f', 'θ': 'č', 's': 'c', 'ʃ': 's', 'h': 'h', 'v': 'v', 'ð': 'ž', 'z': 'z', 'ʒ': 'x', 'l': 'l', 'r': 'r',
       'j': 'y', 'w': 'w', 'a': 'a', 'æ': 'ä', 'ə': 'e', 'ɛ': 'ë', 'ɜ': 'ē', 'ɒ': 'o', 'ɪ': 'i', 'i': 'ī', 'ʊ': 'u',
       'u': 'ū', 'ö': 'ö', 'ː': '', 'ˈ': '', 'ˌ': ''}  # must replace "ˈəʊ" with ö

def ipa_to_kerct(text):
    output = ""
    arg = re.sub("ˈəʊ", 'ö', text)
    for i in arg.split(" "):
        for j in i:
            if j in ipa:
                output += ipa[j]
            else:
                output += j
        output += " "
    return output

@bot.command(name='ipa2kerct')  # ipa to kerct
async def ipa2kerct(ctx, *, arg1=None):
    output = (ipa_to_kerct(arg1))
    await send_message_as_user(ctx.author,output,ctx.message)

def kerct_to_ipa(text):
    output = ""
    for i in text.split(" "):
        for j in i:
            if j in kerct:
                output += kerct[j]
            else:
                output += j
        output += " "
    return output

@bot.command(name='kerct2ipa')  # kerct to ipa
async def kerct2ipa(ctx, *, arg1=None):
    output = (kerct_to_ipa(arg1))
    await send_message_as_user(ctx.author,output,ctx.message)

@bot.command(name='eng2ipa') # english to ipa
async def eng2ipa(ctx, *, arg1=None):
    output = (convert(arg1))
    await send_message_as_user(ctx.author,output,ctx.message)

@bot.command(name='eng2kerct') # english to kerct
async def eng2kerct(ctx, *, arg1=None):
    output = ipa_to_kerct(convert(arg1))
    await send_message_as_user(ctx.author, output, ctx.message)

@bot.command(name='vowelnt')  # english to vowelnt
async def vowelnt(ctx, *, arg1=None):
    output = ""
    for i in arg1.split(" "):
        for j in i:
            if not re.match('[aeiouAEIOU]', j):
                output += j
        output += " "
    await send_message_as_user(ctx.author,output,ctx.message)

@bot.command(name="help")
async def help(ctx):
    await ctx.send(helptext)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('pong')

@bot.command(name="chi2ipa")
async def chi2ipa(ctx, *, arg1=None):
    output=hanzi.to_ipa(arg1)
    await send_message_as_user(ctx.author,output,ctx.message)

@bot.command(name="chi2zhu")
async def chi2zhu(ctx, *, arg1=None):
    output=hanzi.to_zhuyin(arg1)
    await send_message_as_user(ctx.author,output,ctx.message)

@bot.command(name="webhooktest")
async def webhooktest(ctx):
    await send_message_as_user(ctx.author,"Hello World!",ctx.message)

bot.run(open("api.key","r").read())
