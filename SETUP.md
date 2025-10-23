# 🔧 Installation and Setup Guide

## Prerequisites
Make sure you have Python 3.7+ installed on your system.

### Option 1: Quick Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/raahul3/satellite-cloud-analyzer.git
cd satellite-cloud-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the analyzer (v2 recommended)
python cloud_analyzer_v2.py
```

### Option 2: Manual Installation
```bash
# Install individual packages
pip install opencv-python selenium reportlab numpy webdriver-manager pillow matplotlib

# Clone and run
git clone https://github.com/raahul3/satellite-cloud-analyzer.git
cd satellite-cloud-analyzer
python cloud_analyzer_v2.py
```

## Files Overview

### 🗂️ Main Scripts
- `cloud_analyzer.py` - Original version (requires manual ChromeDriver setup)
- `cloud_analyzer_v2.py` - **Improved version** (automatic driver management) ⭐

### 📄 Configuration Files  
- `requirements.txt` - Python dependencies
- `README.md` - Main documentation
- `LICENSE` - MIT license

### 🎯 Expected Outputs
After running the script, you'll get:
- `MOSDAC_BT_TAMILNADU_09JUN2025.png` - Screenshot from MOSDAC
- `Cloud_Density_Report.pdf` - Detailed analysis report

## Troubleshooting

### Common Issues & Solutions

**❌ ChromeDriver Issues**
```bash
# v2 automatically handles this, but if needed:
# Download ChromeDriver from: https://chromedriver.chromium.org/
# Make sure Chrome browser is installed
```

**❌ Module Not Found**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**❌ Website Loading Problems**
```python
# Increase wait time in the script (line ~43):
time.sleep(20)  # Instead of 15
```

**❌ Image Processing Errors**
```bash
# Make sure OpenCV is properly installed
pip uninstall opencv-python
pip install opencv-python-headless
```

## System Requirements
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **RAM**: Minimum 4GB (8GB recommended)
- **Python**: 3.7 or higher
- **Internet**: Required for MOSDAC data access
- **Browser**: Chrome/Chromium installed

## Usage Examples

### Basic Usage
```bash
python cloud_analyzer_v2.py
```

### Advanced Configuration
Edit the configuration section in `cloud_analyzer_v2.py`:
```python
# Change grid size for more/fewer zones
GRID_ROWS, GRID_COLS = 4, 4  # 16 zones instead of 9

# Change output filenames
SCREENSHOT_PATH = "custom_screenshot.png"
PDF_REPORT_PATH = "custom_report.pdf"
```

## 🎯 What Happens When You Run?

1. **Screenshot Capture** 🛰️
   - Opens MOSDAC website automatically
   - Captures satellite imagery
   - Saves as PNG file

2. **Zone Analysis** 📊
   - Divides image into 3x3 grid (9 zones)
   - Analyzes cloud types using HSV color space
   - Calculates percentages for each zone

3. **Report Generation** 📄
   - Creates comprehensive PDF report
   - Includes statistics and analysis
   - Adds visual elements and thumbnails

## Performance Tips

- **Faster Processing**: Use `cloud_analyzer_v2.py` (optimized)
- **Better Accuracy**: Ensure good internet connection for clear images
- **Memory Usage**: Close other browsers before running
- **File Size**: PNG screenshots are ~500KB, PDF reports ~2MB

## Next Steps
After successful installation:
1. Run the basic analysis
2. Check the generated PDF report
3. Modify configuration for your needs
4. Explore the code for customizations

---
**Need Help?** 
- Check the main [README.md](README.md) for detailed documentation
- Report issues on [GitHub Issues](https://github.com/raahul3/satellite-cloud-analyzer/issues)