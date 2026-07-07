# Investment Aggregator

A comprehensive Python-based system that aggregates investment data from multiple sources (SEC filings, shareholder letters, news articles, podcasts, and YouTube videos) for prominent value investors and investment funds, generating daily PDF reports sent to your email.

## Features

✅ **Multi-Source Data Aggregation:**
- SEC 13F filings from EDGAR
- Shareholder letters and annual reports
- Financial news articles from major outlets
- Podcast mentions and interviews
- YouTube video tracking
- Real-time market data and indices

✅ **Tracked Investors & Funds:**
- Maverick Capital
- Tiger Global
- Surgo Capital
- Ruane Cunniff
- Gardner Russo
- Quinn Davis Funds
- Lone Pine Capital
- Bill Ackman (Pershing Square)
- Tom Russo (Gardner Russo & Quinn)
- Gavin Baker (Atreides Management)
- Abramas Bison
- Giverny Capital
- David Poppe

✅ **Professional Reports:**
- Beautiful PDF formatting with company branding
- Market overview with key indices
- Individual investor sections with key metrics
- Investment themes and market commentary
- Portfolio holdings summaries
- Chronological organization of all information

✅ **Daily Automation:**
- Scheduled daily execution at specified time
- Automatic email delivery to your inbox
- Archive management with configurable retention
- Error notifications and logging

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Gmail account with app password (for email sending)

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/investment-aggregator.git
cd investment-aggregator
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
```

5. **Edit `.env` with your settings:**

```
# Email Configuration (Gmail)
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password  # Use app-specific password, not your Gmail password
RECIPIENT_EMAIL=kfeitler04@icloud.com

# API Keys (optional - for enhanced functionality)
NEWS_API_KEY=your_news_api_key
YOUTUBE_API_KEY=your_youtube_api_key

# Schedule Settings
DAILY_RUN_TIME=08:00  # 8 AM in your timezone
TIMEZONE=America/New_York
```

### Gmail App Password Setup

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication if not already enabled
3. Go to "App passwords" (at bottom of security page)
4. Select "Mail" and "Windows Computer" (or your device)
5. Generate a 16-character password
6. Copy this into `EMAIL_PASSWORD` in your `.env` file

## Usage

### Run Once (Testing)
```bash
python main.py --once
```

### Start Scheduler (Continuous Mode)
```bash
python main.py
```

This will:
1. Start the scheduler
2. Run the first report immediately
3. Schedule subsequent reports for the specified time each day
4. Keep running in the background

### Manual Report Generation
```python
from data_scrapers import InvestorDataScraper
from pdf_generator import InvestmentReportGenerator
from email_sender import EmailSender

# Collect data
scraper = InvestorDataScraper()
data = scraper.collect_all_investors_data()

# Generate PDF
generator = InvestmentReportGenerator("custom_report.pdf")
pdf_file = generator.generate_report(data)

# Send email
sender = EmailSender()
sender.send_report(pdf_file)
```

## File Structure

```
investment-aggregator/
├��─ config.py                 # Configuration and investor list
├── data_scrapers.py         # Data collection from all sources
├── pdf_generator.py         # PDF report creation
├── email_sender.py          # Email delivery
├── main.py                  # Orchestration and scheduling
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── investment_aggregator.log # Execution logs
├── archives/               # Archived PDF reports
└── README.md              # This file
```

## Report Contents

Each daily PDF includes:

1. **Market Overview**
   - S&P 500, Nasdaq, Dow Jones
   - VIX and Treasury yields
   - Daily changes and trends

2. **For Each Tracked Investor:**
   - Recent 13F SEC filings with dates
   - Latest shareholder letters and reports
   - Recent news mentions and commentary
   - Podcast appearances and interviews
   - Current portfolio holdings
   - Portfolio changes from previous quarter

3. **Market Analysis**
   - Key investment themes
   - Sector rotation insights
   - Valuation trends
   - Market commentary

4. **Disclaimer**
   - Important legal notice about report usage

## Configuration

### Investors
Edit the `INVESTORS` dictionary in `config.py` to add, remove, or modify tracked investors:

```python
INVESTORS = {
    "Your Investor Name": {
        "founder": "Founder Name",
        "focus": "Investment focus area",
        "13f_cik": "SEC CIK number",
        "website": "https://website.com",
    },
    # ... more investors
}
```

### Scheduling
Modify `config.py` to change:
- `DAILY_RUN_TIME`: When reports run (24-hour format)
- `TIMEZONE`: Your timezone for scheduling
- `DATA_RETENTION_DAYS`: How long to keep archived reports

## Logging

All activity is logged to `investment_aggregator.log`:

```bash
tail -f investment_aggregator.log
```

Logs include:
- Data collection status
- PDF generation details
- Email delivery confirmation
- Errors and warnings

## Troubleshooting

### Email Not Sending
- Verify Gmail app password is correct (not your regular password)
- Confirm 2FA is enabled on your Google account
- Check that "Allow less secure apps" is enabled if not using app password
- Verify email addresses in `.env`

### Missing Data
- Check that API keys are configured for optional features
- Verify SEC CIK numbers are correct for 13F filings
- Confirm internet connection
- Check logs for specific error messages

### Schedule Not Running
- Verify `DAILY_RUN_TIME` format is `HH:MM` (24-hour)
- Confirm `TIMEZONE` is correct
- Run `python main.py --once` to test manually
- Check scheduler logs

## Advanced Usage

### Custom Data Filtering
Modify `data_scrapers.py` to filter data by date range, keyword, or source.

### Custom Report Formatting
Edit `pdf_generator.py` to customize colors, layout, or sections.

### Multiple Recipients
In `email_sender.py`, modify to send to multiple emails:

```python
recipients = ["email1@example.com", "email2@example.com"]
for recipient in recipients:
    self.send_report(pdf_filename, recipient)
```

### Docker Deployment
Create a `Dockerfile` for cloud deployment:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Performance

- Data collection: ~2-5 minutes (depending on internet speed)
- PDF generation: ~30-60 seconds
- Email delivery: ~5-10 seconds
- **Total runtime**: ~3-6 minutes per report

## Roadmap

- [ ] Database storage for historical comparison
- [ ] Web dashboard for viewing reports
- [ ] Sentiment analysis on investor commentary
- [ ] Portfolio change detection and alerts
- [ ] Integration with trading platforms
- [ ] Custom filters and preferences
- [ ] Slack/Teams notifications
- [ ] Mobile app for report viewing

## Legal Disclaimer

This tool aggregates publicly available information for educational and research purposes. It is NOT investment advice. All information is provided "as-is" without warranty. Users are responsible for verifying all information and consulting with financial advisors before making investment decisions.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review logs in `investment_aggregator.log`

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

**Made with ❤️ for value investors and investment research enthusiasts**
