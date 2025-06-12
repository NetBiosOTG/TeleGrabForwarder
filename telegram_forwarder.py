# telegram_forwarder.py
import asyncio
import logging
from datetime import datetime
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, ChatAdminRequiredError, UserBannedInChannelError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.sessions import StringSession
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
        # Initialize client with session string
        if config.TELEGRAM_SESSION_STRING:
            logger.info("[INIT] Using session string authentication")
            self.client = TelegramClient(
                StringSession(config.TELEGRAM_SESSION_STRING), 
                config.API_ID, 
                config.API_HASH
            )
        else:
            logger.warning("[INIT] No session string found, falling back to phone authentication")
            self.client = TelegramClient('forwarder_session', config.API_ID, config.API_HASH)
        
        self.forwarded_count = 0
        self.error_count = 0
        
    async def start(self):
        """Initialize and start the userbot"""
        try:
            if config.TELEGRAM_SESSION_STRING:
                # Start with session string (no phone needed)
                await self.client.start()
                logger.info("[SUCCESS] Userbot started with session string!")
            else:
                # Fallback to phone authentication
                await self.client.start(phone=config.PHONE_NUMBER)
                logger.info("[SUCCESS] Userbot started with phone authentication!")
            
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
            if not config.TELEGRAM_SESSION_STRING:
                logger.error("[HINT] Try generating a session string using session_generator.py")
            raise
    
    async def verify_chats(self):
        """Verify access to source and target chats and check for topics"""
        logger.info("[CHECK] Verifying chat access and topics...")
        
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
                        
                        if topic_id:
                            # Verify the topic exists
                            topic_valid = await self.verify_topic(target_group_id, topic_id)
                            topic_status = "✓ VALID" if topic_valid else "✗ INVALID"
                            logger.info(f"[OK]   Target: {target_entity.title} (ID: {target_group_id}) -> Topic ID: {topic_id} [{topic_status}]")
                        else:
                            logger.info(f"[OK]   Target: {target_entity.title} (ID: {target_group_id}) -> General chat")
                            
                    except Exception as e:
                        logger.error(f"[FAIL]   Cannot access target group {target_group_id}: {e}")
                        
            except Exception as e:
                logger.error(f"[FAIL] Cannot access source chat {source_chat_id}: {e}")
        
        logger.info("[CHECK] Chat verification completed!")
        logger.info("=" * 60)
    
    async def verify_topic(self, group_id, topic_id):
        """Verify if a topic exists in a group"""
        try:
            # Try to get the specific message that represents the topic
            message = await self.client.get_messages(group_id, ids=topic_id)
            return message is not None
        except Exception as e:
            logger.debug(f"[TOPIC_CHECK] Topic {topic_id} in group {group_id} verification failed: {e}")
            return False
    
    def get_chat_id_from_peer(self, peer):
        """Convert peer to the correct chat ID format that matches our config"""
        if hasattr(peer, 'channel_id'):
            # For channels/supergroups, convert to the standard -100 prefix format
            return int(f"-100{peer.channel_id}")
        elif hasattr(peer, 'chat_id'):
            # For regular groups, use negative format
            return -peer.chat_id
        elif hasattr(peer, 'user_id'):
            # For private chats (shouldn't happen in this context, but just in case)
            return peer.user_id
        else:
            logger.error(f"[ERROR] Unknown peer type: {type(peer)}")
            return None
    
    async def handle_new_message(self, event):
        """Handle new messages from source chats"""
        try:
            message = event.message
            source_chat = await event.get_chat()
            
            # Use the method to get the proper chat ID
            source_chat_id = self.get_chat_id_from_peer(message.peer_id)
            
            if source_chat_id is None:
                logger.error("[ERROR] Could not determine source chat ID")
                return
            
            # Log incoming message details
            media_type = self.get_media_type(message)
            logger.info(f"[MSG] New message received:")
            logger.info(f"   From: {source_chat.title} (ID: {source_chat_id})")
            logger.info(f"   Message ID: {message.id}")
            logger.info(f"   Media: {media_type}")
            logger.info(f"   Text preview: {(message.text or '')[:100]}{'...' if len(message.text or '') > 100 else ''}")
            
            # Debug: Check if this source_chat_id exists in our mapping
            if source_chat_id in config.SOURCE_TO_TOPIC_MAPPING:
                logger.info(f"[MAPPING] Found mapping for source chat {source_chat_id}")
                mappings = config.SOURCE_TO_TOPIC_MAPPING[source_chat_id]
                logger.info(f"[MAPPING] Will forward to {len(mappings)} target groups")
                for target_id, topic_id in mappings.items():
                    logger.info(f"[MAPPING]   Target: {target_id} -> Topic: {topic_id}")
            else:
                logger.warning(f"[NO_MAPPING] No mapping found for source chat {source_chat_id}")
                logger.info(f"[DEBUG] Available source chat IDs in config: {list(config.SOURCE_TO_TOPIC_MAPPING.keys())}")
            
            # Forward to mapped target topics (completely anonymously)
            await self.forward_anonymously(message, source_chat, source_chat_id)
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[ERROR] Error handling message: {e}")
            import traceback
            logger.error(f"[ERROR] Traceback: {traceback.format_exc()}")
    
    async def forward_anonymously(self, message, source_chat, source_chat_id):
        """Forward message completely anonymously - no trace of original source"""
        # Get the mapping for this source chat
        if source_chat_id not in config.SOURCE_TO_TOPIC_MAPPING:
            logger.warning(f"[SKIP] No mapping found for source chat {source_chat_id}")
            return
        
        mappings = config.SOURCE_TO_TOPIC_MAPPING[source_chat_id]
        logger.info(f"[ANONYMOUS_FORWARD] Processing {len(mappings)} target mappings for source {source_chat_id}")
        
        for target_group_id, topic_id in mappings.items():
            try:
                target_entity = await self.client.get_entity(target_group_id)
                success = False
                
                # Always send as a new message to completely hide the source
                logger.info(f"[ANONYMOUS_FORWARD] Sending anonymous message to {target_entity.title}")
                
                if message.media:
                    # Download media first, then send as new message
                    try:
                        # Download the media file
                        media_file = await message.download_media(file=bytes)
                        
                        # Send as new message with media
                        result = await self.client.send_message(
                            entity=target_group_id,
                            message=message.text or "",
                            reply_to=topic_id if topic_id else None,
                            file=media_file
                        )
                        success = True
                        logger.info(f"[ANONYMOUS_SUCCESS] Media message sent anonymously")
                        
                    except Exception as media_error:
                        logger.error(f"[MEDIA_ERROR] Failed to process media: {media_error}")
                        
                        # Fallback: try to send just the text if media fails
                        if message.text:
                            try:
                                result = await self.client.send_message(
                                    entity=target_group_id,
                                    message=message.text,
                                    reply_to=topic_id if topic_id else None
                                )
                                success = True
                                logger.info(f"[ANONYMOUS_SUCCESS] Text-only message sent (media failed)")
                            except Exception as text_error:
                                logger.error(f"[TEXT_ERROR] Failed to send text fallback: {text_error}")
                else:
                    # Send text message
                    if message.text:
                        result = await self.client.send_message(
                            entity=target_group_id,
                            message=message.text,
                            reply_to=topic_id if topic_id else None
                        )
                        success = True
                        logger.info(f"[ANONYMOUS_SUCCESS] Text message sent anonymously")
                    else:
                        logger.warning(f"[SKIP] Empty message with no media - nothing to forward")
                
                if success:
                    self.forwarded_count += 1
                    
                    # Verbose success logging
                    topic_info = f" to topic {topic_id}" if topic_id else " to general chat"
                    logger.info(f"[ANONYMOUS_SUCCESS] Message sent anonymously:")
                    logger.info(f"   From: {source_chat.title} (ID: {source_chat_id}) [HIDDEN]")
                    logger.info(f"   To: {target_entity.title}{topic_info} (Group ID: {target_group_id})")
                    logger.info(f"   Original message ID: {message.id} [NOT PRESERVED]")
                    logger.info(f"   Total forwarded: {self.forwarded_count}")
                
            except FloodWaitError as e:
                logger.warning(f"[WAIT] Flood wait error: Need to wait {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                # Retry after waiting
                await self.retry_anonymous_forward(message, source_chat_id, target_group_id, topic_id, target_entity)
                
            except ChatAdminRequiredError:
                logger.error(f"[PERM] Admin rights required for group {target_group_id}")
                
            except UserBannedInChannelError:
                logger.error(f"[BANNED] User banned in group {target_group_id}")
                
            except Exception as e:
                self.error_count += 1
                logger.error(f"[FAIL] Failed to send anonymous message to {target_group_id} topic {topic_id}: {e}")
                logger.error(f"[DEBUG] Error type: {type(e).__name__}")
                import traceback
                logger.error(f"[DEBUG] Traceback: {traceback.format_exc()}")
    
    async def retry_anonymous_forward(self, message, source_chat_id, target_group_id, topic_id, target_entity):
        """Retry anonymous forwarding after flood wait"""
        try:
            if message.media:
                # Download and send media
                media_file = await message.download_media(file=bytes)
                result = await self.client.send_message(
                    entity=target_group_id,
                    message=message.text or "",
                    reply_to=topic_id if topic_id else None,
                    file=media_file
                )
            else:
                # Send text message
                result = await self.client.send_message(
                    entity=target_group_id,
                    message=message.text or "",
                    reply_to=topic_id if topic_id else None
                )
            
            self.forwarded_count += 1
            topic_info = f" to topic {topic_id}" if topic_id else " to general chat"
            logger.info(f"[RETRY_SUCCESS] Anonymous message sent successfully after retry:")
            logger.info(f"   To: {target_entity.title}{topic_info} (Group ID: {target_group_id})")
            logger.info(f"   Total forwarded: {self.forwarded_count}")
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[RETRY_FAIL] Anonymous retry failed for {target_group_id}: {e}")
    
    def get_media_type(self, message):
        """Get media type description for logging"""
        if not message.media:
            return "Text only"
        elif isinstance(message.media, MessageMediaPhoto):
            return "Photo"
        elif isinstance(message.media, MessageMediaDocument):
            if message.media.document:
                if message.media.document.mime_type:
                    if 'video' in message.media.document.mime_type:
                        return "Video"
                    elif 'audio' in message.media.document.mime_type:
                        return "Audio"
                    elif 'image' in message.media.document.mime_type:
                        return "Image/GIF"
                    else:
                        return f"Document ({message.media.document.mime_type})"
                return "Document"
            return "Document"
        else:
            return f"Other media ({type(message.media).__name__})"
    
    async def run_forever(self):
        """Keep the bot running"""
        try:
            logger.info("[RUNNING] Anonymous forwarder is running... Press Ctrl+C to stop")
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("[STOP] Bot stopped by user")
        except Exception as e:
            logger.error(f"[ERROR] Bot crashed: {e}")
            raise
        finally:
            await self.client.disconnect()
            logger.info(f"[STATS] Final stats - Forwarded: {self.forwarded_count}, Errors: {self.error_count}")

async def main():
    """Main entry point"""
    forwarder = TelegramForwarder()
    
    try:
        await forwarder.start()
        await forwarder.run_forever()
    except Exception as e:
        logger.error(f"[FATAL] Application failed to start: {e}")
        import traceback
        logger.error(f"[FATAL] Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(main())
