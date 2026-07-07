import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import logging
from datetime import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Handles sending investment reports via email"""

    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = EMAIL_ADDRESS
        self.sender_password = EMAIL_PASSWORD

    def send_report(self, pdf_filename, recipient_email=None):
        """Send PDF report via email"""
        if recipient_email is None:
            recipient_email = RECIPIENT_EMAIL

        try:
            logger.info(f"Preparing to send report to {recipient_email}")

            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = f"Daily Investment Report - {datetime.now().strftime('%B %d, %Y')}"

            # Email body
            body = self._create_email_body()
            message.attach(MIMEText(body, "html"))

            # Attach PDF
            self._attach_pdf(message, pdf_filename)

            # Send email
            self._send_email(message, recipient_email)

            logger.info(f"Report successfully sent to {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise

    def _create_email_body(self):
        """Create HTML email body"""
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #1f4788; text-align: center;">📊 Daily Investment Report</h2>
                    
                    <p>Good morning,</p>
                    
                    <p>Your daily investment aggregation report is attached below. This report includes:</p>
                    
                    <ul>
                        <li>Market overview and indices performance</li>
                        <li>Recent SEC 13F filings from tracked funds</li>
                        <li>Shareholder letters and annual reports</li>
                        <li>Relevant news and market commentary</li>
                        <li>Podcast mentions and interviews</li>
                        <li>Portfolio holdings and changes</li>
                        <li>Key investment themes and insights</li>
                    </ul>
                    
                    <p><strong>Tracked Investors:</strong></p>
                    <ul>
                        <li>Maverick Capital</li>
                        <li>Tiger Global</li>
                        <li>Surgo Capital</li>
                        <li>Ruane Cunniff</li>
                        <li>Gardner Russo</li>
                        <li>Quinn Davis Funds</li>
                        <li>Lone Pine Capital</li>
                        <li>Bill Ackman (Pershing Square)</li>
                        <li>Tom Russo (Gardner Russo & Quinn)</li>
                        <li>Gavin Baker (Atreides Management)</li>
                        <li>Abramas Bison</li>
                        <li>Giverny Capital</li>
                        <li>David Poppe</li>
                    </ul>
                    
                    <p>
                        <strong>Report Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ccc; margin: 20px 0;">
                    
                    <p style="font-size: 12px; color: #666;">
                        <strong>Disclaimer:</strong> This report aggregates publicly available information 
                        from shareholder letters, SEC filings, news sources, podcasts, and other public materials. 
                        The information is provided for informational purposes only and does not constitute 
                        investment advice. Please conduct your own research and consult with a financial advisor 
                        before making any investment decisions.
                    </p>
                    
                    <p style="font-size: 12px; color: #999;">
                        Automatic Daily Report | {datetime.now().strftime('%B %d, %Y')}
                    </p>
                </div>
            </body>
        </html>
        """
        return body

    def _attach_pdf(self, message, pdf_filename):
        """Attach PDF file to email"""
        try:
            with open(pdf_filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {pdf_filename}")
            message.attach(part)
            logger.info(f"PDF attached: {pdf_filename}")

        except FileNotFoundError:
            logger.error(f"PDF file not found: {pdf_filename}")
            raise

    def _send_email(self, message, recipient_email):
        """Send email via SMTP"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                logger.info("Email sent successfully via SMTP")

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check email and password.")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise

    def send_test_email(self):
        """Send a test email to verify configuration"""
        try:
            logger.info("Sending test email...")
            
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = RECIPIENT_EMAIL
            message["Subject"] = "Test Email - Investment Aggregator"

            body = """
            <html>
                <body>
                    <h2>Test Email</h2>
                    <p>This is a test email from the Investment Aggregator system.</p>
                    <p>If you received this, your email configuration is working correctly!</p>
                    <p style="color: #666; font-size: 12px;">
                        Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </body>
            </html>
            """.format(datetime=datetime)

            message.attach(MIMEText(body, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            logger.info("Test email sent successfully!")
            return True

        except Exception as e:
            logger.error(f"Test email failed: {e}")
            return False


if __name__ == "__main__":
    sender = EmailSender()
    # Uncomment to send test email
    # sender.send_test_email()
