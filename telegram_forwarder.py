# telegram_forwarder.py
import asyncio
import logging
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
        logging.FileHandler('forwarder.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramForwarder:
    def __init__(self):
        self.client = TelegramClient('forwarder_session', config.API_ID, config.API_HASH)
        self.forwarded_count = 0
        self.error_count = 0
        
    async def start(self):
        """Initialize and start the userbot"""
        try:
            await self.client.start(phone=config.PHONE_NUMBER)
            logger.info("[SUCCESS] Userbot started successfully!")
            
            # Get and log bot info
            me = await self.client.get_me()
            logger.info(f"[LOGIN] Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or 'no username'})")
            
            # Verify source and target chats
            await self.verify_chats()
            
            # Register event handlers for each source chat
            for source_chat_id in config.SOURCE_TO_TOPIC_MAPPING.keys():
                self.client.add_event_handler(
                    self.handle_new_message, 
                    events.NewMessage(chats=[source_chat_id])
                )
            
            logger.info("[READY] Bot is now listening for messages...")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to start userbot: {e}")
            raise
    
    async def verify_chats(self):
        """Verify access to source and target chats"""
        logger.info("[CHECK] Verifying chat access...")
        
        # Check source chats and their topic mappings
        logger.info(f"[DEBUG] Checking {len(config.SOURCE_TO_TOPIC_MAPPING)} source chats with topic mappings...")
        for i, (source_chat_id, mappings) in enumerate(config.SOURCE_TO_TOPIC_MAPPING.items(), 1):
            try:
                logger.info(f"[DEBUG] Checking source chat {i}/{len(config.SOURCE_TO_TOPIC_MAPPING)}: {source_chat_id}")
                source_entity = await self.client.get_entity(source_chat_id)
                logger.info(f"[OK] Source chat verified: {source_entity.title} (ID: {source_chat_id})")
                
                # Check each target group and topic for this source
                for target_group_id, topic_id in mappings.items():
                    try:
                        target_entity = await self.client.get_entity(target_group_id)
                        topic_info = f" -> Topic ID: {topic_id}" if topic_id else " -> General chat"
                        logger.info(f"[OK]   Target: {target_entity.title} (ID: {target_group_id}){topic_info}")
                    except Exception as e:
                        logger.error(f"[FAIL]   Cannot access target group {target_group_id}: {e}")
                        
            except Exception as e:
                logger.error(f"[FAIL] Cannot access source chat {source_chat_id}: {e}")
        
        logger.info("[CHECK] Chat verification completed!")
        logger.info("=" * 60)
    
    async def handle_new_message(self, event):
        """Handle new messages from source chats"""
        try:
            message = event.message
            source_chat = await event.get_chat()
            
            # FIXED: Get the proper chat ID that matches our config format
            # For channels/supergroups, we need to use the negative format (-100 prefix)
            if hasattr(message.peer_id, 'channel_id'):
                # Convert to the standard negative format that Telegram uses
                source_chat_id = -1000000000000 - message.peer_id.channel_id
            else:
                source_chat_id = message.peer_id.chat_id
            
            # Log incoming message details
            media_type = self.get_media_type(message)
            logger.info(f"[MSG] New message received:")
            logger.info(f"   From: {source_chat.title} (ID: {source_chat_id})")
            logger.info(f"   Message ID: {message.id}")
            logger.info(f"   Media: {media_type}")
            logger.info(f"   Text preview: {(message.text or '')[:100]}{'...' if len(message.text or '') > 100 else ''}")
            
            # Forward to mapped target topics
            await self.forward_to_mapped_topics(message, source_chat, source_chat_id)
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[ERROR] Error handling message: {e}")
    
    async def forward_to_mapped_topics(self, message, source_chat, source_chat_id):
        """Forward message to mapped target topics based on source chat"""
        # Get the mapping for this source chat
        if source_chat_id not in config.SOURCE_TO_TOPIC_MAPPING:
            logger.warning(f"[SKIP] No mapping found for source chat {source_chat_id}")
            return
        
        mappings = config.SOURCE_TO_TOPIC_MAPPING[source_chat_id]
        
        for target_group_id, topic_id in mappings.items():
            try:
                target_entity = await self.client.get_entity(target_group_id)
                
                # Forward the message
                if topic_id:
                    # Forward to specific topic in the group
                    # For topics, we need to send to the supergroup and specify the topic thread
                    forwarded = await self.client.forward_messages(
                        entity=target_group_id,
                        messages=message,
                        reply_to=topic_id  # Reply to the topic's root message
                    )
                else:
                    # Forward to general chat (no topic)
                    forwarded = await self.client.forward_messages(
                        target_group_id,
                        message
                    )
                
                self.forwarded_count += 1
                
                # Verbose success logging
                topic_info = f" to topic {topic_id}" if topic_id else " to general chat"
                logger.info(f"[FORWARD] Message forwarded successfully:")
                logger.info(f"   From: {source_chat.title} (ID: {source_chat_id})")
                logger.info(f"   To: {target_entity.title}{topic_info} (Group ID: {target_group_id})")
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
                # Retry the forward after waiting
                try:
                    if topic_id:
                        forwarded = await self.client.forward_messages(
                            entity=target_group_id,
                            messages=message,
                            reply_to=topic_id
                        )
                    else:
                        forwarded = await self.client.forward_messages(
                            target_group_id,
                            message
                        )
                    self.forwarded_count += 1
                    logger.info(f"[RETRY] Successfully forwarded after flood wait")
                except Exception as retry_e:
                    logger.error(f"[RETRY_FAIL] Failed to forward after flood wait: {retry_e}")
                
            except ChatAdminRequiredError:
                logger.error(f"[PERM] Admin rights required for group {target_group_id}")
                
            except UserBannedInChannelError:
                logger.error(f"[BANNED] User banned in group {target_group_id}")
                
            except Exception as e:
                self.error_count += 1
                logger.error(f"[FAIL] Failed to forward to {target_group_id} topic {topic_id}: {e}")
    
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
    print(f"   Source chats with topic mappings: {len(config.SOURCE_TO_TOPIC_MAPPING)}")
    
    # Show detailed mapping information
    for source_id, mappings in config.SOURCE_TO_TOPIC_MAPPING.items():
        print(f"   Source {source_id} -> {len(mappings)} target topics")
    
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[EXIT] Goodbye!")
    except Exception as e:
        print(f"[FATAL] Fatal error: {e}")
