"""
Sample PDF Generation - Creates a preview of what the daily report looks like
Run this to generate a sample PDF without needing actual data
"""

from pdf_generator import InvestmentReportGenerator
from datetime import datetime
import os

# Create sample data structure
sample_data = {
    "market": {
        "^GSPC": {
            "price": 4750.50,
            "change": 1.25,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        },
        "^IXIC": {
            "price": 14850.25,
            "change": 0.95,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        },
        "^DJI": {
            "price": 37500.75,
            "change": 0.85,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        },
        "^VIX": {
            "price": 18.50,
            "change": -2.10,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        },
        "^TNX": {
            "price": 4.25,
            "change": 0.05,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        }
    },
    "investors": {
        "Maverick Capital": {
            "founder": "Mark Spiegel",
            "focus": "Value investing, short selling",
            "13f_filings": [
                {
                    "date": "2024-01-15",
                    "url": "https://www.sec.gov/cgi-bin/browse-edgar",
                    "type": "13F-HR"
                },
                {
                    "date": "2023-10-15",
                    "url": "https://www.sec.gov/cgi-bin/browse-edgar",
                    "type": "13F-HR"
                }
            ],
            "shareholder_letters": [
                {
                    "title": "2023 Annual Letter to Investors",
                    "url": "https://maverickcapital.com/letters",
                    "date": "2024-01-10"
                },
                {
                    "title": "Q4 2023 Commentary",
                    "url": "https://maverickcapital.com/letters",
                    "date": "2023-12-31"
                }
            ],
            "news_articles": [
                {
                    "title": "Maverick Capital Increases Stake in Tech Companies Amid AI Boom",
                    "source": "Bloomberg",
                    "published": "2024-01-15",
                    "summary": "Maverick Capital has been accumulating positions in artificial intelligence and cloud computing companies, positioning for continued growth in the technology sector."
                },
                {
                    "title": "Maverick Capital's Short Positions Gain as Market Volatility Increases",
                    "source": "MarketWatch",
                    "published": "2024-01-14",
                    "summary": "The fund's defensive positioning has paid off as market uncertainty drives demand for portfolio hedging strategies."
                },
                {
                    "title": "Value Investors See Opportunity in Undervalued Healthcare Stocks",
                    "source": "Reuters",
                    "published": "2024-01-12",
                    "summary": "Maverick Capital and other value-focused funds are finding compelling valuations in the pharmaceutical and biotech sectors."
                }
            ],
            "podcasts": [
                {
                    "podcast": "Masters in Business",
                    "title": "Market Outlook 2024 with Mark Spiegel",
                    "published": "2024-01-10",
                    "link": "https://bloomberg.com/podcasts"
                },
                {
                    "podcast": "We Study Billionaires",
                    "title": "Lessons from Value Investing Legends",
                    "published": "2024-01-05",
                    "link": "https://podcastaddict.com"
                }
            ],
            "portfolio": {
                "holdings": [
                    {
                        "symbol": "AAPL",
                        "company": "Apple Inc.",
                        "shares": 2500000,
                        "value": "$412,500,000",
                        "percent_portfolio": "5.2%"
                    },
                    {
                        "symbol": "MSFT",
                        "company": "Microsoft Corporation",
                        "shares": 1800000,
                        "value": "$648,000,000",
                        "percent_portfolio": "8.1%"
                    },
                    {
                        "symbol": "GOOGL",
                        "company": "Alphabet Inc.",
                        "shares": 950000,
                        "value": "$127,475,000",
                        "percent_portfolio": "1.6%"
                    },
                    {
                        "symbol": "JPM",
                        "company": "JPMorgan Chase",
                        "shares": 3200000,
                        "value": "$512,000,000",
                        "percent_portfolio": "6.4%"
                    },
                    {
                        "symbol": "BRK.B",
                        "company": "Berkshire Hathaway",
                        "shares": 1500000,
                        "value": "$562,500,000",
                        "percent_portfolio": "7.1%"
                    }
                ],
                "last_update": "2024-01-15",
                "total_value": "$7.95B"
            }
        },
        "Tiger Global": {
            "founder": "Chase Coleman",
            "focus": "Global investing, emerging markets",
            "13f_filings": [
                {
                    "date": "2024-01-15",
                    "url": "https://www.sec.gov/cgi-bin/browse-edgar",
                    "type": "13F-HR"
                }
            ],
            "shareholder_letters": [
                {
                    "title": "Tiger Global 2023 Performance Review",
                    "url": "https://tigerglobal.com/letters",
                    "date": "2024-01-08"
                }
            ],
            "news_articles": [
                {
                    "title": "Tiger Global Doubles Down on India Tech Investments",
                    "source": "Financial Times",
                    "published": "2024-01-14",
                    "summary": "Chase Coleman's fund is increasing exposure to Indian technology companies, betting on emerging market growth."
                },
                {
                    "title": "Global Growth Fund Sees Strong Returns in Asian Markets",
                    "source": "WSJ",
                    "published": "2024-01-10",
                    "summary": "Tiger Global's emerging market strategy is delivering strong performance as Asian economies show resilience."
                }
            ],
            "podcasts": [
                {
                    "podcast": "Investor's Roundtable",
                    "title": "Global Macro Trends with Chase Coleman",
                    "published": "2024-01-08",
                    "link": "https://podcastaddict.com"
                }
            ],
            "portfolio": {
                "holdings": [
                    {
                        "symbol": "BABA",
                        "company": "Alibaba Group",
                        "shares": 5000000,
                        "value": "$425,000,000",
                        "percent_portfolio": "4.8%"
                    },
                    {
                        "symbol": "TENCENT",
                        "company": "Tencent Holdings",
                        "shares": 3200000,
                        "value": "$512,000,000",
                        "percent_portfolio": "5.8%"
                    },
                    {
                        "symbol": "INFY",
                        "company": "Infosys Limited",
                        "shares": 8500000,
                        "value": "$306,000,000",
                        "percent_portfolio": "3.5%"
                    }
                ],
                "last_update": "2024-01-15",
                "total_value": "$8.82B"
            }
        },
        "Bill Ackman (Pershing Square)": {
            "founder": "Bill Ackman",
            "focus": "Activist investing, concentrated portfolio",
            "13f_filings": [
                {
                    "date": "2024-01-15",
                    "url": "https://www.sec.gov/cgi-bin/browse-edgar",
                    "type": "13F-HR"
                }
            ],
            "shareholder_letters": [
                {
                    "title": "Pershing Square 2023 Annual Report",
                    "url": "https://pershing.com/letters",
                    "date": "2024-01-12"
                }
            ],
            "news_articles": [
                {
                    "title": "Ackman's Pershing Square Posts Strong 2023 Returns",
                    "source": "Bloomberg",
                    "published": "2024-01-16",
                    "summary": "Bill Ackman's activist fund delivered double-digit returns through concentrated positions and strategic activism."
                },
                {
                    "title": "Pershing Square Initiates Major Position in Financial Services",
                    "source": "MarketWatch",
                    "published": "2024-01-13",
                    "summary": "Ackman signals activist campaign at major financial institution, sees significant value creation opportunity."
                }
            ],
            "podcasts": [
                {
                    "podcast": "Invest Like the Best",
                    "title": "Bill Ackman on Activism and Value Creation",
                    "published": "2024-01-11",
                    "link": "https://podcastaddict.com"
                }
            ],
            "portfolio": {
                "holdings": [
                    {
                        "symbol": "UMC",
                        "company": "UnitedHealth Group",
                        "shares": 2800000,
                        "value": "$1.456B",
                        "percent_portfolio": "12.1%"
                    },
                    {
                        "symbol": "HLI",
                        "company": "Hilton Worldwide",
                        "shares": 5200000,
                        "value": "$858M",
                        "percent_portfolio": "7.1%"
                    },
                    {
                        "symbol": "PHM",
                        "company": "PulteGroup",
                        "shares": 8500000,
                        "value": "$425M",
                        "percent_portfolio": "3.5%"
                    }
                ],
                "last_update": "2024-01-15",
                "total_value": "$12.05B"
            }
        }
    }
}

