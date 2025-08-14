# 🚭 Tobacco Recipe Analysis - Interactive Heatmap Server

A professional web-based interactive heatmap visualization tool for analyzing tobacco recipe ingredient formulations with sensory grouping and advanced visualization features.

## 📁 Files in this workspace:
- `tobacco_heatmap_FINAL.py` - Interactive Dash server application (main file)
- `Data_Raw.xlsx` - Source data containing recipe formulations (18 recipes × 86 ingredients)
- `Sensory_Note.xlsx` - Ingredient sensory classification data
- `README.md` - This documentation file
- `.gitignore` - Git ignore configuration

## 🚀 How to run:

**Interactive Heatmap Server:**
1. Install dependencies: `pip install dash pandas numpy plotly openpyxl`
2. Open terminal in this folder
3. Run: `python tobacco_heatmap_FINAL.py`
4. Open browser and go to: **http://localhost:8050**

## 📊 Features:

### **Professional Visualization:**
- **Interactive Heatmap**: Hover for detailed ingredient information
- **Sensory Grouping**: Ingredients organized by taste profiles (Sweet, Dry, Rich, Light, Smooth, Harsh, Cooling)
- **Recipe Groups**: Color-coded recipe groups (G1-G4) with red borderlines
- **Clean Interface**: Minimal design with white cell grids and optimized layout
- **Real-time Updates**: Auto-reload when data files are modified

### **Smart Data Organization:**
- **Sensory Classification**: 85 ingredients classified into 7 sensory categories
- **Recipe Grouping**: 18 recipes organized into 4 distinct groups
- **Custom Ordering**: Ingredients ordered by sensory profile, recipes by group
- **Visual Clarity**: White cells for blank values, grid lines for clear separation

### **Technical Features:**
- **Dash Web Server**: Professional Flask-based web application
- **Plotly Visualization**: High-quality interactive heatmaps
- **Data Processing**: Pandas-based Excel file handling
- **Responsive Design**: Optimized for various screen sizes

## 📈 Data Overview:
- **Recipe Data**: 18 tobacco formulations across 4 groups (G1-G4)
- **Ingredient Data**: 86 ingredients with sensory classifications
- **Sensory Groups**: Sweet (14), Light (15), Smooth (12), Rich (22), Dry (9), Harsh (10), Cooling (3)
- **Data Source**: Excel files with comprehensive formulation details

## 🎯 Use Cases:
1. **Formulation Analysis**: Visualize ingredient usage patterns across recipes
2. **Sensory Profiling**: Understand taste profile distributions
3. **Recipe Comparison**: Compare ingredient compositions between groups
4. **Research Tool**: Interactive exploration of tobacco blend formulations

## 🛠️ Dependencies:
```bash
pip install dash pandas numpy plotly openpyxl
```

## 📋 Requirements:
- Python 3.7+
- Modern web browser
- Excel data files (Data_Raw.xlsx, Sensory_Note.xlsx)
4. **Quality Control**: Spot unusual ingredient combinations or concentrations

## 🔧 Technical Details:
- Built with Dash (Python web framework)
- Uses Plotly for interactive visualizations
- Pandas for data processing
- Min-max normalization for fair comparison across different concentration ranges

---
*Dashboard created for tobacco recipe formulation analysis*
