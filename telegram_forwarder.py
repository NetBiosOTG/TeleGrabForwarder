# telegram_forwarder.py (updated for Railway deployment)
import asyncio
import logging
import os
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, ChatAdminRequiredError, UserBannedInChannelError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import config

# Set up detailed logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Railway logs to stdout
    ]
)
logger = logging.getLogger(__name__)

class TelegramForwarder:
    def __init__(self):
        # Use string session for Railway deployment
        from telethon.sessions import StringSession
        
        session_string = os.getenv('SESSION_STRING', '')
        
        if session_string:
            self.client = TelegramClient(StringSession(session_string), config.API_ID, config.API_HASH)
            logger.info("[SESSION] Using string session from environment")
        else:
            self.client = TelegramClient('forwarder_session', config.API_ID, config.API_HASH)
            logger.info("[SESSION] Using file session (will require phone auth)")
        
        self.forwarded_count = 0
        self.error_count = 0
        
    async def start(self):
        """Initialize and start the userbot"""
        try:
            if os.getenv('SESSION_STRING'):
                await self.client.start()
            else:
                await self.client.start(phone=config.PHONE_NUMBER)
            
            logger.info("[SUCCESS] Userbot started successfully!")
            
            # Get and log bot info
            me = await self.client.get_me()
            logger.info(f"[LOGIN] Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or 'no username'})")
            
            # Verify source and target chats
            await self.verify_chats()
            
            # Register event handlers
            self.client.add_event_handler(self.handle_new_message, events.NewMessage(chats=config.SOURCE_CHATS))
            
            logger.info("[READY] Bot is now listening for messages...")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to start userbot: {e}")
            raise
    
    async def verify_chats(self):
        """Verify access to source and target chats"""
        logger.info("[CHECK] Verifying chat access...")
        
        # Check source chats
        logger.info(f"[DEBUG] Checking {len(config.SOURCE_CHATS)} source chats...")
        for i, chat_id in enumerate(config.SOURCE_CHATS, 1):
            try:
                logger.info(f"[DEBUG] Checking source chat {i}/{len(config.SOURCE_CHATS)}: {chat_id}")
                entity = await self.client.get_entity(chat_id)
                logger.info(f"[OK] Source chat verified: {entity.title} (ID: {chat_id})")
            except Exception as e:
                logger.error(f"[FAIL] Cannot access source chat {chat_id}: {e}")
        
        # Check target chats
        logger.info(f"[DEBUG] Checking {len(config.TARGET_CHATS)} target chats...")
        for i, (chat_id, topic_id) in enumerate(config.TARGET_CHATS.items(), 1):
            try:
                logger.info(f"[DEBUG] Checking target chat {i}/{len(config.TARGET_CHATS)}: {chat_id}")
                entity = await self.client.get_entity(chat_id)
                topic_info = f" (Topic: {topic_id})" if topic_id else " (No topic)"
                logger.info(f"[OK] Target chat verified: {entity.title}{topic_info} (ID: {chat_id})")
            except Exception as e:
                logger.error(f"[FAIL] Cannot access target chat {chat_id}: {e}")
        
        logger.info("[CHECK] Chat verification completed!")
        logger.info("=" * 60)
    
    async def handle_new_message(self, event):
        """Handle new messages from source chats"""
        try:
            message = event.message
            source_chat = await event.get_chat()
            
            # Log incoming message details
            media_type = self.get_media_type(message)
            logger.info(f"[MSG] New message received:")
            logger.info(f"   From: {source_chat.title} (ID: {message.peer_id.channel_id})")
            logger.info(f"   Message ID: {message.id}")
            logger.info(f"   Media: {media_type}")
            logger.info(f"   Text preview: {(message.text or '')[:100]}{'...' if len(message.text or '') > 100 else ''}")
            
            # Forward to all target chats
            await self.forward_to_targets(message, source_chat)
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[ERROR] Error handling message: {e}")
    
    async def forward_to_targets(self, message, source_chat):
        """Forward message to all target chats"""
        for target_chat_id, topic_id in config.TARGET_CHATS.items():
            try:
                target_entity = await self.client.get_entity(target_chat_id)
                
                # Forward the message
                if topic_id:
                    # For groups with topics - forward and reply to topic message
                    forwarded = await self.client.forward_messages(
                        target_chat_id,
                        message
                    )
                    # Note: Topic integration may need different approach
                else:
                    # Forward to general chat
                    forwarded = await self.client.forward_messages(
                        target_chat_id,
                        message
                    )
                
                self.forwarded_count += 1
                
                # Verbose success logging
                topic_info = f" to topic {topic_id}" if topic_id else ""
                logger.info(f"[FORWARD] Message forwarded successfully:")
                logger.info(f"   To: {target_entity.title}{topic_info} (ID: {target_chat_id})")
                logger.info(f"   Original message ID: {message.id}")
                if forwarded:
                    if hasattr(forwarded, 'id'):
                        logger.info(f"   New message ID: {forwarded.id}")
                    elif isinstance(forwarded, list) and len(forwarded) > 0:
                        logger.info(f"   Forwarded message ID: {forwarded[0].id}")
                logger.info(f"   Total forwarded: {self.forwarded_count}")
                
            except FloodWaitError as e:
                logger.warning(f"[WAIT] Flood wait error: Need to wait {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                
            except ChatAdminRequiredError:
                logger.error(f"[PERM] Admin rights required for chat {target_chat_id}")
                
            except UserBannedInChannelError:
                logger.error(f"[BANNED] User banned in chat {target_chat_id}")
                
            except Exception as e:
                self.error_count += 1
                logger.error(f"[FAIL] Failed to forward to {target_chat_id}: {e}")
    
    def get_media_type(self, message):
        """Get human-readable media type"""
        if not message.media:
            return "Text only"
        elif isinstance(message.media, MessageMediaPhoto):
            return "Photo"
        elif isinstance(message.media, MessageMediaDocument):
            if message.media.document.mime_type.startswith('video/'):
                return "Video"
            elif message.media.document.mime_type.startswith('audio/'):
                return "Audio"
            else:
                return "Document"
        else:
            return "Other media"
    
    async def run(self):
        """Main run loop"""
        await self.start()
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("[STOP] Bot stopped by user")
        except Exception as e:
            logger.error(f"[CRASH] Bot crashed: {e}")
        finally:
            logger.info(f"[STATS] Final stats - Forwarded: {self.forwarded_count}, Errors: {self.error_count}")

async def main():
    """Main function"""
    forwarder = TelegramForwarder()
    await forwarder.run()

if __name__ == "__main__":
    print("[START] Starting Telegram Message Forwarder...")
    print("[CONFIG] Configuration loaded:")
    print(f"   Source chats: {len(config.SOURCE_CHATS)} channels")
    print(f"   Target chats: {len(config.TARGET_CHATS)} groups")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[EXIT] Goodbye!")
    except Exception as e:
        print(f"[FATAL] Fatal error: {e}")
