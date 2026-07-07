# Setup Guide - Investment Aggregator

This guide walks you through setting up the Investment Aggregator on your system.

## Step 1: Environment Setup

### macOS / Linux

```bash
# Create project directory
mkdir investment-aggregator
cd investment-aggregator

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows

```bash
# Create project directory
mkdir investment-aggregator
cd investment-aggregator

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Gmail Configuration

### Create Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click "Security" in left menu
3. Scroll down to "How you sign in to Google"
4. Make sure 2-Step Verification is ON (enable if needed)
5. After enabling 2FA, go back to Security
6. Scroll down to "App passwords"
7. Select:
   - App: Mail
   - Device: Windows Computer (or your device type)
8. Google will show a 16-character password
9. Copy this password (you won't see it again)

### Configure .env File

1. Copy the example:
```bash
cp .env.example .env
```

2. Open `.env` in your text editor and fill in:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx    # Your 16-character app password (remove spaces if needed)
RECIPIENT_EMAIL=kfeitler04@icloud.com

# Optional API Keys
NEWS_API_KEY=
YOUTUBE_API_KEY=

DAILY_RUN_TIME=08:00
TIMEZONE=America/New_York
```

## Step 3: Test Configuration

### Run Test Email

```bash
python -c "from email_sender import EmailSender; sender = EmailSender(); sender.send_test_email()"
```

If successful, you should receive a test email at your recipient address.

### Generate Single Report

```bash
python main.py --once
```

This will:
1. Scrape all investor data
2. Generate a PDF
3. Send it to your email
4. Save to `archives/` folder

## Step 4: Schedule Daily Reports

### Option A: Run Continuously (Recommended)

```bash
python main.py
```

This will:
- Run a report immediately
- Schedule daily reports at your specified time
- Keep running in background
- Log all activity to `investment_aggregator.log`

To stop: Press `Ctrl+C`

### Option B: Use System Scheduler

#### macOS / Linux - cron

1. Open crontab:
```bash
crontab -e
```

2. Add this line (runs at 8 AM daily):
```
0 8 * * * cd /path/to/investment-aggregator && /path/to/venv/bin/python main.py --once >> cron.log 2>&1
```

3. Save and exit

#### Windows - Task Scheduler

1. Open Task Scheduler
2. Click "Create Task..."
3. General tab:
   - Name: "Investment Aggregator"
   - Description: "Daily investment report generation"
4. Triggers tab:
   - New trigger
   - Daily
   - Set time (e.g., 8:00 AM)
5. Actions tab:
   - New action
   - Program: `C:\path\to\venv\Scripts\python.exe`
   - Arguments: `main.py --once`
   - Start in: `C:\path\to\investment-aggregator`
6. Conditions tab:
   - Uncheck "Stop if on battery"
7. Settings tab:
   - Check "If task fails, restart every: 1 minute"
6. Click OK

## Step 5: Verify Installation

Check the log file:
```bash
tail -f investment_aggregator.log
```

Expected output:
```
2024-01-15 08:00:01 - __main__ - INFO - ================================================================================
2024-01-15 08:00:01 - __main__ - INFO - STARTING DAILY INVESTMENT REPORT GENERATION
2024-01-15 08:00:01 - __main__ - INFO - ================================================================================
2024-01-15 08:00:02 - data_scrapers - INFO - Fetching market data
2024-01-15 08:00:15 - data_scrapers - INFO - Starting data collection for Maverick Capital
...
2024-01-15 08:05:30 - __main__ - INFO - DAILY REPORT COMPLETED SUCCESSFULLY
```

## Common Issues & Solutions

### "ModuleNotFoundError: No module named 'requests'"
**Solution:** Make sure virtual environment is activated and dependencies installed
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### "SMTPAuthenticationError"
**Solution:** Verify Gmail app password
- Make sure you're using the 16-character **app password**, not your regular Gmail password
- Spaces in the password are normal, remove them in .env
- Confirm 2FA is enabled
- Generate a new app password if needed

### "Email not received"
**Troubleshooting steps:**
1. Check spam folder
2. Verify RECIPIENT_EMAIL is correct in .env
3. Run test email: `python -c "from email_sender import EmailSender; sender = EmailSender(); sender.send_test_email()"`
4. Check logs for errors: `tail -f investment_aggregator.log`

### "Report not generating"
**Troubleshooting steps:**
1. Run manually: `python main.py --once`
2. Check logs: `tail -f investment_aggregator.log`
3. Verify internet connection
4. Check SEC EDGAR is accessible: `curl https://www.sec.gov`
5. Verify API keys if using optional features

### "Timeout errors when scraping"
**Solutions:**
- Increase timeout in `data_scrapers.py` (default is 10 seconds)
- Check internet speed
- Run during off-peak hours (SEC servers less busy at night)
- Some sources may be temporarily unavailable

## Production Deployment

### Cloud Deployment (Recommended)

#### Heroku
1. Create Procfile:
```
worker: python main.py
```

2. Create app:
```bash
heroku create investment-aggregator
git push heroku main
```

3. Set environment variables:
```bash
heroku config:set EMAIL_ADDRESS=your@email.com
heroku config:set EMAIL_PASSWORD=xxxxx
# ... etc
```

#### AWS Lambda + CloudWatch
1. Package as ZIP with dependencies
2. Create Lambda function
3. Set CloudWatch Events to trigger daily
4. Set environment variables in Lambda

#### Google Cloud Run
1. Create Dockerfile
2. Deploy to Cloud Run
3. Set Cloud Scheduler to invoke daily

### Docker

1. Create Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

2. Build:
```bash
docker build -t investment-aggregator .
```

3. Run:
```bash
docker run -e EMAIL_ADDRESS=your@email.com \
           -e EMAIL_PASSWORD=xxxxx \
           -e RECIPIENT_EMAIL=kfeitler04@icloud.com \
           investment-aggregator
```

## Next Steps

1. ✅ Verify report generation with `python main.py --once`
2. ✅ Check your email for the test report
3. ✅ Start the scheduler: `python main.py`
4. ✅ Monitor logs: `tail -f investment_aggregator.log`
5. ✅ Customize investors in `config.py` if needed
6. ✅ Adjust report time in `.env` if needed

## Support Resources

- **Logs:** Check `investment_aggregator.log` for detailed information
- **Documentation:** See `README.md` for full documentation
- **SEC EDGAR:** https://www.sec.gov/cgi-bin/browse-edgar
- **GitHub:** Open an issue with error logs

---

**Installation Complete!** Your Investment Aggregator is now configured and ready to send daily reports to your email.
