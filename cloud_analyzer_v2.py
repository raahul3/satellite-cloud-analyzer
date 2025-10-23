# 🔧 Improved Cloud Analyzer with WebDriver Manager

import cv2
import numpy as np
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# === CONFIGURATION ===
URL = "https://mosdac.gov.in/gallery/index.html?&prod=3SIMG_%27*_L1C_ASIA_MER_BIMG_TAMILNADU_V%27*.jpg&date=2025-06-12&count=8"
SCREENSHOT_PATH = "MOSDAC_BT_TAMILNADU_09JUN2025.png"
PDF_REPORT_PATH = "Cloud_Density_Report.pdf"
GRID_ROWS, GRID_COLS = 3, 3  # 3x3 = 9 zones

class SatelliteCloudAnalyzer:
    def __init__(self):
        self.screenshot_path = SCREENSHOT_PATH
        self.pdf_path = PDF_REPORT_PATH
        self.url = URL
        
    def capture_satellite_image(self):
        """Capture screenshot from MOSDAC website with automatic driver management"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        
        try:
            print("[🛰] Accessing MOSDAC...")
            # Automatically download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            driver.get(self.url)
            time.sleep(15)  # Increased wait time for page loading
            driver.save_screenshot(self.screenshot_path)
            driver.quit()
            print(f"[✅] Screenshot saved as {self.screenshot_path}")
            return True
            
        except Exception as e:
            print(f"[❌] Error capturing screenshot: {str(e)}")
            return False

    def analyze_grid_cloud_density(self, image_path):
        """Analyze cloud density in 9 zones using improved color thresholds"""
        if not os.path.exists(image_path):
            print(f"[❌] Image file not found: {image_path}")
            return []
            
        try:
            image = cv2.imread(image_path)
            if image is None:
                print("[❌] Could not load image file")
                return []
                
            height, width = image.shape[:2]
            zone_height, zone_width = height // GRID_ROWS, width // GRID_COLS

            # Improved BGR thresholds for different cloud types
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # HSV thresholds (more accurate than BGR)
            high_cloud = cv2.inRange(hsv, np.array([0, 0, 200]), np.array([180, 50, 255]))  # White/bright areas
            medium_cloud = cv2.inRange(hsv, np.array([0, 0, 100]), np.array([180, 100, 199]))  # Gray areas
            low_cloud = cv2.inRange(hsv, np.array([0, 0, 50]), np.array([180, 150, 99]))  # Dark gray areas

            zone_data = []

            print("\n📊 Zonal Cloud Density (Grid View):")
            print("| Zone | High % | Medium % | Low % | Clear % |")
            print("|------|--------|----------|--------|----------|")

            zone_number = 1
            for r in range(GRID_ROWS):
                for c in range(GRID_COLS):
                    y1, y2 = r * zone_height, (r + 1) * zone_height
                    x1, x2 = c * zone_width, (c + 1) * zone_width

                    zone_total = (y2 - y1) * (x2 - x1)
                    h = np.sum(high_cloud[y1:y2, x1:x2] > 0)
                    m = np.sum(medium_cloud[y1:y2, x1:x2] > 0)
                    l = np.sum(low_cloud[y1:y2, x1:x2] > 0)
                    
                    # Avoid double counting
                    total_cloud = h + m + l
                    if total_cloud > zone_total:
                        # Normalize if overlap occurs
                        factor = zone_total / total_cloud
                        h, m, l = h * factor, m * factor, l * factor
                    
                    clear = zone_total - (h + m + l)

                    h_pct = (h / zone_total) * 100
                    m_pct = (m / zone_total) * 100
                    l_pct = (l / zone_total) * 100
                    clear_pct = (clear / zone_total) * 100

                    print(f"| Z{zone_number:^2} | {h_pct:6.1f} | {m_pct:8.1f} | {l_pct:6.1f} | {clear_pct:8.1f} |")
                    zone_data.append([f"Z {zone_number}", f"{h_pct:.1f}%", f"{m_pct:.1f}%", f"{l_pct:.1f}%", f"{clear_pct:.1f}%"])
                    zone_number += 1

            return zone_data
            
        except Exception as e:
            print(f"[❌] Error analyzing image: {str(e)}")
            return []

    def generate_pdf_report(self, zone_data, screenshot_path):
        """Generate comprehensive PDF report with enhanced styling"""
        try:
            c = canvas.Canvas(self.pdf_path, pagesize=A4)
            width, height = A4

            # Header
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width / 2, height - 50, "🛰️ Tamil Nadu Satellite Cloud Density Report")

            # Date and time
            from datetime import datetime
            current_time = datetime.now().strftime("%B %d, %Y at %H:%M IST")
            c.setFont("Helvetica", 10)
            c.drawCentredString(width / 2, height - 70, f"Generated on {current_time}")

            # Description
            c.setFont("Helvetica", 12)
            c.drawString(50, height - 100, "This report analyzes cloud coverage over Tamil Nadu using MOSDAC satellite imagery.")
            c.drawString(50, height - 115, "The region is divided into 9 zones for detailed analysis.")

            if zone_data:
                # Prepare table data
                headers = ["Zone", "High Cloud ☁️", "Medium Cloud 🌫️", "Low Cloud 🌤️", "Clear Sky ☀️"]
                data = [headers] + zone_data
                table = Table(data, colWidths=[60, 80, 80, 80, 80])

                # Enhanced table styling
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightgrey, colors.white])
                ])
                table.setStyle(style)

                # Draw table
                table.wrapOn(c, width, height)
                table.drawOn(c, 50, height - 300)
                
                # Analysis summary
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, height - 320, "📋 Analysis Summary:")
                
                # Calculate overall statistics
                total_high = sum([float(row[1].replace('%', '')) for row in zone_data])
                total_medium = sum([float(row[2].replace('%', '')) for row in zone_data])
                total_low = sum([float(row[3].replace('%', '')) for row in zone_data])
                total_clear = sum([float(row[4].replace('%', '')) for row in zone_data])
                
                avg_high = total_high / len(zone_data)
                avg_medium = total_medium / len(zone_data)
                avg_low = total_low / len(zone_data)
                avg_clear = total_clear / len(zone_data)
                
                c.setFont("Helvetica", 10)
                c.drawString(50, height - 340, f"• Average High Cloud Coverage: {avg_high:.1f}%")
                c.drawString(50, height - 355, f"• Average Medium Cloud Coverage: {avg_medium:.1f}%")
                c.drawString(50, height - 370, f"• Average Low Cloud Coverage: {avg_low:.1f}%")
                c.drawString(50, height - 385, f"• Average Clear Sky: {avg_clear:.1f}%")
                
                # Most/least cloudy zones
                cloudiest_zone = max(zone_data, key=lambda x: float(x[1].replace('%', '')) + float(x[2].replace('%', '')) + float(x[3].replace('%', '')))
                clearest_zone = max(zone_data, key=lambda x: float(x[4].replace('%', '')))
                
                c.drawString(50, height - 410, f"• Most Cloudy Zone: {cloudiest_zone[0]}")
                c.drawString(50, height - 425, f"• Clearest Zone: {clearest_zone[0]} ({clearest_zone[4]} clear)")

            else:
                c.setFont("Helvetica", 12)
                c.drawString(50, height - 200, "❌ No analysis data available")

            # Legend
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, height - 450, "🎨 Cloud Type Classification:")
            
            c.setFont("Helvetica", 9)
            c.drawString(50, height - 470, "☁️  High Cloud: Bright white or intense regions (High altitude)")
            c.drawString(50, height - 485, "🌫️  Medium Cloud: Light grayish areas (Medium altitude)")
            c.drawString(50, height - 500, "🌤️  Low Cloud: Diffuse or darker regions (Low altitude)")
            c.drawString(50, height - 515, "☀️  Clear Sky: Areas without significant cloud coverage")

            # Footer
            c.setFont("Helvetica", 8)
            c.drawString(50, 50, "Data Source: MOSDAC (Meteorological & Oceanographic Satellite Data Archival Centre)")
            c.drawString(50, 35, "Analysis Tool: Satellite Cloud Analyzer v2.0 | GitHub: @raahul3")

            # Add thumbnail if image exists
            if os.path.exists(screenshot_path):
                try:
                    from reportlab.lib.utils import ImageReader
                    img_width, img_height = 200, 120
                    c.drawImage(screenshot_path, width - img_width - 50, height - 200, 
                              width=img_width, height=img_height, preserveAspectRatio=True)
                    c.setFont("Helvetica", 8)
                    c.drawString(width - img_width - 50, height - 210, "Satellite Image Thumbnail")
                except Exception as img_error:
                    print(f"[⚠️] Could not add image thumbnail: {img_error}")

            c.save()
            print(f"📄] PDF Report generated: {self.pdf_path}")
            return True
            
        except Exception as e:
            print(f"[❌] Error generating PDF: {str(e)}")
            return False

    def run_analysis(self):
        """Run complete analysis pipeline"""
        print("🛰️ Starting Satellite Cloud Analysis...")
        print("=" * 50)
        
        # Step 1: Capture screenshot
        if not self.capture_satellite_image():
            return False
        
        # Step 2: Analyze cloud density
        zone_stats = self.analyze_grid_cloud_density(self.screenshot_path)
        if not zone_stats:
            return False
        
        # Step 3: Generate PDF report
        if not self.generate_pdf_report(zone_stats, self.screenshot_path):
            return False
        
        print("=" * 50)
        print("✅ Analysis completed successfully!")
        print(f"📊 Results saved in: {self.pdf_path}")
        print(f"🖼️ Screenshot saved as: {self.screenshot_path}")
        return True

# === MAIN EXECUTION ===
if __name__ == "__main__":
    analyzer = SatelliteCloudAnalyzer()
    analyzer.run_analysis()