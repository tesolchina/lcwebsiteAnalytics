#!/bin/bash
# LC Website Crawler Runner Script

echo "🚀 LC Website Analysis Tool"
echo "=========================="

# Check if we're in the right directory
if [ ! -f "lc_crawler.py" ]; then
    echo "❌ Error: lc_crawler.py not found. Please run from the LCmain directory."
    exit 1
fi

# Run the crawler
echo "🕷️  Starting website crawl and analysis..."
python3 lc_crawler.py

echo ""
echo "📁 Analysis complete! Check the generated files:"
echo "   - lc_main_page_*.html (Raw HTML)"
echo "   - lc_analysis_report_*.md (Human-readable report)" 
echo "   - lc_analysis_*.json (Machine-readable data)"
echo ""
echo "💡 Use these files to prepare your front page redesign discussion!"
