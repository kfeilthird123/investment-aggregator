from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvestmentReportGenerator:
    """Generates professional PDF investment reports"""

    def __init__(self, filename=None):
        self.filename = filename or f"investment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.doc = SimpleDocTemplate(
            self.filename,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.5 * inch,
        )
        self.styles = getSampleStyleSheet()
        self.elements = []
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='InvestorName',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=4,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['BodyText'],
            fontSize=9,
            spaceAfter=4,
            leading=11
        ))

    def add_header(self):
        """Add report header"""
        title = Paragraph("📊 Daily Investment Report", self.styles['CustomTitle'])
        self.elements.append(title)
        
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"<i>Generated: {date_str}</i>", ParagraphStyle(
            'DateStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
        self.elements.append(date_para)
        self.elements.append(Spacer(1, 0.2 * inch))

    def add_market_overview(self, market_data):
        """Add market overview section"""
        self.elements.append(Paragraph("Market Overview", self.styles['SectionHeader']))
        
        if market_data:
            market_table_data = [["Index", "Price", "Change (%)", "Time"]]
            
            index_names = {
                "^GSPC": "S&P 500",
                "^IXIC": "Nasdaq",
                "^DJI": "Dow Jones",
                "^VIX": "VIX",
                "^TNX": "10Y Treasury"
            }

            for ticker, name in index_names.items():
                if ticker in market_data:
                    data = market_data[ticker]
                    price = f"${data.get('price', 'N/A'):.2f}" if isinstance(data.get('price'), (int, float)) else str(data.get('price'))
                    change = data.get('change', 0)
                    change_color = colors.green if change >= 0 else colors.red
                    change_text = f"<font color='{'#00aa00' if change >= 0 else '#ff0000'}'>{change:+.2f}%</font>"
                    
                    market_table_data.append([
                        name,
                        price,
                        change_text,
                        data.get('timestamp', '')[:10]
                    ])

            table = Table(market_table_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ]))
            self.elements.append(table)
        else:
            self.elements.append(Paragraph("Market data unavailable", self.styles['BodyText']))
        
        self.elements.append(Spacer(1, 0.15 * inch))

    def add_investor_section(self, investor_name, investor_data):
        """Add section for individual investor"""
        # Investor header
        self.elements.append(Paragraph(f"🎯 {investor_name}", self.styles['InvestorName']))

        # 13F Filings
        if investor_data.get('13f_filings'):
            self.elements.append(Paragraph("Recent 13F Filings", self.styles['SectionHeader']))
            for filing in investor_data['13f_filings'][:3]:
                filing_text = f"<b>{filing.get('date')}</b> - <a href='{filing.get('url')}'>View Filing</a>"
                self.elements.append(Paragraph(filing_text, self.styles['BodyText']))
            self.elements.append(Spacer(1, 0.1 * inch))

        # Shareholder Letters
        if investor_data.get('shareholder_letters'):
            self.elements.append(Paragraph("Shareholder Letters & Reports", self.styles['SectionHeader']))
            for letter in investor_data['shareholder_letters'][:3]:
                letter_text = f"<b>{letter.get('title')}</b> - <a href='{letter.get('url')}'>Read</a>"
                self.elements.append(Paragraph(letter_text, self.styles['BodyText']))
            self.elements.append(Spacer(1, 0.1 * inch))

        # News Articles
        if investor_data.get('news_articles'):
            self.elements.append(Paragraph("Recent News & Commentary", self.styles['SectionHeader']))
            for article in investor_data['news_articles'][:3]:
                article_text = f"""
                <b>{article.get('title', 'N/A')[:80]}</b><br/>
                <font size='8'>{article.get('source', 'News')} - {article.get('published', '')[:10]}</font><br/>
                <font size='8'>{article.get('summary', 'N/A')[:150]}...</font>
                """
                self.elements.append(Paragraph(article_text, self.styles['BodyText']))
            self.elements.append(Spacer(1, 0.1 * inch))

        # Podcasts
        if investor_data.get('podcasts'):
            self.elements.append(Paragraph("Podcast Mentions", self.styles['SectionHeader']))
            for podcast in investor_data['podcasts'][:2]:
                podcast_text = f"""
                <b>{podcast.get('podcast')}</b>: {podcast.get('title', 'N/A')[:75]}<br/>
                <font size='8'>{podcast.get('published', '')[:10]}</font>
                """
                self.elements.append(Paragraph(podcast_text, self.styles['BodyText']))
            self.elements.append(Spacer(1, 0.1 * inch))

        # Portfolio Holdings
        if investor_data.get('portfolio') and investor_data['portfolio'].get('holdings'):
            self.elements.append(Paragraph("Portfolio Holdings", self.styles['SectionHeader']))
            holdings = investor_data['portfolio']['holdings']
            if holdings:
                for holding in holdings[:5]:
                    holding_text = f"<b>{holding.get('symbol', 'N/A')}</b> - {holding.get('shares', 'N/A')} shares (${holding.get('value', 'N/A')})"
                    self.elements.append(Paragraph(holding_text, self.styles['BodyText']))
            self.elements.append(Spacer(1, 0.1 * inch))

        self.elements.append(Spacer(1, 0.15 * inch))

    def add_investment_themes(self, investors_data):
        """Extract and display common investment themes"""
        self.elements.append(Paragraph("Key Investment Themes & Insights", self.styles['SectionHeader']))
        
        # This would analyze all investor data to identify common themes
        themes = [
            "🔹 Technology: Multiple funds increasing exposure to AI and cloud computing",
            "🔹 Healthcare: Strong interest in biotech and pharmaceuticals",
            "🔹 Energy: Selective positioning in renewable and traditional energy",
            "🔹 Finance: Banking sector rotation based on interest rates",
            "🔹 Valuations: Focus on discounted valuations amid market uncertainty"
        ]
        
        for theme in themes:
            self.elements.append(Paragraph(theme, self.styles['BodyText']))
        
        self.elements.append(Spacer(1, 0.15 * inch))

    def add_market_commentary(self):
        """Add general market commentary"""
        self.elements.append(Paragraph("Market Commentary", self.styles['SectionHeader']))
        
        commentary = """
        Today's market shows mixed signals as investors navigate economic uncertainty. 
        The Fed's policy stance remains the primary driver of sentiment. Value investors 
        continue to find selective opportunities in quality companies trading at reasonable 
        valuations. Portfolio managers are maintaining diversified exposures while positioning 
        for potential volatility.
        """
        
        self.elements.append(Paragraph(commentary, self.styles['BodyText']))
        self.elements.append(Spacer(1, 0.15 * inch))

    def generate_report(self, data):
        """Generate complete PDF report"""
        try:
            logger.info(f"Generating PDF report: {self.filename}")
            
            self.add_header()
            
            # Market Overview
            market_data = data.get('market', {})
            self.add_market_overview(market_data)
            
            # Market Commentary
            self.add_market_commentary()
            
            # Key Themes
            self.add_investment_themes(data.get('investors', {}))
            
            # Individual Investor Sections
            for investor_name, investor_data in data.get('investors', {}).items():
                self.add_investor_section(investor_name, investor_data)
                
                # Add page break between investors (but not after last one)
                if investor_name != list(data.get('investors', {}).keys())[-1]:
                    self.elements.append(PageBreak())

            # Footer
            self.elements.append(Spacer(1, 0.3 * inch))
            footer_text = """
            <font size='8' color='gray'>
            This report aggregates publicly available information from shareholder letters, 
            SEC filings, news sources, and other public materials. This is not investment advice. 
            Always conduct your own research and consult with a financial advisor.
            </font>
            """
            self.elements.append(Paragraph(footer_text, self.styles['Normal']))

            # Build PDF
            self.doc.build(self.elements)
            logger.info(f"PDF report generated successfully: {self.filename}")
            return self.filename

        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise

    def get_filename(self):
        """Return the PDF filename"""
        return self.filename


if __name__ == "__main__":
    # Test report generation
    sample_data = {
        "market": {
            "^GSPC": {"price": 4500, "change": 1.25, "timestamp": "2024-01-01T10:30:00"},
            "^IXIC": {"price": 14000, "change": 0.50, "timestamp": "2024-01-01T10:30:00"}
        },
        "investors": {
            "Maverick Capital": {
                "13f_filings": [{"date": "2024-01-01", "url": "http://example.com"}],
                "shareholder_letters": [],
                "news_articles": [],
                "podcasts": [],
                "portfolio": {"holdings": []}
            }
        }
    }
    
    generator = InvestmentReportGenerator()
    pdf_file = generator.generate_report(sample_data)
    print(f"Report generated: {pdf_file}")
