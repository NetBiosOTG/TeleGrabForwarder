import os

# Your Telegram API credentials
API_ID = '21637014'
API_HASH = '410955dedb8c4b1628eb41df366762c6'
PHONE_NUMBER = '+18126979150'
# Mapping structure: Source chat ID -> Target groups with their topics
# SOURCE_TO_TOPIC_MAPPING = {
#     source_chat_id: {
#         target_group_id: topic_id,  # Use topic_id from forum topics, or None for general chat
#         target_group_id2: topic_id2,
#         # ... more target groups
#     },
#     # ... more source chats
# }

SOURCE_TO_TOPIC_MAPPING = {
    # MetaWin.com MAIN TG: Messages from "MetaWin.com MAIN TG" source channel
    -1001892037773: {   # MetaWin.com MAIN TG source channel ID
        -1002756711574: 36,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Shuffle.com - Bonus Code VIP: Messages from "Shuffle.com - Bonus Code VIP" source channel
    -1002185512641: {   # Shuffle.com - Bonus Code VIP source channel ID
        -1002756711574: 8,      # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Winna.com - Winna Casino: Messages from "Winna.com - Winna Casino" source channel
    -1002472636693: {   # Winna.com - Winna Casino source channel ID
        -1002756711574: 34,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # ₿C Token Lounge: Messages from "₿C Token Lounge" source channel
    -1002249193735: {   # ₿C Token Lounge source channel ID
        -1002756711574: 52,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Goated Drops: Messages from "Goated Drops" source channel
    -1002234305882: {   # Goated Drops source channel ID
        -1002756711574: 26,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Stake.US Daily Drops 🇺🇸: Messages from "Stake.US Daily Drops 🇺🇸" source channel
    -1002133338932: {   # Stake.US Daily Drops 🇺🇸 source channel ID
        -1002756711574: 16,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # BC.Game 🔔 Notifications: Messages from "BC.Game 🔔 Notifications" source channel
    -1001166926064: {   # BC.Game 🔔 Notifications source channel ID
        -1002756711574: 6,      # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Shuffle.com: Messages from "Shuffle.com" source channel
    -1001517758091: {   # Shuffle.com source channel ID
        -1002756711574: 10,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Razed - Community: Messages from "Razed - Community" source channel
    -1002061136110: {   # Razed - Community source channel ID
        -1002756711574: 30,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Staxx Boosts: Messages from "Staxx Boosts" source channel
    -1002378946187: {   # Staxx Boosts source channel ID
        -1002756711574: 49,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Shuffle Sports: Messages from "Shuffle Sports" source channel
    -1002109995475: {   # Shuffle Sports source channel ID
        -1002756711574: 12,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Goated.com: Messages from "Goated.com" source channel
    -1002434383104: {   # Goated.com source channel ID
        -1002756711574: 28,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Stake.com - Play Smarter: Messages from "Stake.com - Play Smarter" source channel
    -1001356950325: {   # Stake.com - Play Smarter source channel ID
        -1002756711574: 18,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Roobet: Messages from "Roobet" source channel
    -1001278995047: {   # Roobet source channel ID
        -1002756711574: 38,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Shuffle JP ブースト: Messages from "Shuffle JP ブースト" source channel
    -1002060359531: {   # Shuffle JP ブースト source channel ID
        -1002756711574: 14,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Stake.us - Play Smarter: Messages from "Stake.us - Play Smarter" source channel
    -1001751288924: {   # Stake.us - Play Smarter source channel ID
        -1002756711574: 20,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Gamba.com: Messages from "Gamba.com" source channel
    -1002121217568: {   # Gamba.com source channel ID
        -1002756711574: 40,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)  
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Luckybird.io - Play Smarter: Messages from "Luckybird.io - Play Smarter" source channel
    -1001703288746: {   # Luckybird.io - Play Smarter source channel ID
        -1002756711574: 44,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Stake.us - VIP Notices: Messages from "Stake.us - VIP Notices" source channel
    -1001542279201: {   # Stake.us - VIP Notices source channel ID
        -1002756711574: 22,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Razed Sports: Messages from "Razed Sports" source channel
    -1002379667487: {   # Razed Sports source channel ID
        -1002756711574: 42,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # Sicodice Official Channel: Messages from "Sicodice Official Channel" source channel
    -1001677525545: {   # Sicodice Official Channel source channel ID
        -1002756711574: 46,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    },

    # High Rollers - Stake.US - (Unofficial): Messages from "High Rollers - Stake.US - (Unofficial)" source channel
    -1002102309936: {   # High Rollers - Stake.US - (Unofficial) source channel ID
        -1002756711574: 24,     # Bonus Codes (Topic ID)
        -1002027750840: 501,    # TipMeTips (Bonus Codes)
        -1002210132078: None,   # Hotmamajess's Playground (No Topic)
    }
    
}

# Legacy configuration (kept for backwards compatibility, but not used in new version)
SOURCE_CHATS = list(SOURCE_TO_TOPIC_MAPPING.keys())
TARGET_CHATS = {}
for source_mappings in SOURCE_TO_TOPIC_MAPPING.values():
    for target_group_id, topic_id in source_mappings.items():
        TARGET_CHATS[target_group_id] = topic_id
