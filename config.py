import os

# Telegram API credentials - get these from https://my.telegram.org
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '')

# Source chats to monitor (list of chat IDs or usernames)
# Examples: [-1001234567890, '@channelname', 'https://t.me/channelname']
SOURCE_CHATS = [
    -1002133338932, -1002234305882, -1002185512641, -1002249193735,
    -1001892037773, -1002434383104, -1002061136110, -1001166926064,
    -1002109995475, -1001517758091, -1002060359531, -1001278995047,
    -1002414808284, -1001356950325, -1001751288924, -1001703288746, 
    -1001738096535, -1001542279201, -1002102309936, -1002378946187
]

# Target chats to forward to (dict with chat_id: topic_id)
# topic_id can be None for regular groups
TARGET_CHATS = {
   -1002210132078: None,  # Hotmamajess's Playground (no topic)
   -1002336070508: None,   # Casino sites hub (no topic)
   -1002027750840: 501
}

# Validate configuration
def validate_config():
    """Validate that all required config values are set"""
    errors = []
    
    if not API_ID or API_ID == 0:
        errors.append("API_ID is required")
    
    if not API_HASH:
        errors.append("API_HASH is required")
    
    if not PHONE_NUMBER:
        errors.append("PHONE_NUMBER is required")
    
    if not SOURCE_CHATS:
        errors.append("At least one SOURCE_CHAT is required")
    
    if not TARGET_CHATS:
        errors.append("At least one TARGET_CHAT is required")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

# Validate on import
validate_config()
