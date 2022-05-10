from pymongo import MongoClient
import os
import logging

"""
Environment Variables
"""
TOKEN = os.getenv("TOKEN")
RANDOMMER_API = os.getenv("RANDOMMER_API")
MONGODB = os.getenv("MONGODB")

"""
Logging setup.
"""
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w'
)

handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)



"""
MongoDB 
"""
Client = MongoClient(MONGODB)

def warn_count(idict: dict, id: int):
    try:
        count = 0
        print(idict)
        for i in idict[id]:
            count += 1
        return(count)
    except KeyError:
        return(0)


permission_dict = {
    "create_instant_invite": "Create Instant Invite",
    "kick_members": "Kick Members",
    "ban_members": "Ban Members",
    "administrator": "Administrator",
    "manage_channels": "Manage Channels",
    "manage_guild": "Manage Guild",
    "add_reactions": "Add Reactions",
    "view_audit_log": "View Audit Log",
    "priority_speaker": "Priority Speaker",
    "stream": "Stream",
    "view_channel": "View Channel",
    "send_messages": "Send Messages",
    "send_tts_messages": "Send TTS Messages",
    "manage_messages": "Manage Messages",
    "embed_links": "Embed Links",
    "attach_files": "Attach Files",
    "read_message_history": "Read Message History",
    "mention_everyone": "Mention EVERYONE",
    "use_external_emojis": "Use External Emojis",
    "view_guild_insights": "View Guild Insights",
    "connect": "Connect",
    "speak": "Speak",
    "mute_members": "Mute Members",
    "deafen_members": "Deafen Members",
    "move_members": "Move Members",
    "use_vad": "Use Voice-Activity-Detection",
    "change_nickname": "Change Nickname",
    "manage_nicknames": "Manage Nicknames",
    "manage_roles": "Manage Roles",
    "manage_webhooks": "Manage Webhooks",
    "manage_emojis_and_stickers": "Manage Emojis and Stickers",
    "use_application_commands": "Manage Application Commands",
    "request_to_speak": "Request to Speak",
    "manage_events": "Manage Events",
    "manage_threads": "Manage Threads",
    "create_public_threads": "Create Public Threads",
    "create_public_threads": "Create Private Threads",
    "use_external_stickers": "Use External Stickers",
    "send_messages_in_threads": "Send Messages in Threads",
    "use_embedded_activities": "Use Embedded Activities",
    "moderate_members": "Moderate Members"
    }


def parse_permissions_human(
    permission_list: list
    ):
    new_permission_list = []
    for permission in permission_list:
        permission = str(permission)
        new_permission_list.append(permission_dict[permission])
    return(new_permission_list)


def main():
    pass

if __name__ == "__main__":
    main()
