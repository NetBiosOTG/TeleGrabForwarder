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
    # BOOST by MetaWin: Messages from "BOOST by MetaWin" source channel
    -1002079157553: {   # BOOST by MetaWin source channel ID
       -1002210132078: None,    # Hotmamajess's Playground (No Topic)
       -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Shuffle.com - Bonus Code VIP: Messages from "Shuffle.com - Bonus Code VIP" source channel
    -1002185512641: {   # Shuffle.com - Bonus Code VIP source channel ID
       -1002210132078: None,    # Hotmamajess's Playground (No Topic)
       -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Winna.com - Winna Casino: Messages from "Winna.com - Winna Casino" source channel
    -1002472636693: {   # Winna.com - Winna Casino source channel ID
       -1002210132078: None,    # Hotmamajess's Playground (No Topic)
       -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },
    
    # ₿C Token Lounge: Messages from "₿C Token Lounge" source channel
    -1002249193735: {   # ₿C Token Lounge source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Goated Drops: Messages from "Goated Drops" source channel
    -1002234305882: {   # Goated Drops source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Stake.US Daily Drops & HighRollers 🇺🇸: Messages from "Stake.US Daily Drops 🇺🇸" source channel
    -1002343155225: {   # Stake.US Daily Drops 🇺🇸 source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # BC.Game 🔔 Notifications: Messages from "BC.Game 🔔 Notifications" source channel
    -1001166926064: {   # BC.Game 🔔 Notifications source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Shuffle.com: Messages from "Shuffle.com" source channel
    -1001517758091: {   # Shuffle.com source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Razed - Community: Messages from "Razed - Community" source channel
    -1002061136110: {   # Razed - Community source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Shuffle Sports: Messages from "Shuffle Sports" source channel
    -1002109995475: {   # Shuffle Sports source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Goated.com: Messages from "Goated.com" source channel
    -1002434383104: {   # Goated.com source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Stake.com Play Smarter: Messages from "Stake.com Play Smarter" source channel
    -1002239669640: {   # Stake.com Play Smarter source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Roobet: Messages from "Roobet" source channel
    -1001278995047: {   # Roobet source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Shuffle JP ブースト: Messages from "Shuffle JP ブースト" source channel
    -1002060359531: {   # Shuffle JP ブースト source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Stake.us - Play Smarter: Messages from "Stake.us - Play Smarter" source channel
    -1001751288924: {   # Stake.us - Play Smarter source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Gamba.com: Messages from "Gamba.com" source channel
    -1002121217568: {   # Gamba.com source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Luckybird.io - Play Smarter: Messages from "Luckybird.io - Play Smarter" source channel
    -1001703288746: {   # Luckybird.io - Play Smarter source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Stake.us - VIP Notices: Messages from "Stake.us - VIP Notices" source channel
    -1001542279201: {   # Stake.us - VIP Notices source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Razed Sports: Messages from "Razed Sports" source channel
    -1002379667487: {   # Razed Sports source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

    # Sicodice Official Channel: Messages from "Sicodice Official Channel" source channel
    -1001677525545: {   # Sicodice Official Channel source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

     # Bonus Codes-Stake.com: Messages from "Bonus Codes-Stake.com" source channel
    -1002239669640: {   # Bonus Codes - Stake.com source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    },

     # Razed Jp - レイズド日本公式: Messages from "Razed Jp - レイズド日本公式" source channel
    -1002400779729: {   # Razed Jp - レイズド日本公式 source channel ID
        -1002210132078: None,    # Hotmamajess's Playground (No Topic)
        -1002027750840: 501,     # TipMeTips (Bonus Codes Topic)
    }

    # Test
   # -1002751892666: { #Jess,Nasty,Me
   #    -1002561417317: None, #Nasty,Me
   #}

    
}
    
# Legacy configuration (kept for backwards compatibility, but not used in new version)
SOURCE_CHATS = list(SOURCE_TO_TOPIC_MAPPING.keys())
TARGET_CHATS = {}
for source_mappings in SOURCE_TO_TOPIC_MAPPING.values():
    for target_group_id, topic_id in source_mappings.items():
        TARGET_CHATS[target_group_id] = topic_id
