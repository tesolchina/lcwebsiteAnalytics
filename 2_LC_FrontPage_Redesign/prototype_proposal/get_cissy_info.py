#!/usr/bin/env python3
"""
LC Conference Page Crawler - Get Cissy's Photo and Info
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re

def crawl_conference_page():
    """Crawl the LC conference page to get Cissy's photo and information"""
    url = "https://lc.hkbu.edu.hk/main/lconference/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save raw HTML for reference
        output_dir = "/Users/simonwang/Documents/GitHub/lcwebsiteAnalytics/prototype_proposal"
        html_file = os.path.join(output_dir, "conference_page.html")
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✅ Conference page saved: {html_file}")
        
        # Look for Cissy's information
        cissy_info = find_cissy_info(soup, url)
        
        # Save findings
        info_file = os.path.join(output_dir, "cissy_info.txt")
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write("LC Head Information Found:\n")
            f.write("=" * 40 + "\n\n")
            for key, value in cissy_info.items():
                f.write(f"{key}: {value}\n")
        
        print(f"✅ Cissy info extracted: {info_file}")
        return cissy_info
        
    except Exception as e:
        print(f"❌ Error crawling conference page: {e}")
        return {}

def find_cissy_info(soup, base_url):
    """Find Cissy's photo and information"""
    info = {}
    
    # Look for images that might be Cissy's photo
    images = soup.find_all('img')
    cissy_images = []
    
    for img in images:
        alt_text = img.get('alt', '').lower()
        src = img.get('src', '')
        
        # Look for images with Cissy-related alt text or file names
        if any(keyword in alt_text for keyword in ['cissy', 'li', 'director', 'head']):
            full_url = urljoin(base_url, src)
            cissy_images.append({
                'src': full_url,
                'alt': alt_text,
                'title': img.get('title', '')
            })
    
    info['potential_photos'] = cissy_images
    
    # Look for text mentioning Cissy or LC Head
    text_content = soup.get_text()
    cissy_mentions = []
    
    # Split into paragraphs and look for relevant ones
    paragraphs = soup.find_all(['p', 'div', 'span'])
    for p in paragraphs:
        text = p.get_text().strip()
        if any(keyword.lower() in text.lower() for keyword in ['Cissy', 'Li', 'Director', 'Head of Language']):
            cissy_mentions.append(text)
    
    info['text_mentions'] = cissy_mentions[:5]  # Limit to first 5 matches
    
    # Look for staff or leadership sections
    leadership_sections = soup.find_all(['div', 'section'], class_=re.compile(r'staff|team|leadership|director', re.I))
    info['leadership_sections'] = len(leadership_sections)
    
    return info

if __name__ == "__main__":
    print("🕷️ Crawling LC Conference page for Cissy's information...")
    cissy_info = crawl_conference_page()
    print("\n📋 Information extracted:")
    for key, value in cissy_info.items():
        print(f"   {key}: {value}")