if __name__ == "__main__":
    print("=" * 80)
    print("GENERATING SAMPLE INVESTMENT REPORT PDF")
    print("=" * 80)
    
    # Create PDF
    pdf_filename = "sample_investment_report.pdf"
    generator = InvestmentReportGenerator(pdf_filename)
    
    print(f"\n📄 Generating PDF: {pdf_filename}")
    generated_pdf = generator.generate_report(sample_data)
    
    print(f"✅ PDF Generated Successfully!")
    print(f"📍 Location: {os.path.abspath(generated_pdf)}")
    print(f"📊 File Size: {os.path.getsize(generated_pdf) / 1024:.2f} KB")
    print("\n" + "=" * 80)
    print("PDF REPORT CONTENTS:")
    print("=" * 80)
    print("""
✓ Market Overview
  - S&P 500, Nasdaq, Dow Jones, VIX, 10Y Treasury
  - Current prices and daily changes

✓ Investment Themes & Insights
  - Technology sector trends
  - Healthcare and biotech opportunities
  - Energy sector positioning
  - Banking and finance rotation
  - Valuation opportunities

✓ Individual Investor Sections (Maverick Capital, Tiger Global, Bill Ackman, etc.)
  - Recent 13F SEC filings
  - Shareholder letters & reports
  - News mentions and commentary
  - Podcast appearances
  - Top portfolio holdings
  - Portfolio allocation percentages

✓ Professional Formatting
  - Color-coded headers
  - Tables and structured data
  - Chronological organization
  - Easy-to-read layout

✓ Legal Disclaimer
  - Important risk acknowledgments
    """)
    print("=" * 80)
    print(f"\n📧 This is what will be emailed daily to kfeitler04@icloud.com")
    print("🕒 Configure DAILY_RUN_TIME in .env to set when it runs")
    print("=" * 80)
