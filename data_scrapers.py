import requests
import feedparser
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import logging
from config import *
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvestorDataScraper:
    """Scrapes data from multiple sources for tracked investors"""

    def __init__(self):
        self.data = {}
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": SEC_USER_AGENT
        })

    def scrape_shareholder_letters(self, investor_name):
        """Scrape shareholder letters from investor websites"""
        try:
            logger.info(f"Scraping shareholder letters for {investor_name}")
            investor = INVESTORS.get(investor_name)
            if not investor or "website" not in investor:
                return []

            website = investor["website"]
            response = self.session.get(website, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            letters = []
            # Look for links containing "letter", "shareholder", "annual report"
            for link in soup.find_all('a', href=True):
                text = link.get_text().lower()
                href = link['href']
                if any(keyword in text for keyword in ['letter', 'shareholder', 'annual', 'report']):
                    letters.append({
                        "title": link.get_text(),
                        "url": href,
                        "date": datetime.now().isoformat(),
                        "source": investor_name
                    })
            return letters
        except Exception as e:
            logger.error(f"Error scraping shareholder letters for {investor_name}: {e}")
            return []

    def scrape_13f_filings(self, investor_name):
        """Scrape 13F filings from SEC EDGAR"""
        try:
            logger.info(f"Scraping 13F filings for {investor_name}")
            investor = INVESTORS.get(investor_name)
            if not investor or "13f_cik" not in investor:
                return []

            cik = investor["13f_cik"]
            url = SEC_13F_URL.format(cik=cik)
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            filings = []
            for row in soup.find_all('tr')[1:]:  # Skip header
                cols = row.find_all('td')
                if len(cols) >= 4:
                    filing_date = cols[3].get_text().strip()
                    filing_link = cols[1].find('a')
                    if filing_link:
                        filings.append({
                            "date": filing_date,
                            "url": SEC_BASE_URL + filing_link['href'],
                            "cik": cik,
                            "investor": investor_name,
                            "type": "13F"
                        })
            return filings[:5]  # Return last 5 filings
        except Exception as e:
            logger.error(f"Error scraping 13F filings for {investor_name}: {e}")
            return []

    def scrape_news_articles(self, investor_name):
        """Scrape news articles about investor"""
        try:
            logger.info(f"Scraping news for {investor_name}")
            # Using a news RSS feed approach (requires NEWS_API_KEY for full functionality)
            
            search_terms = [investor_name, investor_name.replace(" ", "-").lower()]
            articles = []

            for term in search_terms:
                # Popular financial news feeds
                feeds = [
                    "https://feeds.bloomberg.com/markets/news.rss",
                    "https://feeds.cnbc.com/cnbc/world/",
                    "https://feeds.marketwatch.com/marketwatch/topstories/",
                    "https://feeds.reuters.com/finance/markets",
                ]

                for feed_url in feeds:
                    try:
                        feed = feedparser.parse(feed_url)
                        for entry in feed.entries[:10]:
                            if term.lower() in entry.title.lower() or term.lower() in entry.get('summary', '').lower():
                                articles.append({
                                    "title": entry.title,
                                    "link": entry.link,
                                    "published": entry.get('published', datetime.now().isoformat()),
                                    "summary": entry.get('summary', '')[:200],
                                    "source": feed.feed.get('title', 'News'),
                                    "investor": investor_name
                                })
                    except Exception as e:
                        logger.debug(f"Error parsing feed {feed_url}: {e}")
                        continue

            return articles[:10]  # Return top 10 articles
        except Exception as e:
            logger.error(f"Error scraping news for {investor_name}: {e}")
            return []

    def scrape_youtube_videos(self, investor_name):
        """Scrape YouTube videos (requires API key)"""
        try:
            logger.info(f"Scraping YouTube videos for {investor_name}")
            if not YOUTUBE_API_KEY:
                logger.warning("YouTube API key not configured")
                return []

            # YouTube search would go here
            # This is a placeholder for when API is configured
            videos = []
            return videos
        except Exception as e:
            logger.error(f"Error scraping YouTube for {investor_name}: {e}")
            return []

    def scrape_podcasts(self, investor_name):
        """Scrape podcast mentions"""
        try:
            logger.info(f"Scraping podcasts for {investor_name}")
            # Popular investment podcast feeds
            podcasts = []
            
            podcast_feeds = {
                "Masters in Business": "https://feeds.bloomberg.com/podcast/masters-in-business.xml",
                "We Study Billionaires": "https://feeds.podcastaddict.com/we-study-billionaires",
                "Investor's Podcast Network": "https://feeds.podcastaddict.com/investors",
            }

            for podcast_name, feed_url in podcast_feeds.items():
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:5]:
                        if investor_name.lower() in entry.title.lower():
                            podcasts.append({
                                "title": entry.title,
                                "podcast": podcast_name,
                                "link": entry.link,
                                "published": entry.get('published', datetime.now().isoformat()),
                                "summary": entry.get('summary', '')[:200],
                                "investor": investor_name
                            })
                except Exception as e:
                    logger.debug(f"Error parsing podcast feed {podcast_name}: {e}")
                    continue

            return podcasts
        except Exception as e:
            logger.error(f"Error scraping podcasts for {investor_name}: {e}")
            return []

    def get_portfolio_holdings(self, investor_name):
        """Get current portfolio holdings (from latest 13F)"""
        try:
            logger.info(f"Fetching portfolio holdings for {investor_name}")
            investor = INVESTORS.get(investor_name)
            if not investor or "13f_cik" not in investor:
                return {"holdings": [], "last_update": None}

            cik = investor["13f_cik"]
            # This would parse the actual 13F XML to get holdings
            # Placeholder implementation
            holdings = {
                "holdings": [],
                "last_update": datetime.now().isoformat(),
                "total_value": "N/A"
            }
            return holdings
        except Exception as e:
            logger.error(f"Error fetching portfolio for {investor_name}: {e}")
            return {"holdings": [], "last_update": None}

    def get_market_data(self):
        """Get current market data and relevant indices"""
        try:
            logger.info("Fetching market data")
            import yfinance as yf

            indices = ["^GSPC", "^IXIC", "^DJI", "^VIX", "^TNX"]
            market_data = {}

            for ticker in indices:
                try:
                    data = yf.Ticker(ticker)
                    hist = data.history(period="5d")
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        market_data[ticker] = {
                            "price": latest['Close'],
                            "change": ((latest['Close'] - hist.iloc[0]['Close']) / hist.iloc[0]['Close']) * 100,
                            "timestamp": datetime.now().isoformat()
                        }
                except Exception as e:
                    logger.debug(f"Error fetching {ticker}: {e}")
                    continue

            return market_data
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return {}

    def scrape_all_data(self, investor_name):
        """Scrape all available data for an investor"""
        logger.info(f"Starting data collection for {investor_name}")
        
        investor_data = {
            "investor": investor_name,
            "timestamp": datetime.now().isoformat(),
            "shareholder_letters": self.scrape_shareholder_letters(investor_name),
            "13f_filings": self.scrape_13f_filings(investor_name),
            "news_articles": self.scrape_news_articles(investor_name),
            "youtube_videos": self.scrape_youtube_videos(investor_name),
            "podcasts": self.scrape_podcasts(investor_name),
            "portfolio": self.get_portfolio_holdings(investor_name),
        }
        
        return investor_data

    def collect_all_investors_data(self):
        """Collect data for all tracked investors"""
        all_data = {
            "market": self.get_market_data(),
            "investors": {}
        }

        for investor_name in INVESTORS.keys():
            try:
                all_data["investors"][investor_name] = self.scrape_all_data(investor_name)
            except Exception as e:
                logger.error(f"Error collecting data for {investor_name}: {e}")
                continue

        return all_data


if __name__ == "__main__":
    scraper = InvestorDataScraper()
    data = scraper.collect_all_investors_data()
    print(json.dumps(data, indent=2, default=str))
