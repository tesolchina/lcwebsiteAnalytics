#!/usr/bin/env python3
"""
LC Website Front Page Crawler & Analyzer
Crawls https://lc.hkbu.edu.hk/main/ and analyzes the WordPress-generated structure
"""

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse
import time

class LCWebsiteCrawler:
    def __init__(self, base_url="https://lc.hkbu.edu.hk/main/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.output_dir = "/Users/simonwang/Documents/GitHub/lcwebsiteAnalytics/LCmain"
        self.analysis_data = {}
        
    def crawl_main_page(self):
        """Crawl the main LC website front page"""
        print(f"🕷️  Crawling LC main page: {self.base_url}")
        
        try:
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            # Save raw HTML
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            html_file = os.path.join(self.output_dir, f"lc_main_page_{timestamp}.html")
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"✅ Raw HTML saved: {html_file}")
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Analyze the structure
            self.analyze_page_structure(soup, timestamp)
            
            # Extract specific elements
            self.extract_navigation(soup)
            self.extract_content_sections(soup)
            self.extract_wordpress_info(soup)
            self.identify_issues(soup)
            
            # Save analysis report
            self.save_analysis_report(timestamp)
            
            return True
            
        except requests.RequestException as e:
            print(f"❌ Error crawling website: {e}")
            return False
            
    def analyze_page_structure(self, soup, timestamp):
        """Analyze the overall page structure"""
        print("🔍 Analyzing page structure...")
        
        self.analysis_data['crawl_info'] = {
            'timestamp': timestamp,
            'url': self.base_url,
            'title': soup.title.string if soup.title else "No title found"
        }
        
        # Basic structure analysis
        structure = {
            'total_elements': len(soup.find_all()),
            'div_count': len(soup.find_all('div')),
            'nav_elements': len(soup.find_all(['nav', 'menu'])),
            'header_elements': len(soup.find_all(['header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
            'link_count': len(soup.find_all('a')),
            'image_count': len(soup.find_all('img')),
            'form_count': len(soup.find_all('form')),
            'script_count': len(soup.find_all('script')),
            'style_count': len(soup.find_all('style'))
        }
        
        self.analysis_data['structure'] = structure
        print(f"   📊 Found {structure['total_elements']} total elements")
        
    def extract_navigation(self, soup):
        """Extract navigation structure"""
        print("🧭 Extracting navigation...")
        
        navigation = {
            'main_nav': [],
            'top_bar': [],
            'footer_nav': [],
            'breadcrumbs': []
        }
        
        # Look for common navigation patterns
        nav_elements = soup.find_all(['nav', 'ul', 'ol'], class_=re.compile(r'nav|menu', re.I))
        
        for nav in nav_elements:
            nav_info = {
                'tag': nav.name,
                'classes': nav.get('class', []),
                'id': nav.get('id', ''),
                'links': []
            }
            
            # Extract links from this navigation
            for link in nav.find_all('a'):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                nav_info['links'].append({
                    'text': text,
                    'href': href,
                    'is_external': not href.startswith('/') and not href.startswith('#') and 'hkbu.edu.hk' not in href
                })
            
            navigation['main_nav'].append(nav_info)
        
        # Look for top bar (like the 2024 Conference link)
        top_elements = soup.find_all(['div', 'header'], class_=re.compile(r'top|bar|header', re.I))
        for top in top_elements:
            links = []
            for link in top.find_all('a'):
                links.append({
                    'text': link.get_text(strip=True),
                    'href': link.get('href', ''),
                    'classes': link.get('class', [])
                })
            if links:
                navigation['top_bar'].append({
                    'element': str(top)[:200] + "..." if len(str(top)) > 200 else str(top),
                    'links': links
                })
        
        self.analysis_data['navigation'] = navigation
        print(f"   🔗 Found {len(navigation['main_nav'])} navigation sections")
        
    def extract_content_sections(self, soup):
        """Extract main content sections"""
        print("📄 Extracting content sections...")
        
        sections = []
        
        # Look for main content areas
        main_content = soup.find(['main', 'div'], class_=re.compile(r'content|main', re.I))
        if not main_content:
            main_content = soup.find('body')
            
        # Extract sections
        for section in main_content.find_all(['section', 'div'], class_=True):
            section_info = {
                'tag': section.name,
                'classes': section.get('class', []),
                'id': section.get('id', ''),
                'text_content': section.get_text(strip=True)[:200] + "..." if len(section.get_text(strip=True)) > 200 else section.get_text(strip=True),
                'child_count': len(section.find_all()),
                'has_images': len(section.find_all('img')) > 0,
                'has_links': len(section.find_all('a')) > 0
            }
            sections.append(section_info)
        
        self.analysis_data['content_sections'] = sections
        print(f"   📋 Found {len(sections)} content sections")
        
    def extract_wordpress_info(self, soup):
        """Extract WordPress-specific information"""
        print("🔧 Extracting WordPress info...")
        
        wp_info = {
            'is_wordpress': False,
            'theme': 'Unknown',
            'plugins': [],
            'wp_version': 'Unknown'
        }
        
        # Check for WordPress indicators
        wp_indicators = [
            soup.find('meta', attrs={'name': 'generator', 'content': re.compile(r'WordPress', re.I)}),
            soup.find('link', href=re.compile(r'wp-content', re.I)),
            soup.find('script', src=re.compile(r'wp-content', re.I))
        ]
        
        if any(wp_indicators):
            wp_info['is_wordpress'] = True
            
            # Try to extract theme info
            theme_links = soup.find_all('link', href=re.compile(r'wp-content/themes', re.I))
            if theme_links:
                theme_path = theme_links[0].get('href', '')
                theme_match = re.search(r'themes/([^/]+)', theme_path)
                if theme_match:
                    wp_info['theme'] = theme_match.group(1)
        
        self.analysis_data['wordpress_info'] = wp_info
        print(f"   🔧 WordPress detected: {wp_info['is_wordpress']}")
        
    def identify_issues(self, soup):
        """Identify potential issues with the current site"""
        print("🚨 Identifying issues...")
        
        issues = []
        
        # Check for 2024 conference link
        conference_links = soup.find_all('a', href=re.compile(r'conference|lconference', re.I))
        if conference_links:
            issues.append({
                'type': 'Outdated Content',
                'severity': 'Medium',
                'issue': f'Found {len(conference_links)} links to 2024 conference',
                'details': [link.get('href') for link in conference_links],
                'recommendation': 'Remove outdated conference links'
            })
        
        # Check for excessive divs (potential over-nesting)
        div_count = len(soup.find_all('div'))
        if div_count > 100:
            issues.append({
                'type': 'Structure',
                'severity': 'Low',
                'issue': f'Excessive div count: {div_count}',
                'recommendation': 'Consider simplifying HTML structure'
            })
        
        # Check for missing alt tags
        images_without_alt = soup.find_all('img', alt=lambda x: not x or x.strip() == '')
        if images_without_alt:
            issues.append({
                'type': 'Accessibility',
                'severity': 'Medium',
                'issue': f'{len(images_without_alt)} images missing alt text',
                'recommendation': 'Add descriptive alt text to all images'
            })
        
        # Check for inline styles (maintainability issue)
        inline_styles = soup.find_all(style=True)
        if len(inline_styles) > 10:
            issues.append({
                'type': 'Maintainability',
                'severity': 'Low',
                'issue': f'{len(inline_styles)} elements with inline styles',
                'recommendation': 'Move inline styles to CSS files'
            })
        
        self.analysis_data['issues'] = issues
        print(f"   🚨 Identified {len(issues)} potential issues")
        
    def save_analysis_report(self, timestamp):
        """Save comprehensive analysis report"""
        print("💾 Saving analysis report...")
        
        # Save JSON data
        json_file = os.path.join(self.output_dir, f"lc_analysis_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_data, f, indent=2, ensure_ascii=False)
        
        # Create human-readable report
        report_file = os.path.join(self.output_dir, f"lc_analysis_report_{timestamp}.md")
        
        report_content = f"""# LC Website Analysis Report
Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
URL: {self.base_url}

## Summary
- **Page Title:** {self.analysis_data['crawl_info']['title']}
- **Total Elements:** {self.analysis_data['structure']['total_elements']:,}
- **WordPress Site:** {self.analysis_data['wordpress_info']['is_wordpress']}
- **Issues Found:** {len(self.analysis_data['issues'])}

## Structure Analysis
- **Div Elements:** {self.analysis_data['structure']['div_count']:,}
- **Navigation Elements:** {self.analysis_data['structure']['nav_elements']}
- **Links:** {self.analysis_data['structure']['link_count']:,}
- **Images:** {self.analysis_data['structure']['image_count']:,}
- **Scripts:** {self.analysis_data['structure']['script_count']:,}

## Navigation Analysis
Found {len(self.analysis_data['navigation']['main_nav'])} navigation sections:
"""
        
        # Add navigation details
        for i, nav in enumerate(self.analysis_data['navigation']['main_nav']):
            report_content += f"\n### Navigation Section {i+1}\n"
            report_content += f"- **Type:** {nav['tag']}\n"
            report_content += f"- **Classes:** {', '.join(nav['classes'])}\n"
            report_content += f"- **Links:** {len(nav['links'])}\n"
            
            if nav['links']:
                report_content += "\n**Links found:**\n"
                for link in nav['links'][:10]:  # Show first 10 links
                    report_content += f"- [{link['text']}]({link['href']})\n"
                if len(nav['links']) > 10:
                    report_content += f"- ... and {len(nav['links']) - 10} more links\n"
        
        # Add top bar analysis
        if self.analysis_data['navigation']['top_bar']:
            report_content += "\n## Top Bar Analysis\n"
            for bar in self.analysis_data['navigation']['top_bar']:
                report_content += f"Found top bar with {len(bar['links'])} links:\n"
                for link in bar['links']:
                    report_content += f"- [{link['text']}]({link['href']})\n"
        
        # Add issues
        if self.analysis_data['issues']:
            report_content += "\n## Issues Identified\n"
            for issue in self.analysis_data['issues']:
                report_content += f"\n### {issue['type']} - {issue['severity']} Priority\n"
                report_content += f"**Issue:** {issue['issue']}\n"
                report_content += f"**Recommendation:** {issue['recommendation']}\n"
                if 'details' in issue:
                    report_content += f"**Details:** {', '.join(issue['details'])}\n"
        
        # Add WordPress info
        report_content += f"\n## WordPress Information\n"
        report_content += f"- **WordPress Site:** {self.analysis_data['wordpress_info']['is_wordpress']}\n"
        report_content += f"- **Theme:** {self.analysis_data['wordpress_info']['theme']}\n"
        
        report_content += f"\n## Content Sections\n"
        report_content += f"Found {len(self.analysis_data['content_sections'])} content sections.\n"
        
        report_content += f"\n---\n*Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Analysis saved:")
        print(f"   📄 Report: {report_file}")
        print(f"   📊 Data: {json_file}")

def main():
    """Main function to run the crawler"""
    print("🚀 Starting LC Website Analysis...")
    print("=" * 60)
    
    crawler = LCWebsiteCrawler()
    
    if crawler.crawl_main_page():
        print("=" * 60)
        print("✅ Analysis completed successfully!")
        print(f"📁 Check results in: {crawler.output_dir}")
    else:
        print("❌ Analysis failed. Please check your connection and try again.")

if __name__ == "__main__":
    main()
