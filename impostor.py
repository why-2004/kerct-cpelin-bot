# when the impostor is sus!
import discord


async def send_message_as_user(user, text, message):
    webhook = await message.channel.create_webhook(name="sus")# TODO: actually use 1 webhook per channel
    await print(user.avatar_url)
    #webhook = discord.Webhook.partial(123, None, adapter=discord.RequestsWebhookAdapter())
    await message.delete()
    await webhook.send(content=text, username=user.name, avatar_url=user.avatar_url)

async def send_message_as_name(name, text, message, picture):
    webhook = await message.channel.create_webhook(name="sus")
    #webhook = discord.Webhook.partial(123, None, adapter=discord.RequestsWebhookAdapter())
    await message.delete()
    await webhook.send(content=text, username=name, avatar_url=picture)