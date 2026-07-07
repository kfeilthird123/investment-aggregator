import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "kfeitler04@icloud.com")

# API Keys
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

# Scheduler
DAILY_RUN_TIME = os.getenv("DAILY_RUN_TIME", "08:00")
TIMEZONE = os.getenv("TIMEZONE", "America/New_York")

# Investors and Funds to Track
INVESTORS = {
    "Maverick Capital": {
        "ticker": "MAVK",
        "founder": "Mark Spiegel",
        "focus": "Value investing, short selling",
        "13f_cik": "0001018015",
        "website": "https://maverickcapital.com",
    },
    "Tiger Global": {
        "founder": "Chase Coleman",
        "focus": "Global investing, emerging markets",
        "13f_cik": "0001456797",
        "website": "https://tigerglobal.com",
    },
    "Surgo Capital": {
        "founder": "Surgo Capital",
        "focus": "Value and growth investing",
        "website": "https://surgocapital.com",
    },
    "Ruane Cunniff": {
        "founder": "Ruane Cunniff",
        "focus": "Value investing",
        "13f_cik": "0001109822",
        "website": "https://ruanecunniff.com",
    },
    "Gardner Russo": {
        "founder": "Bill Ackman",
        "focus": "Activist investing",
        "website": "https://gardnerrusso.com",
    },
    "Quinn Davis Funds": {
        "founder": "Quinn Davis",
        "focus": "Small cap value investing",
        "website": "https://quinnlavis.com",
    },
    "Lone Pine Capital": {
        "founder": "Stephen Mandel",
        "focus": "Growth and value investing",
        "13f_cik": "0001046951",
        "website": "https://lonepine.com",
    },
    "Bill Ackman": {
        "fund": "Pershing Square",
        "focus": "Activist investing, concentrated portfolio",
        "13f_cik": "0001026948",
        "website": "https://pershing.com",
    },
    "Tom Russo": {
        "fund": "Gardner Russo & Quinn",
        "focus": "Value investing",
        "13f_cik": "0001109822",
        "website": "https://grqfunds.com",
    },
    "Gavin Baker": {
        "fund": "Atreides Management",
        "focus": "Technology and healthcare",
        "13f_cik": "0001620207",
        "website": "https://atreides.com",
    },
    "Abramas Bison": {
        "focus": "Value investing",
        "website": "https://abrasasbison.com",
    },
    "Giverny Capital": {
        "founder": "Giverny Capital",
        "focus": "European value investing",
        "13f_cik": "0001622254",
        "website": "https://givernycapital.com",
    },
    "David Poppe": {
        "fund": "Poppe Capital",
        "focus": "Value investing",
        "website": "https://poppecapital.com",
    },
}

# SEC EDGAR Configuration
SEC_BASE_URL = "https://www.sec.gov"
SEC_CIKS_URL = f"{SEC_BASE_URL}/cgi-bin/browse-edgar"
SEC_13F_URL = f"{SEC_BASE_URL}/cgi-bin/browse-edgar?action=getcompany&CIK={{cik}}&type=13F&dateb=&owner=exclude&count=100"

# PDF Configuration
PDF_TITLE = "Daily Investment Report"
PDF_AUTHOR = "Investment Aggregator"
PDF_PAGE_WIDTH = 8.5
PDF_PAGE_HEIGHT = 11

# Data Retention
DATA_RETENTION_DAYS = 30
ARCHIVE_DIR = "archives"
