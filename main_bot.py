from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, FloodWaitError
import asyncio
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get credentials from environment variables
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING', '')

# Validate environment variables
if not API_ID or not API_HASH:
    logger.error("API_ID and API_HASH environment variables are required!")
    exit(1)

if not SESSION_STRING:
    logger.error("TELEGRAM_SESSION_STRING environment variable is required!")
    logger.info("Run generate_session.py locally first to get your session string")
    exit(1)

class TelegramForwarder:
    def __init__(self):
        self.client = TelegramClient(
            StringSession(SESSION_STRING),
            API_ID,
            API_HASH,
            connection_retries=5,
            retry_delay=3,
            timeout=30
        )
    
    async def start(self):
        """Start the Telegram client"""
        try:
            await self.client.start()
            me = await self.client.get_me()
            logger.info(f"Successfully connected as {me.first_name} (@{me.username})")
            return True
        except Exception as e:
            logger.error(f"Failed to start client: {e}")
            return False
    
    async def get_channel_info(self, channel_id):
        """Get information about a channel"""
        try:
            entity = await self.client.get_entity(channel_id)
            logger.info(f"Channel: {entity.title} (ID: {entity.id})")
            return entity
        except FloodWaitError as e:
            logger.warning(f"Rate limited. Waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            return await self.get_channel_info(channel_id)
        except Exception as e:
            logger.error(f"Error accessing channel {channel_id}: {e}")
            return None
    
    async def forward_message(self, from_channel, to_channel, message_id):
        """Forward a message from one channel to another"""
        try:
            await self.client.forward_messages(to_channel, message_id, from_channel)
            logger.info(f"Forwarded message {message_id} from {from_channel} to {to_channel}")
            return True
        except FloodWaitError as e:
            logger.warning(f"Rate limited. Waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
            return await self.forward_message(from_channel, to_channel, message_id)
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
            return False
    
    async def listen_for_messages(self, channel_id):
        """Listen for new messages in a channel"""
        try:
            logger.info(f"Starting to listen for messages in channel {channel_id}")
            
            @self.client.on(events.NewMessage(chats=channel_id))
            async def handler(event):
                logger.info(f"New message received: {event.message.id}")
                # Add your forwarding logic here
                # await self.forward_message(channel_id, target_channel, event.message.id)
            
            # Keep the client running
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Error in message listener: {e}")
    
    async def disconnect(self):
        """Disconnect the client"""
        await self.client.disconnect()
        logger.info("Client disconnected")

async def main():
    """Main function"""
    forwarder = TelegramForwarder()
    
    try:
        # Start the client
        if not await forwarder.start():
            return
        
        # Test channel access (replace with your channel ID)
        channel_id = 2210132078  # Your channel ID
        channel_info = await forwarder.get_channel_info(channel_id)
        
        if channel_info:
            logger.info("Channel access successful!")
            # Add your main bot logic here
            # await forwarder.listen_for_messages(channel_id)
        else:
            logger.error("Failed to access channel")
    
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        await forwarder.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
