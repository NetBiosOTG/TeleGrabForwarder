import os

# Your Telegram API credentials
API_ID = '21637014'
API_HASH = '410955dedb8c4b1628eb41df366762c6'

# Session string instead of phone number
# To generate a session string, run the session_generator.py script first
TELEGRAM_SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING', '')

# Legacy phone number (kept for session generation only)
PHONE_NUMBER = '+18126979150'

SOURCE_TO_TOPIC_MAPPING = {
    # MetaWin.com MAIN TG: Messages from "MetaWin.com MAIN TG" source channel
    -1001892037773: {   # MetaWin.com MAIN TG source channel ID
        -1002756711574: 325,     # Bonus Codes (Topic ID)
    },

    # Shuffle.com - Bonus Code VIP: Messages from "Shuffle.com - Bonus Code VIP" source channel
    -1002185512641: {   # Shuffle.com - Bonus Code VIP source channel ID
        -1002756711574: 8,      # Bonus Codes (Topic ID)
    },

    # Winna.com - Winna Casino: Messages from "Winna.com - Winna Casino" source channel
    -1002472636693: {   # Winna.com - Winna Casino source channel ID
        -1002756711574: 34,     # Bonus Codes (Topic ID)
    },

    # ₿C Token Lounge: Messages from "₿C Token Lounge" source channel
    -1002249193735: {   # ₿C Token Lounge source channel ID
        -1002756711574: 52,     # Bonus Codes (Topic ID)
    },

    # Goated Drops: Messages from "Goated Drops" source channel
    -1002234305882: {   # Goated Drops source channel ID
        -1002756711574: 26,     # Bonus Codes (Topic ID)
    },

    # Stake.US Daily Drops 🇺🇸: Messages from "Stake.US Daily Drops 🇺🇸" source channel
    -1002133338932: {   # Stake.US Daily Drops 🇺🇸 source channel ID
        -1002756711574: 16,     # Bonus Codes (Topic ID)
    },

    # BC.Game 🔔 Notifications: Messages from "BC.Game 🔔 Notifications" source channel
    -1001166926064: {   # BC.Game 🔔 Notifications source channel ID
        -1002756711574: 6,      # Bonus Codes (Topic ID)
    },

    # Shuffle.com: Messages from "Shuffle.com" source channel
    -1001517758091: {   # Shuffle.com source channel ID
        -1002756711574: 10,     # Bonus Codes (Topic ID)
    },

    # Razed - Community: Messages from "Razed - Community" source channel
    -1002061136110: {   # Razed - Community source channel ID
        -1002756711574: 30,     # Bonus Codes (Topic ID)
    },

    # Shuffle Sports: Messages from "Shuffle Sports" source channel
    -1002109995475: {   # Shuffle Sports source channel ID
        -1002756711574: 12,     # Bonus Codes (Topic ID)
    },

    # Goated.com: Messages from "Goated.com" source channel
    -1002434383104: {   # Goated.com source channel ID
        -1002756711574: 28,     # Bonus Codes (Topic ID)
    },

    # Stake.com - Play Smarter: Messages from "Stake.com - Play Smarter" source channel
    -1001356950325: {   # Stake.com - Play Smarter source channel ID
        -1002756711574: 18,     # Bonus Codes (Topic ID)
    },

    # Roobet: Messages from "Roobet" source channel
    -1001278995047: {   # Roobet source channel ID
        -1002756711574: 38,     # Bonus Codes (Topic ID)
    },

    # Shuffle JP ブースト: Messages from "Shuffle JP ブースト" source channel
    -1002060359531: {   # Shuffle JP ブースト source channel ID
        -1002756711574: 14,     # Bonus Codes (Topic ID)
    },

    # Stake.us - Play Smarter: Messages from "Stake.us - Play Smarter" source channel
    -1001751288924: {   # Stake.us - Play Smarter source channel ID
        -1002756711574: 20,     # Bonus Codes (Topic ID)
    },

    # Gamba.com: Messages from "Gamba.com" source channel
    -1002121217568: {   # Gamba.com source channel ID
        -1002756711574: 40,     # Bonus Codes (Topic ID)
    },

    # Luckybird.io - Play Smarter: Messages from "Luckybird.io - Play Smarter" source channel
    -1001703288746: {   # Luckybird.io - Play Smarter source channel ID
        -1002756711574: 44,     # Bonus Codes (Topic ID)
    },

    # Stake.us - VIP Notices: Messages from "Stake.us - VIP Notices" source channel
    -1001542279201: {   # Stake.us - VIP Notices source channel ID
        -1002756711574: 22,     # Bonus Codes (Topic ID)
    },

    # Razed Sports: Messages from "Razed Sports" source channel
    -1002379667487: {   # Razed Sports source channel ID
        -1002756711574: 42,     # Bonus Codes (Topic ID)
    },

    # Sicodice Official Channel: Messages from "Sicodice Official Channel" source channel
    -1001677525545: {   # Sicodice Official Channel source channel ID
        -1002756711574: 46,     # Bonus Codes (Topic ID)
    },

    # High Rollers - Stake.US - (Unofficial): Messages from "High Rollers - Stake.US - (Unofficial)" source channel
    -1002102309936: {   # High Rollers - Stake.US - (Unofficial) source channel ID
        -1002756711574: 24,     # Bonus Codes (Topic ID)
    }, 

    # RainsTEAM: Messages from "RainsTEAM" source channel
    -1001738096535: {   # RainsTEAM source channel ID
        -1002756711574: 153,    # Bonus Codes (Topic ID)
    },

    # EmpireDrop: Messages from "EmpireDrop" source channel
    -1002069575599: {   # EmpireDrop source channel ID
        -1002756711574: 277,    # Bonus Codes (Topic ID)
    }
}

# Legacy configuration (kept for backwards compatibility, but not used in new version)
SOURCE_CHATS = list(SOURCE_TO_TOPIC_MAPPING.keys())
TARGET_CHATS = {}
for source_mappings in SOURCE_TO_TOPIC_MAPPING.values():
    for target_group_id, topic_id in source_mappings.items():
        TARGET_CHATS[target_group_id] = topic_id
