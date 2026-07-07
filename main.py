import schedule
import time
import logging
from datetime import datetime
import os
from data_scrapers import InvestorDataScraper
from pdf_generator import InvestmentReportGenerator
from email_sender import EmailSender
from config import DAILY_RUN_TIME, TIMEZONE, RECIPIENT_EMAIL, ARCHIVE_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('investment_aggregator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InvestmentAggregatorScheduler:
    """Orchestrates data collection, report generation, and email distribution"""

    def __init__(self):
        self.scraper = InvestorDataScraper()
        self.email_sender = EmailSender()
        self.archive_dir = ARCHIVE_DIR
        self._create_archive_dir()

    def _create_archive_dir(self):
        """Create archive directory if it doesn't exist"""
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)
            logger.info(f"Created archive directory: {self.archive_dir}")

    def run_daily_report(self):
        """Execute the complete daily report workflow"""
        try:
            logger.info("=" * 80)
            logger.info("STARTING DAILY INVESTMENT REPORT GENERATION")
            logger.info("=" * 80)

            # Step 1: Collect Data
            logger.info("Step 1: Collecting data from all sources...")
            start_collection = datetime.now()
            data = self.scraper.collect_all_investors_data()
            collection_time = (datetime.now() - start_collection).total_seconds()
            logger.info(f"Data collection completed in {collection_time:.2f} seconds")

            # Step 2: Generate PDF
            logger.info("Step 2: Generating PDF report...")
            start_pdf = datetime.now()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = os.path.join(self.archive_dir, f"investment_report_{timestamp}.pdf")
            
            generator = InvestmentReportGenerator(pdf_filename)
            generated_pdf = generator.generate_report(data)
            pdf_time = (datetime.now() - start_pdf).total_seconds()
            logger.info(f"PDF generated in {pdf_time:.2f} seconds: {generated_pdf}")

            # Step 3: Send Email
            logger.info("Step 3: Sending report via email...")
            start_email = datetime.now()
            self.email_sender.send_report(generated_pdf, RECIPIENT_EMAIL)
            email_time = (datetime.now() - start_email).total_seconds()
            logger.info(f"Email sent in {email_time:.2f} seconds")

            # Step 4: Archive Management
            logger.info("Step 4: Managing archives...")
            self._cleanup_old_reports()

            total_time = (datetime.now() - start_collection).total_seconds()
            logger.info("=" * 80)
            logger.info(f"DAILY REPORT COMPLETED SUCCESSFULLY")
            logger.info(f"Total execution time: {total_time:.2f} seconds")
            logger.info(f"Report sent to: {RECIPIENT_EMAIL}")
            logger.info("=" * 80)

        except Exception as e:
            logger.error("=" * 80)
            logger.error(f"ERROR IN DAILY REPORT GENERATION: {e}")
            logger.error("=" * 80)
            self._send_error_notification(str(e))

    def _cleanup_old_reports(self, days_to_keep=30):
        """Remove reports older than specified days"""
        try:
            import shutil
            from datetime import timedelta

            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            deleted_count = 0

            for filename in os.listdir(self.archive_dir):
                if filename.startswith('investment_report_'):
                    filepath = os.path.join(self.archive_dir, filename)
                    file_date = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if file_date < cutoff_date:
                        os.remove(filepath)
                        deleted_count += 1
                        logger.info(f"Deleted old report: {filename}")

            if deleted_count > 0:
                logger.info(f"Cleanup: Removed {deleted_count} reports older than {days_to_keep} days")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def _send_error_notification(self, error_message):
        """Send error notification email"""
        try:
            logger.info("Sending error notification email...")
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from config import EMAIL_ADDRESS, EMAIL_PASSWORD

            message = MIMEMultipart()
            message["From"] = EMAIL_ADDRESS
            message["To"] = RECIPIENT_EMAIL
            message["Subject"] = f"⚠️ Investment Aggregator Error - {datetime.now().strftime('%Y-%m-%d')}"

            body = f"""
            <html>
                <body>
                    <h2 style="color: red;">Error in Investment Aggregator</h2>
                    <p>An error occurred while generating today's investment report:</p>
                    <pre style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
{error_message}
                    </pre>
                    <p>Please check the logs for more details.</p>
                    <p style="color: #666; font-size: 12px;">
                        Error time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </body>
            </html>
            """

            message.attach(MIMEText(body, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(message)

            logger.info("Error notification sent")
        except Exception as e:
            logger.error(f"Failed to send error notification: {e}")

    def schedule_daily_run(self):
        """Schedule the daily report to run at specified time"""
        run_time = DAILY_RUN_TIME  # Format: "08:00"
        
        schedule.every().day.at(run_time).do(self.run_daily_report)
        logger.info(f"Scheduled daily report to run at {run_time} {TIMEZONE}")

    def start_scheduler(self):
        """Start the scheduler and keep it running"""
        logger.info("Starting Investment Aggregator Scheduler")
        logger.info(f"Timezone: {TIMEZONE}")
        logger.info(f"Daily run time: {DAILY_RUN_TIME}")
        logger.info(f"Reports will be sent to: {RECIPIENT_EMAIL}")

        self.schedule_daily_run()

        # Run immediately on startup (optional - comment out to disable)
        logger.info("Running initial report on startup...")
        self.run_daily_report()

        # Keep scheduler running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)

    def run_once(self):
        """Run the report generation once (for testing)"""
        logger.info("Running report generation once...")
        self.run_daily_report()


def main():
    """Main entry point"""
    import sys

    scheduler = InvestmentAggregatorScheduler()

    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once and exit
        scheduler.run_once()
    else:
        # Start scheduler
        scheduler.start_scheduler()


if __name__ == "__main__":
    main()
