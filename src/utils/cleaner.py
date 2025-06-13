"""
Utility functions for cleaning and formatting GPT responses.
"""

import re
from typing import List, Optional

def clean_gpt_reply(reply: str) -> str:
    """
    Clean and format the GPT response.
    Removes static-sounding GPT filler phrases and suggestions.
    
    Args:
        reply: Raw response from GPT
        
    Returns:
        Cleaned response text
    """
    if not reply:
        return ""
        
    # Remove suggestion-style endings and filler phrases
    patterns = [
        r"(Can you elaborate.*?|Would you like more.*?|What specific aspects.*?|Would you like me to.*?|Is there anything else.*?)$",
        r"(Let me know if you need.*?|Feel free to ask.*?|I'm here to help.*?)$",
        r"(Would you like to know.*?|Do you want me to.*?|Should I.*?)$",
        r"(I hope this helps.*?|Let me know if.*?|Please let me know.*?)$"
    ]
    
    cleaned = reply
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    
    # Clean up any remaining whitespace
    cleaned = cleaned.strip()
    
    return cleaned

def format_table_response(text: str) -> Optional[str]:
    """
    Format table-like responses for better display.
    
    Args:
        text: Raw response text
        
    Returns:
        Formatted table HTML or None if not a table
    """
    if not text or "|" not in text:
        return None
        
    lines = text.split("\n")
    if len(lines) < 2:
        return None
        
    # Check if it's a markdown table
    if any("|" in line for line in lines[:2]):
        headers = lines[0].split("|")
        if len(headers) > 1:
            return text
            
    return None 