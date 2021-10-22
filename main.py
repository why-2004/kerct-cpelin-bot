import discord
import re

from discord.ext import commands

import settings
from converters import *

from messages import *

from settings import webhooks_set
from settings import delete_set
from settings import prefix_set

intents = discord.Intents.default()
intents.members = True

settings.update_settings_from_file()
command_prefix = settings.command_prefix

bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command("help")

helptext = '''Commands available:

eng2kerct: english to kerct spëliñ
eng2ipa: english to IPA
kerct2ipa: kerct spëliñ to IPA
ipa2kerct: IPA to kerct spëliñ
vowelnt: english to english (without vowels)
chi2ipa: chinese to IPA
help: this
webhooks: change whether the bot uses webhooks
delete: change whether the bot deletes the original message
prefix: change prefix'''

trueregex = "(True)|(T)|(t)|(true)|(on)|(enable)|(On)|(Enable)|(1)"
falseregex = "(False)|(F)|(f)|(false)|(off)|(disable)|(off)|(Disable)|(0)"


@bot.command(name='ipa2kerct')  # ipa to kerct
async def ipa2kerct(ctx, *, arg1=""):
    output = (ipa_to_kerct(arg1))
    await send_message(ctx, output, arg1)


@bot.command(name='kerct2ipa')  # kerct to ipa
async def kerct2ipa(ctx, *, arg1=""):
    output = (kerct_to_ipa(arg1))
    await send_message(ctx, output, arg1)


@bot.command(name='eng2ipa')  # english to ipa
async def eng2ipa(ctx, *, arg1=""):
    output = (eng_to_ipa(arg1))
    await send_message(ctx, output, arg1)


@bot.command(name='eng2kerct')  # english to kerct
async def eng2kerct(ctx, *, arg1=""):
    output = eng_to_kerct(arg1)
    await send_message(ctx, output, arg1)


@bot.command(name='vowelnt')  # english to vowelnt
async def vowelnt(ctx, *, arg1=""):
    output = remove_vowels(arg1)
    await send_message(ctx, output, arg1)


@bot.command(name="help")
async def help(ctx):
    await ctx.send(helptext)
    await ctx.send("The current prefix is " + command_prefix)


@bot.command(name="hëlp")
async def kercthelp(ctx):
    print("hëlp")
    output = ""
    for i in helptext.split("\n"):
        output += eng_to_kerct(i)
        output += "\n"
    await ctx.send(output[:-1])


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('pong')


@bot.command(name="chi2ipa")
async def chi2ipa(ctx, *, arg1=""):
    output = han_to_ipa(arg1)
    await send_message(ctx, output, arg1)


@bot.command(name="chi2zhu")
async def chi2zhu(ctx, *, arg1=""):
    output = han_to_zhu(arg1)
    await send_message(ctx, output, arg1)


@bot.command(name="chi2pin")
async def chi2pin(ctx, *, arg1=""):
    output = han_to_pin(arg1)
    await send_message(ctx, output, arg1)


@bot.command(name="webhooks")
async def webhooks_setting(ctx, *, arg1=""):
    if re.match(trueregex, arg1):
        o = webhooks_set(True)
    elif re.match(falseregex, arg1):
        o = webhooks_set(False)
    else:
        o = webhooks_set(None)
    await ctx.send(o)


@bot.command(name="delete")
async def delete_setting(ctx, *, arg1=""):
    if re.match(trueregex, arg1):
        o = delete_set(True)
    elif re.match(falseregex, arg1):
        o = delete_set(False)
    else:
        o = delete_set(None)
    await ctx.send(o)


@bot.command(name="prefix")
async def prefix(ctx, *, arg1=""):
    if arg1 == "":
        o = prefix_set()
    else:
        o = prefix_set(arg1)
        bot.command_prefix = arg1
        command_prefix = arg1
    await ctx.send(o)


bot.run(open("api.key", "r").read())
