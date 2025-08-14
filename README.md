# 🚭 Tobacco Recipe Analysis Dashboard

An interactive web dashboard for analyzing tobacco recipe ingredient formulations with advanced filtering and visualization capabilities.

## 📁 Files in this workspace:
- `tobacco_dashboard.py` - Interactive dashboard application (main file)
- `Data_Raw.xlsx` - Source data containing recipe formulations
- `WORKING_HEATMAP.html` - Static heatmap (complete dataset)
- `FOCUSED_HEATMAP.html` - Static heatmap (recipes with data)
- `README.md` - This documentation file
- `.venv/` - Python virtual environment

## 🚀 How to run:

**Option 1 - Interactive Dashboard:**
1. Open terminal in this folder
2. Run: `python tobacco_dashboard.py`
3. Open browser and go to: **http://127.0.0.1:8060**

**Option 2 - Static HTML Files (Always Work):**
- Double-click `WORKING_HEATMAP.html` for complete dataset
- Double-click `FOCUSED_HEATMAP.html` for optimized view

## 📊 Features:

### **Interactive Controls:**
- **Recipe Selection**: Choose individual recipes or view all 18 recipes
- **Ingredient Selection**: Focus on specific ingredients or view all 73 filtered ingredients
- **Multi-select**: Select multiple recipes/ingredients for comparison

### **Smart Data Processing:**
- **Min-Max Normalization**: Values automatically normalized (0-1 scale) based on your selection
- **Intelligent Filtering**: Automatically removes 49 low-significance ingredients (used only once AND <0.03% weight)
- **Dynamic Updates**: Visualization updates in real-time as you change selections

### **Professional Visualization:**
- **Interactive Heatmap**: Hover for details, zoom and pan
- **Color Coding**: Dark = ingredient not used, Bright colors = high concentration
- **Clear Labels**: Recipe names on Y-axis, ingredient names on X-axis

## 📈 Data Overview:
- **Original Dataset**: 18 recipes × 122 ingredients
- **After Filtering**: 18 recipes × 73 significant ingredients
- **Total Data Points**: 1,314 recipe-ingredient combinations
- **Non-zero Values**: ~369 active ingredient usages

## 🎯 Use Cases:
1. **Recipe Comparison**: Select 2-3 recipes to see their differences
2. **Ingredient Analysis**: Choose key ingredients to see usage patterns
3. **Formulation Insights**: Identify ingredient clusters and recipe similarities
4. **Quality Control**: Spot unusual ingredient combinations or concentrations

## 🔧 Technical Details:
- Built with Dash (Python web framework)
- Uses Plotly for interactive visualizations
- Pandas for data processing
- Min-max normalization for fair comparison across different concentration ranges

---
*Dashboard created for tobacco recipe formulation analysis*
