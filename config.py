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
    # BOOST by Metawin: Messages from "BOOST by Metawin" source channel
    -1002079157553: {   # BOOST by Metawin source channel ID
        -1002756711574: 325,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Shuffle.com - Bonus Code VIP: Messages from "Shuffle.com - Bonus Code VIP" source channel
    -1002185512641: {   # Shuffle.com - Bonus Code VIP source channel ID
        -1002756711574: 8,      # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Winna.com - Winna Casino: Messages from "Winna.com - Winna Casino" source channel
    -1002472636693: {   # Winna.com - Winna Casino source channel ID
        -1002756711574: 34,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # ₿C Token Lounge: Messages from "₿C Token Lounge" source channel
    -1002249193735: {   # ₿C Token Lounge source channel ID
        -1002756711574: 52,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Goated Drops: Messages from "Goated Drops" source channel
    -1002234305882: {   # Goated Drops source channel ID
        -1002756711574: 26,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Stake.US Daily Drops & HighRoller: Messages from "Stake.US Daily Drops 🇺🇸" source channel
    -1002343155225: {   # Stake.US Daily Drops 🇺🇸 source channel ID
        -1002756711574: 16,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # BC.Game 🔔 Notifications: Messages from "BC.Game 🔔 Notifications" source channel
    -1001166926064: {   # BC.Game 🔔 Notifications source channel ID
        -1002756711574: 6,      # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Shuffle.com: Messages from "Shuffle.com" source channel
    -1001517758091: {   # Shuffle.com source channel ID
        -1002756711574: 10,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Razed - Community: Messages from "Razed - Community" source channel
    -1002061136110: {   # Razed - Community source channel ID
        -1002756711574: 30,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Shuffle Sports: Messages from "Shuffle Sports" source channel
    -1002109995475: {   # Shuffle Sports source channel ID
        -1002756711574: 12,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Goated.com: Messages from "Goated.com" source channel
    -1002434383104: {   # Goated.com source channel ID
        -1002756711574: 28,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Stake.com - Play Smarter: Messages from "Stake.com - Play Smarter" source channel
    -1001356950325: {   # Stake.com - Play Smarter source channel ID
        -1002756711574: 18,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Roobet: Messages from "Roobet" source channel
    -1001278995047: {   # Roobet source channel ID
        -1002756711574: 38,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Shuffle JP ブースト: Messages from "Shuffle JP ブースト" source channel
    -1002060359531: {   # Shuffle JP ブースト source channel ID
        -1002756711574: 14,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Stake.us - Play Smarter: Messages from "Stake.us - Play Smarter" source channel
    -1001751288924: {   # Stake.us - Play Smarter source channel ID
        -1002756711574: 20,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Gamba.com: Messages from "Gamba.com" source channel
    -1002121217568: {   # Gamba.com source channel ID
        -1002756711574: 40,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Luckybird.io - Play Smarter: Messages from "Luckybird.io - Play Smarter" source channel
    -1001703288746: {   # Luckybird.io - Play Smarter source channel ID
        -1002756711574: 44,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Stake.us - VIP Notices: Messages from "Stake.us - VIP Notices" source channel
    -1001542279201: {   # Stake.us - VIP Notices source channel ID
        -1002756711574: 22,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Razed Sports: Messages from "Razed Sports" source channel
    -1002379667487: {   # Razed Sports source channel ID
        -1002756711574: 42,     # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # Sicodice Official Channel: Messages from "Sicodice Official Channel" source channel
    -1001677525545: {   # Sicodice Official Channel source channel ID
        -1002756711574: 46,     # Bonus Codes (Topic ID)
    }, 

    # Bonus Codes - Stake.com: Messages from "Bonus Codes - Stake.com" source channel
   -1002239669640: {   # Bonus Codes - Stake.com source channel ID
        -1002756711574: 153,    # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    },

    # EmpireDrop: Messages from "EmpireDrop" source channel
    -1002069575599: {   # EmpireDrop source channel ID
        -1002756711574: 277,    # Bonus Codes (Topic ID)
        -1002210132078: None,  # Hotamajess's Playground (No topics)
    }
}

# Legacy configuration (kept for backwards compatibility, but not used in new version)
SOURCE_CHATS = list(SOURCE_TO_TOPIC_MAPPING.keys())
TARGET_CHATS = {}
for source_mappings in SOURCE_TO_TOPIC_MAPPING.values():
    for target_group_id, topic_id in source_mappings.items():
        TARGET_CHATS[target_group_id] = topic_id
