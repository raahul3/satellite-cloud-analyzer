import cv2
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

# === CONFIGURATION ===
URL = "https://mosdac.gov.in/gallery/index.html?&prod=3SIMG_%27*_L1C_ASIA_MER_BIMG_TAMILNADU_V%27*.jpg&date=2025-06-12&count=8"
SCREENSHOT_PATH = "MOSDAC_BT_TAMILNADU_09JUN2025.png"
PDF_REPORT_PATH = "Cloud_Density_Report.pdf"
GRID_ROWS, GRID_COLS = 3, 3  # 3x3 = 9 zones

# === STEP 1: Capture Screenshot (VISIBLE browser) ===
def capture_satellite_image():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")

    print("[🛰] Accessing MOSDAC...")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(10)  # wait for page to load
    driver.save_screenshot(SCREENSHOT_PATH)
    driver.quit()
    print(f"[✅] Screenshot saved as {SCREENSHOT_PATH}")

# === STEP 2: Analyze Zones ===
def analyze_grid_cloud_density(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    zone_height, zone_width = height // GRID_ROWS, width // GRID_COLS

    # BGR thresholds for different cloud types
    high_cloud = cv2.inRange(image, np.array([0, 0, 100]), np.array([80, 80, 255]))
    medium_cloud = cv2.inRange(image, np.array([100, 180, 180]), np.array([200, 255, 255]))
    low_cloud = cv2.inRange(image, np.array([180, 0, 100]), np.array([255, 100, 255]))

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
            clear = zone_total - (h + m + l)

            h_pct, m_pct, l_pct, clear_pct = h/zone_total*100, m/zone_total*100, l/zone_total*100, clear/zone_total*100
            print(f"| Z{zone_number:^4} | {h_pct:6.1f} | {m_pct:8.1f} | {l_pct:6.1f} | {clear_pct:8.1f} |")

            zone_data.append([f"Zone {zone_number}", f"{h_pct:.1f}%", f"{m_pct:.1f}%", f"{l_pct:.1f}%", f"{clear_pct:.1f}%"])
            zone_number += 1

    return zone_data

# === STEP 3: Generate PDF Report ===
def generate_pdf_report(zone_data, screenshot_path):
    c = canvas.Canvas(PDF_REPORT_PATH, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Tamil Nadu Satellite Cloud Density Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "This report shows the cloud coverage over Tamil Nadu in 9 zones.")

    # Prepare table data
    data = [["Zone", "High Cloud", "Medium Cloud", "Low Cloud", "Clear Sky"]] + zone_data
    table = Table(data, colWidths=[80]*5)

    # Table Styling
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10)
    ])
    table.setStyle(style)

    # Draw table
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 350)

    # Final notes
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 370, "Cloud type colors:")
    c.drawString(50, height - 385, "- High Cloud: Bright white or intense regions")
    c.drawString(50, height - 400, "- Medium Cloud: Light grayish or soft white")
    c.drawString(50, height - 415, "- Low Cloud: Diffuse or shaded regions")
    c.drawString(50, height - 430, "- Clear Sky: Areas without clouds")

    # Optional: add image thumbnail
    try:
        from reportlab.platypus import Image
        img = Image(screenshot_path, width=250, height=140)
        img.drawOn(c, width - 300, height - 550)
    except:
        pass

    c.save()
    print(f"[📄] PDF Report generated: {PDF_REPORT_PATH}")

# === MAIN ===
if __name__ == "__main__":
    capture_satellite_image()
    zone_stats = analyze_grid_cloud_density(SCREENSHOT_PATH)
    generate_pdf_report(zone_stats, SCREENSHOT_PATH)