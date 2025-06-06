import re
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class MessageProcessor:
    """Class to extract and format important information from messages"""
    
    def __init__(self):
        # Patterns for bonus codes
        self.bonus_code_patterns = [
            r'(?:code|bonus|promo)[\s:]*([A-Z0-9]{3,15})',
            r'(?:use|enter|claim)[\s:]*([A-Z0-9]{3,15})',
            r'\b([A-Z0-9]{4,12})\b(?=.*(?:bonus|code|promo|free))',
            r'🎁[\s]*([A-Z0-9]{3,15})',
            r'💰[\s]*([A-Z0-9]{3,15})',
            r'(?:^|\s)([A-Z]{2,4}[0-9]{2,8})(?=\s|$)',
        ]
        
        # Patterns for wager requirements
        self.wager_patterns = [
            r'(\d+x?\s*(?:wager|wagering|rollover|playthrough))',
            r'(?:wager|wagering|rollover|playthrough)[\s:]*(\d+x?)',
            r'(\d+x?\s*(?:times|×)?\s*(?:wager|wagering))',
            r'(?:must\s+(?:wager|bet))[\s:]*(\d+x?)',
            r'(\d+%?\s*(?:wagering\s+requirement|wager\s+req))',
        ]
        
        # Patterns for redeem/claim links
        self.link_patterns = [
            r'(https?://[^\s]+)',
            r'(?:link|redeem|claim|visit)[\s:]*([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/?[^\s]*)',
        ]
        
        # Patterns for monetary values
        self.money_patterns = [
            r'(\$\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?\s*(?:USD|usd|\$))',
            r'(€\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?\s*(?:EUR|eur|€))',
        ]
        
        # Keywords that indicate important bonus information
        self.important_keywords = [
            'free', 'bonus', 'code', 'promo', 'spins', 'deposit', 'no deposit',
            'welcome', 'reload', 'cashback', 'match', 'exclusive', 'limited',
            'expires', 'valid', 'claim', 'redeem', 'wager', 'wagering'
        ]
    
    def extract_bonus_info(self, text: str) -> Dict[str, List[str]]:
        """Extract bonus codes, wager requirements, and links from text"""
        if not text:
            return {'codes': [], 'wager': [], 'links': [], 'money': []}
        
        text_upper = text.upper()
        
        # Extract bonus codes
        codes = []
        for pattern in self.bonus_code_patterns:
            matches = re.findall(pattern, text_upper, re.IGNORECASE)
            codes.extend([match.strip() for match in matches if len(match.strip()) >= 3])
        
        # Extract wager requirements
        wager = []
        for pattern in self.wager_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            wager.extend([match.strip() for match in matches])
        
        # Extract links
        links = []
        for pattern in self.link_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            links.extend([match.strip() for match in matches])
        
        # Extract monetary values
        money = []
        for pattern in self.money_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            money.extend([match.strip() for match in matches])
        
        # Remove duplicates while preserving order
        codes = list(dict.fromkeys(codes))
        wager = list(dict.fromkeys(wager))
        links = list(dict.fromkeys(links))
        money = list(dict.fromkeys(money))
        
        return {
            'codes': codes,
            'wager': wager,
            'links': links,
            'money': money
        }
    
    def format_extracted_info(self, extracted_info: Dict[str, List[str]], source_name: str = "") -> Optional[str]:
        """Format the extracted information into a clean message"""
        codes = extracted_info['codes']
        wager = extracted_info['wager']
        links = extracted_info['links']
        money = extracted_info['money']
        
        # If no important info found, return None
        if not codes and not wager and not links and not money:
            return None
        
        # Build formatted message
        formatted_parts = []
        
        # Add source if provided
        if source_name:
            formatted_parts.append(f"🎰 **{source_name}**")
            formatted_parts.append("")
        
        # Add bonus codes
        if codes:
            formatted_parts.append("🎁 **Bonus Code(s):**")
            for code in codes[:3]:  # Limit to 3 codes to avoid spam
                formatted_parts.append(f"   `{code}`")
            formatted_parts.append("")
        
        # Add monetary values
        if money:
            formatted_parts.append("💰 **Amount:**")
            for amount in money[:2]:  # Limit to 2 amounts
                formatted_parts.append(f"   {amount}")
            formatted_parts.append("")
        
        # Add wager requirements
        if wager:
            formatted_parts.append("📊 **Wager Requirement:**")
            for req in wager[:2]:  # Limit to 2 requirements
                formatted_parts.append(f"   {req}")
            formatted_parts.append("")
        
        # Add links
        if links:
            formatted_parts.append("🔗 **Redeem Link(s):**")
            for link in links[:2]:  # Limit to 2 links
                # Clean up the link
                clean_link = link if link.startswith('http') else f"https://{link}"
                formatted_parts.append(f"   {clean_link}")
        
        # Join all parts
        result = "\n".join(formatted_parts).strip()
        
        # Add separator for readability
        result += "\n" + "─" * 30
        
        return result if result.replace("─", "").strip() else None
    
    def should_forward_message(self, text: str) -> bool:
        """Determine if a message contains bonus-related content worth forwarding"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Check for important keywords
        keyword_count = sum(1 for keyword in self.important_keywords if keyword in text_lower)
        
        # Check for potential bonus codes (alphanumeric strings)
        code_matches = len(re.findall(r'\b[A-Z0-9]{4,12}\b', text.upper()))
        
        # Check for links
        has_links = bool(re.search(r'https?://[^\s]+', text))
        
        # Check for monetary values
        has_money = bool(re.search(r'[\$€]\d+|\d+\s*(?:USD|EUR|usd|eur)', text))
        
        # Forward if it has multiple indicators of bonus content
        return (keyword_count >= 2) or (code_matches >= 1 and keyword_count >= 1) or has_links or has_money
    
    def clean_and_extract(self, original_text: str, source_name: str = "") -> Optional[str]:
        """Main method to clean message and extract important info"""
        if not self.should_forward_message(original_text):
            logger.info(f"[FILTER] Message filtered out - no bonus content detected")
            return None
        
        extracted_info = self.extract_bonus_info(original_text)
        formatted_message = self.format_extracted_info(extracted_info, source_name)
        
        if formatted_message:
            logger.info(f"[EXTRACT] Successfully extracted bonus info:")
            logger.info(f"   Codes: {len(extracted_info['codes'])}")
            logger.info(f"   Wager: {len(extracted_info['wager'])}")
            logger.info(f"   Links: {len(extracted_info['links'])}")
            logger.info(f"   Money: {len(extracted_info['money'])}")
        
        return formatted_message
