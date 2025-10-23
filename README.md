# 🛰️ Satellite Cloud Analyzer

**Automated Tamil Nadu Satellite Cloud Density Analysis Tool** 

## 📋 Overview
This tool automatically captures satellite imagery from MOSDAC (Meteorological & Oceanographic Satellite Data Archival Centre) and analyzes cloud density patterns over Tamil Nadu region. It divides the area into 9 zones and generates detailed PDF reports with cloud coverage percentages.

## ✨ Features
- 🔄 **Automated Screenshot Capture** from MOSDAC website
- 📊 **9-Zone Grid Analysis** for detailed regional coverage  
- ☁️ **Multi-Cloud Type Detection** (High, Medium, Low clouds)
- 📄 **Professional PDF Report Generation**
- 🎯 **Real-time Processing** with visual feedback

## 🛠️ Technologies Used
- **Python 3.x** - Main programming language
- **OpenCV** - Image processing and analysis
- **Selenium WebDriver** - Automated web scraping
- **ReportLab** - PDF generation
- **NumPy** - Numerical computations

## 📦 Installation

### Prerequisites
```bash
# Install Python packages
pip install opencv-python selenium reportlab numpy

# Download ChromeDriver
# Visit: https://chromedriver.chromium.org/
# Extract and add to PATH
```

### Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/raahul3/satellite-cloud-analyzer.git
cd satellite-cloud-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure ChromeDriver is in your system PATH

## 🚀 Usage

### Basic Usage
```bash
python cloud_analyzer.py
```

### Configuration Options
Edit the configuration section in `cloud_analyzer.py`:

```python
# === CONFIGURATION ===
URL = "https://mosdac.gov.in/gallery/index.html?&prod=3SIMG_%27*_L1C_ASIA_MER_BIMG_TAMILNADU_V%27*.jpg&date=2025-06-12&count=8"
SCREENSHOT_PATH = "MOSDAC_BT_TAMILNADU_09JUN2025.png"
PDF_REPORT_PATH = "Cloud_Density_Report.pdf"
GRID_ROWS, GRID_COLS = 3, 3  # Modify for different zone divisions
```

## 📊 Output Analysis

### Zone Grid Layout
```
Zone 1 | Zone 2 | Zone 3
Zone 4 | Zone 5 | Zone 6  
Zone 7 | Zone 8 | Zone 9
```

### Cloud Type Classification
- **High Cloud** ☁️ - Bright white or intense regions
- **Medium Cloud** 🌫️ - Light grayish or soft white areas
- **Low Cloud** 🌤️ - Diffuse or shaded regions  
- **Clear Sky** ☀️ - Areas without cloud coverage

### Sample Output
```
📊 Zonal Cloud Density (Grid View):
| Zone | High % | Medium % | Low % | Clear % |
|------|--------|----------|--------|-----------|
| Z 1  |    0.1 |      0.6 |    0.2 |     99.1 |
| Z 2  |    0.8 |      3.8 |    6.6 |     88.9 |
| Z 3  |    0.0 |      0.0 |    0.6 |     99.3 |
```

## 📁 File Structure
```
satellite-cloud-analyzer/
├── cloud_analyzer.py          # Main analysis script
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
├── sample_outputs/           # Example results
│   ├── sample_screenshot.png
│   └── sample_report.pdf
└── docs/                    # Additional documentation
    └── API_reference.md
```

## 🔧 Troubleshooting

### Common Issues

**1. ChromeDriver Not Found**
```bash
# Download ChromeDriver matching your Chrome version
# Add to PATH or place in project directory
```

**2. Website Loading Issues**
```python
# Increase wait time in capture_satellite_image()
time.sleep(15)  # Instead of 10 seconds
```

**3. Image Processing Errors**
```python
# Verify image file exists and is readable
if not os.path.exists(SCREENSHOT_PATH):
    print("Screenshot not found!")
```

## 🎯 Applications
- **Weather Forecasting** - Regional cloud pattern analysis
- **Agricultural Planning** - Crop irrigation scheduling  
- **Research Projects** - Climate study and meteorology
- **Educational Purpose** - Understanding satellite imagery

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- **MOSDAC** for providing satellite imagery data
- **ISRO** for meteorological satellite services
- **OpenCV Community** for image processing tools

## 📞 Contact
- **GitHub**: [@raahul3](https://github.com/raahul3)
- **Project Link**: [https://github.com/raahul3/satellite-cloud-analyzer](https://github.com/raahul3/satellite-cloud-analyzer)

---
⭐ **Star this repo if you found it helpful!** ⭐