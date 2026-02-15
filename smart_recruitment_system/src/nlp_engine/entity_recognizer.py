"""
Entity Recognizer - Extract contact information and personal details
"""
import re

class EntityRecognizer:
    def __init__(self):
        # Enhanced regex patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        self.phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}'
        self.linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+/?'
        self.github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+/?'
    
    def extract_entities(self, text):
        """Extract all entities from resume text"""
        return {
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'linkedin': self._extract_linkedin(text),
            'github': self._extract_github(text),
            'location': self._extract_location(text)
        }
    
    def _extract_name(self, text):
        """Extract candidate name from first few lines"""
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        
        for line in lines[:5]:
            # Name heuristics: 2-4 words, no digits, reasonable length
            words = line.split()
            if 2 <= len(words) <= 4 and len(line) <= 50:
                if not any(char.isdigit() for char in line):
                    # Avoid common headers
                    if not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum']):
                        return line.title()
        return None
    
    def _extract_email(self, text):
        """Extract email address"""
        matches = re.findall(self.email_pattern, text)
        # Return first valid email
        for email in matches:
            if '@' in email and '.' in email.split('@')[1]:
                return email.lower()
        return None
    
    def _extract_phone(self, text):
        """Extract phone number"""
        matches = re.findall(self.phone_pattern, text)
        if matches:
            # Clean and format phone number
            phone = re.sub(r'[^0-9+]', '', matches[0])
            return phone if len(phone) >= 10 else None
        return None
    
    def _extract_linkedin(self, text):
        """Extract LinkedIn profile URL"""
        matches = re.findall(self.linkedin_pattern, text, re.IGNORECASE)
        if matches:
            url = matches[0]
            if not url.startswith('http'):
                url = 'https://' + url
            return url.rstrip('/')
        return None
    
    def _extract_github(self, text):
        """Extract GitHub profile URL"""
        matches = re.findall(self.github_pattern, text, re.IGNORECASE)
        if matches:
            url = matches[0]
            if not url.startswith('http'):
                url = 'https://' + url
            return url.rstrip('/')
        return None
    
    def _extract_location(self, text):
        """Extract location/address"""
        # Simple location pattern (City, State/Country)
        location_pattern = r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*([A-Z]{2}|[A-Z][a-z]+)\b'
        matches = re.findall(location_pattern, text)
        return f"{matches[0][0]}, {matches[0][1]}" if matches else None
