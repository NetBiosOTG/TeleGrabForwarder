# telegram_forwarder.py
import asyncio
import logging
from datetime import datetime
import random
import aiohttp
import json
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, ChatAdminRequiredError, UserBannedInChannelError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.functions.messages import ForwardMessagesRequest
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
        self.translation_count = 0
        
        # Channels that need translation (Japanese to English)
        self.translate_channels = {
            -1002060359531: "ja",  # Shuffle JP ブースト - Japanese
            -1002400779729: "ja",  # Razed Jp - レイズド日本公式
            -1002751892666: "ja",  #Jess,Nasty,Me
            }
        
    async def translate_text(self, text, source_lang="ja", target_lang="en"):
        """Translate text using Google Translate API (free tier)"""
        if not text or not text.strip():
            return text
            
        try:
            # Use Google Translate's free API endpoint
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        # Extract translated text from the response
                        translated_text = ""
                        if result and len(result) > 0 and len(result[0]) > 0:
                            for translation in result[0]:
                                if translation[0]:
                                    translated_text += translation[0]
                        
                        if translated_text:
                            self.translation_count += 1
                            logger.info(f"[TRANSLATION] Successfully translated text:")
                            logger.info(f"   Original: {text[:100]}{'...' if len(text) > 100 else ''}")
                            logger.info(f"   Translated: {translated_text[:100]}{'...' if len(translated_text) > 100 else ''}")
                            return translated_text
                        else:
                            logger.warning("[TRANSLATION] No translation returned, using original text")
                            return text
                    else:
                        logger.error(f"[TRANSLATION] Translation API error: HTTP {response.status}")
                        return text
                        
        except Exception as e:
            logger.error(f"[TRANSLATION] Translation failed: {e}")
            return text
    
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
                
                # Check if this channel needs translation
                translation_info = ""
                if source_chat_id in self.translate_channels:
                    translation_info = f" [TRANSLATION: {self.translate_channels[source_chat_id]} → en]"
                
                logger.info(f"[OK] Source chat verified: {source_entity.title} (ID: {source_chat_id}){translation_info}")
                
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
    
    def generate_random_id(self):
        """Generate a random ID for Telegram requests"""
        return random.randint(1, 2**63 - 1)
    
    def get_media_type(self, message):
        """Get the media type of a message"""
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
            translation_note = " [NEEDS TRANSLATION]" if source_chat_id in self.translate_channels else ""
            logger.info(f"[MSG] New message received{translation_note}:")
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
            
            # Forward to mapped target topics
            await self.forward_to_mapped_topics(message, source_chat, source_chat_id)
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[ERROR] Error handling message: {e}")
            import traceback
            logger.error(f"[ERROR] Traceback: {traceback.format_exc()}")
    
    async def forward_to_mapped_topics(self, message, source_chat, source_chat_id):
        """Forward message to mapped target topics based on source chat"""
        # Get the mapping for this source chat
        if source_chat_id not in config.SOURCE_TO_TOPIC_MAPPING:
            logger.warning(f"[SKIP] No mapping found for source chat {source_chat_id}")
            return
        
        mappings = config.SOURCE_TO_TOPIC_MAPPING[source_chat_id]
        logger.info(f"[FORWARD_START] Processing {len(mappings)} target mappings for source {source_chat_id}")
        
        # Check if this message needs translation
        translated_text = None
        if source_chat_id in self.translate_channels and message.text:
            source_lang = self.translate_channels[source_chat_id]
            logger.info(f"[TRANSLATION] Translating message from {source_lang} to English...")
            translated_text = await self.translate_text(message.text, source_lang, "en")
        
        for target_group_id, topic_id in mappings.items():
            try:
                target_entity = await self.client.get_entity(target_group_id)
                success = False
                
                if topic_id:
                    # Forward to specific topic in the group
                    logger.info(f"[FORWARD_ATTEMPT] Attempting to forward to topic {topic_id} in {target_entity.title}")
                    
                    try:
                        # If we have a translation, send translated message instead of forwarding
                        if translated_text and source_chat_id in self.translate_channels:
                            logger.info(f"[TRANSLATION_FORWARD] Sending translated message to topic {topic_id}")
                            
                            # Create a formatted message with translation info
                            formatted_message = f"🌐 Translated from {source_chat.title}:\n\n{translated_text}"
                            
                            if message.media:
                                # For media messages, send with translated caption
                                result = await self.client.send_message(
                                    entity=target_group_id,
                                    message=formatted_message,
                                    reply_to=topic_id,
                                    file=message.media
                                )
                            else:
                                # For text messages, send the translated text
                                result = await self.client.send_message(
                                    entity=target_group_id,
                                    message=formatted_message,
                                    reply_to=topic_id
                                )
                            success = True
                            logger.info(f"[TRANSLATION_SUCCESS] Translated message sent successfully")
                        else:
                            # Regular forward without translation
                            # FIXED: Use 'id' instead of 'msg_ids'
                            result = await self.client(ForwardMessagesRequest(
                                from_peer=await self.client.get_input_entity(source_chat_id),
                                id=[message.id],  # FIXED: Changed from msg_ids to id
                                to_peer=await self.client.get_input_entity(target_group_id),
                                reply_to_msg_id=topic_id,
                                random_id=[self.generate_random_id()],
                                drop_author=False,
                                drop_media_captions=False
                            ))
                            success = True
                            logger.info(f"[TOPIC_SUCCESS] Method 1 (ForwardMessagesRequest) succeeded")
                        
                    except Exception as e1:
                        logger.warning(f"[TOPIC_FAIL] Primary method failed: {e1}")
                        
                        try:
                            # Fallback method: Try using send_message with forwarded content
                            if message.media:
                                # For media messages, download and re-upload
                                message_text = translated_text if (translated_text and source_chat_id in self.translate_channels) else message.text
                                display_text = message_text or "[Forwarded media]"
                                
                                if translated_text and source_chat_id in self.translate_channels:
                                    display_text = f"🌐 Translated from {source_chat.title}:\n\n{display_text}"
                                else:
                                    display_text = f"🔄 Forwarded from {source_chat.title}:\n\n{display_text}"
                                
                                result = await self.client.send_message(
                                    entity=target_group_id,
                                    message=display_text,
                                    reply_to=topic_id,
                                    file=message.media
                                )
                            else:
                                # For text messages, send the text (translated if available)
                                if translated_text and source_chat_id in self.translate_channels:
                                    forwarded_text = f"🌐 Translated from {source_chat.title}:\n\n{translated_text}"
                                else:
                                    forwarded_text = f"🔄 Forwarded from {source_chat.title}:\n\n{message.text}"
                                
                                result = await self.client.send_message(
                                    entity=target_group_id,
                                    message=forwarded_text,
                                    reply_to=topic_id
                                )
                            success = True
                            logger.info(f"[TOPIC_SUCCESS] Method 2 (send_message) succeeded")
                            
                        except Exception as e2:
                            logger.warning(f"[TOPIC_FAIL] Method 2 failed: {e2}")
                            
                            try:
                                # Method 3: Simple forward without topic (FALLBACK)
                                result = await self.client.forward_messages(
                                    target_group_id,
                                    message,
                                    from_peer=source_chat_id
                                )
                                success = True
                                logger.info(f"[FALLBACK_SUCCESS] Forwarded to general chat (topic forward failed)")
                                
                            except Exception as e3:
                                logger.error(f"[TOPIC_FAIL] All methods failed: {e3}")
                else:
                    # Forward to general chat (no topic)
                    logger.info(f"[FORWARD_ATTEMPT] Forwarding to general chat in {target_entity.title}")
                    
                    if translated_text and source_chat_id in self.translate_channels:
                        # Send translated message to general chat
                        logger.info(f"[TRANSLATION_FORWARD] Sending translated message to general chat")
                        formatted_message = f"🌐 Translated from {source_chat.title}:\n\n{translated_text}"
                        
                        if message.media:
                            result = await self.client.send_message(
                                entity=target_group_id,
                                message=formatted_message,
                                file=message.media
                            )
                        else:
                            result = await self.client.send_message(
                                entity=target_group_id,
                                message=formatted_message
                            )
                        success = True
                    else:
                        # Regular forward
                        result = await self.client.forward_messages(
                            target_group_id,
                            message,
                            from_peer=source_chat_id
                        )
                        success = True
                
                if success:
                    self.forwarded_count += 1
                    
                    # Verbose success logging
                    topic_info = f" to topic {topic_id}" if topic_id else " to general chat"
                    translation_info = " (TRANSLATED)" if translated_text and source_chat_id in self.translate_channels else ""
                    logger.info(f"[FORWARD_SUCCESS] Message forwarded successfully{translation_info}:")
                    logger.info(f"   From: {source_chat.title} (ID: {source_chat_id})")
                    logger.info(f"   To: {target_entity.title}{topic_info} (Group ID: {target_group_id})")
                    logger.info(f"   Original message ID: {message.id}")
                    logger.info(f"   Total forwarded: {self.forwarded_count}, Translated: {self.translation_count}")
                
            except FloodWaitError as e:
                logger.warning(f"[WAIT] Flood wait error: Need to wait {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
                # Retry after waiting (note: this will use the original message, not translated)
                await self.retry_forward(message, source_chat_id, target_group_id, topic_id, target_entity)
                
            except ChatAdminRequiredError:
                logger.error(f"[PERM] Admin rights required for group {target_group_id}")
                
            except UserBannedInChannelError:
                logger.error(f"[BANNED] User banned in group {target_group_id}")
                
            except Exception as e:
                self.error_count += 1
                logger.error(f"[FAIL] Failed to forward to {target_group_id} topic {topic_id}: {e}")
                logger.error(f"[DEBUG] Error type: {type(e).__name__}")
                import traceback
                logger.error(f"[DEBUG] Traceback: {traceback.format_exc()}")
    
    async def retry_forward(self, message, source_chat_id, target_group_id, topic_id, target_entity):
        """Retry forwarding a message after a flood wait"""
        try:
            if topic_id:
                logger.info(f"[RETRY] Retrying forward to topic {topic_id} in {target_entity.title}")
                # FIXED: Use 'id' instead of 'msg_ids'
                result = await self.client(ForwardMessagesRequest(
                    from_peer=await self.client.get_input_entity(source_chat_id),
                    id=[message.id],  # FIXED: Changed from msg_ids to id
                    to_peer=await self.client.get_input_entity(target_group_id),
                    reply_to_msg_id=topic_id,
                    random_id=[self.generate_random_id()],
                    drop_author=False,
                    drop_media_captions=False
                ))
            else:
                logger.info(f"[RETRY] Retrying forward to general chat in {target_entity.title}")
                result = await self.client.forward_messages(
                    target_group_id,
                    message,
                    from_peer=source_chat_id
                )
            
            self.forwarded_count += 1
            topic_info = f" to topic {topic_id}" if topic_id else " to general chat"
            logger.info(f"[RETRY_SUCCESS] Message forwarded successfully after retry:")
            logger.info(f"   To: {target_entity.title}{topic_info} (Group ID: {target_group_id})")
            logger.info(f"   Total forwarded: {self.forwarded_count}")
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"[RETRY_FAIL] Retry forward failed: {e}")
    
    async def run(self):
        """Main run method"""
        await self.start()
        logger.info("[RUN] Telegram forwarder is running. Press Ctrl+C to stop.")
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("[STOP] Shutting down...")
        finally:
            logger.info(f"[STATS] Final stats - Forwarded: {self.forwarded_count}, Translated: {self.translation_count}, Errors: {self.error_count}")

# Main execution
async def main():
    forwarder = TelegramForwarder()
    await forwarder.run()

if __name__ == "__main__":
    asyncio.run(main())
