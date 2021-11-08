import ast

import messages
from messages import send_message

webhooks = False
delete_og_message = False
command_prefix = '!'


def update_settings_from_file():
    global webhooks, delete_og_message, command_prefix
    try:
        with open('settings.kerst', 'r') as f:
            setdict = ast.literal_eval(f.read())
        webhooks = setdict['webhooks']
        delete_og_message = setdict['delete']
        command_prefix = setdict['prefix']
        messages.delete_og_message = delete_og_message
        messages.webhooks = webhooks
    except:
        update_settings_to_file()


def update_settings_to_file():
    setdict = {'webhooks': webhooks, 'delete': delete_og_message, 'prefix': command_prefix}
    with open('settings.kerst', 'w') as f: f.write(repr(setdict))
    messages.delete_og_message = delete_og_message
    messages.webhooks = webhooks


def webhooks_set(setting=None):
    global webhooks
    if setting is None:
        webhooks = not webhooks
        output = "Webhooks are now " + ("on" if webhooks else "off")
    elif setting:
        webhooks = True
        output = "Webhooks are now on"
    else:
        webhooks = False
        output = "Webhooks are now off"
    update_settings_to_file()
    return output


def delete_set(setting=None):
    global delete_og_message
    if setting is None:
        delete_og_message = not delete_og_message
        output = "Old message is now " + ("deleted" if delete_og_message else "not deleted")
    elif setting:
        delete_og_message = True
        output = "Old message is now deleted"
    else:
        delete_og_message = False
        output = "Old message is now not deleted"
    update_settings_to_file()
    return output


def prefix_set(setting=None):
    global command_prefix
    if setting:
        command_prefix = setting
        update_settings_to_file()
        return "Prefix changed to " + command_prefix
    return "Prefix is " + command_prefix
