#!/usr/bin/env python3
"""
STANDALONE TOBACCO HEATMAP GENERATOR
====================================
This script generates a standalone HTML file with embedded JavaScript
for interactive tobacco heatmap visualization.

Output: tobacco_heatmap_standalone.html

Usage: python generate_standalone_heatmap.py
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

def load_and_process_data():
    """Load and process the tobacco data"""
    print("=" * 70)
    print("🚭 GENERATING STANDALONE TOBACCO HEATMAP")
    print("Loading and processing data...")
    print("=" * 70)
    
    # Load main data
    try:
        df = pd.read_excel('Data_Raw.xlsx', index_col=0)
        print(f"✅ Loaded main data: {df.shape[0]} recipes × {df.shape[1]} ingredients")
    except Exception as e:
        print(f"❌ Error loading Data_Raw.xlsx: {e}")
        return None, None
    
    # Load sensory notes
    try:
        sensory_df = pd.read_excel('Sensory_Note.xlsx')
        print(f"✅ Loaded sensory notes: {len(sensory_df)} ingredient classifications")
    except Exception as e:
        print(f"❌ Error loading Sensory_Note.xlsx: {e}")
        return None, None
    
    return df, sensory_df

def define_recipe_groups():
    """Define the G1-G4 recipe groups"""
    tobacco_groups = {
        'G1 - MGO and Filed': [
            'J1 Virginia Tobacco 5%',
            'TOBACCO (VIRGINIA) 5% (+38% FL) E-400360',
            'VIRGINIA TOBACCO 5% (DDS00451B)',
            '(ILLINOIS) TOBACCO VT 5% NFC) DDS00734',
            'TOBACCO(GOLDEN) 5% ( +38% FL) (E-400361)'
        ],
        'G2': [
            'RUBY TOBACCO (S2) 3% (40%VG) (E-400518)',
            'PURPLE TOBACCO3% (E-400514)',
            'TOBACCO(AMERICAN) 5% (E-400469)',
            '(OREGON) AMERICAN TOBACCO 5% (CHINA WL) DDS00737'
        ],
        'G3': [
            'AUTUMN TOBACCO 3% (E-400519)',
            'TOBACCO (BLONDE) 5% +25% FL (PAB00426B)',
            'SRI LANKA  TOBACCO 5% (E-400451)',
            'VERMONT TOBACCO  5% (E-400454)',
            '(COLORADO) VIRGINIA TOBACCO 5% (DDS00735)',
            '(ARIZONA) BLONDE TOBACCO5% (CHINA WL) DDS00736'
        ],
        'G4 - Unique': [
            'Classic Tobacco 5% (345-00006)',
            'CALIFORNIA TOBACCO 5% (E-400452)',
            'Golden Tobacco 5% J1 (345-00124)'
        ]
    }
    return tobacco_groups

def create_sensory_groups(df, sensory_df):
    """Create ingredient groupings based on sensory notes"""
    print("\n🧪 INGREDIENT SENSORY GROUPING")
    print("-" * 40)
    
    # Create sensory note mapping
    sensory_map = {}
    for _, row in sensory_df.iterrows():
        ingredient = row['product']
        sensory_note = row['Sensory Note']
        if pd.notna(ingredient) and pd.notna(sensory_note):
            sensory_map[ingredient] = sensory_note
    
    print(f"Sensory notes for {len(sensory_map)} ingredients")
    
    # Group ingredients by sensory notes
    sensory_groups = {
        'Sweet': [], 'Light': [], 'Smooth': [], 'Rich': [],
        'Dry': [], 'Harsh': [], 'Cooling': [], 'Ungrouped': []
    }
    
    for ingredient in df.columns:
        sensory_note = sensory_map.get(ingredient, 'Ungrouped')
        if sensory_note in sensory_groups:
            sensory_groups[sensory_note].append(ingredient)
        else:
            sensory_groups['Ungrouped'].append(ingredient)
    
    # Print grouping summary
    for group, ingredients in sensory_groups.items():
        print(f"  {group}: {len(ingredients)} ingredients")
        if group == 'Ungrouped' and ingredients:
            print(f"    Ungrouped ingredients: {', '.join(ingredients[:5])}{'...' if len(ingredients) > 5 else ''}")
    
    return sensory_groups

def organize_data(df, tobacco_groups, sensory_groups):
    """Organize data by groups and prepare for HTML export"""
    print("\n📊 ORGANIZING DATA FOR HTML EXPORT")
    print("-" * 40)
    
    # Order recipes by groups
    recipe_order = []
    recipe_groups = {}
    
    for group_name, recipes in tobacco_groups.items():
        print(f"  {group_name}: {len(recipes)} recipes")
        for recipe in recipes:
            if recipe in df.index:
                recipe_order.append(recipe)
                recipe_groups[recipe] = group_name
    
    # Order ingredients by sensory groups
    ingredient_order = []
    ingredient_groups = {}
    sensory_group_order = ['Sweet', 'Dry', 'Rich', 'Light', 'Smooth', 'Harsh', 'Cooling']
    
    for group_name in sensory_group_order:
        for ingredient in sensory_groups[group_name]:
            if ingredient in df.columns:
                ingredient_order.append(ingredient)
                ingredient_groups[ingredient] = group_name
    
    # Add ungrouped ingredients at the end
    for ingredient in sensory_groups['Ungrouped']:
        if ingredient in df.columns:
            ingredient_order.append(ingredient)
            ingredient_groups[ingredient] = 'Ungrouped'
    
    print(f"  Total recipes ordered: {len(recipe_order)}")
    print(f"  Total ingredients ordered: {len(ingredient_order)}")
    
    return recipe_order, ingredient_order, recipe_groups, ingredient_groups

def generate_html_file(df, recipe_order, ingredient_order, recipe_groups, ingredient_groups, tobacco_groups):
    """Generate the standalone HTML file with embedded JavaScript"""
    
    # Prepare data for JavaScript
    heatmap_data = []
    for recipe in recipe_order:
        row_data = []
        for ingredient in ingredient_order:
            value = df.loc[recipe, ingredient] if ingredient in df.columns else 0
            row_data.append(float(value) if pd.notna(value) else 0)
        heatmap_data.append(row_data)
    
    # Group headers for display
    group_headers = {
        'G1 - MGO and Filed': 'G1',
        'G2': 'G2', 
        'G3': 'G3',
        'G4 - Unique': 'G4'
    }
    
    # Organize recipes by groups for buttons
    grouped_recipes = {}
    for group_name in ['G1 - MGO and Filed', 'G2', 'G3', 'G4 - Unique']:
        grouped_recipes[group_name] = [recipe for recipe in recipe_order if recipe_groups.get(recipe) == group_name]
    
    # Organize ingredients by sensory groups for column headers
    sensory_group_order = ['Sweet', 'Dry', 'Rich', 'Light', 'Smooth', 'Harsh', 'Cooling', 'Ungrouped']
    grouped_ingredients = {}
    for group_name in sensory_group_order:
        grouped_ingredients[group_name] = [ing for ing in ingredient_order if ingredient_groups.get(ing) == group_name]
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Tobacco Heatmap</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 5px;
            background-color: #f5f5f5;
            height: 100vh;
            overflow: hidden;
        }}
        
        .container {{
            display: flex;
            flex-direction: column;
            height: calc(100vh - 10px);
            width: calc(100vw - 10px);
            overflow: hidden;
        }}
        
        .top-controls {{
            background: white;
            padding: 8px 12px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 15px;
            flex-shrink: 0;
            height: 40px;
        }}
        
        .threshold-label {{
            font-size: 14px;
            font-weight: bold;
            margin-right: 5px;
            color: #333;
        }}
        
        .threshold-input {{
            padding: 5px;
            border: 2px solid #888;
            border-radius: 3px;
            font-size: 12px;
            width: 100px;
        }}
        
        .heatmap-container {{
            flex: 1;
            background: white;
            padding: 8px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: row;
            margin-bottom: 5px;
            gap: 10px;
            min-height: 0;
        }}
        
        .heatmap-wrapper {{
            flex: 1;
            overflow: auto;
            min-height: 0;
            min-width: 0;
            position: relative;
        }}
        
        .color-scale {{
            width: 60px;
            display: flex;
            flex-direction: column;
            align-items: center;
            flex-shrink: 0;
        }}
        
        .color-scale-title {{
            font-size: 10px;
            font-weight: bold;
            margin-bottom: 8px;
            text-align: center;
            color: #333;
        }}
        
        .color-scale-bar {{
            width: 16px;
            height: 150px;
            border: 1px solid #ccc;
            border-radius: 3px;
            position: relative;
            background: linear-gradient(to top, 
                rgb(68, 1, 84) 0%, 
                rgb(59, 82, 139) 25%, 
                rgb(33, 144, 141) 50%, 
                rgb(94, 201, 98) 75%, 
                rgb(253, 231, 37) 100%);
        }}
        
        .color-scale-labels {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 150px;
            margin-left: 5px;
            font-size: 9px;
            color: #666;
        }}
        
        .color-scale-label {{
            line-height: 1;
        }}
        
        .heatmap {{
            border-collapse: collapse;
            font-size: 8px;
            width: 100%;
            height: fit-content;
            table-layout: auto;
        }}
        
        .heatmap th,
        .heatmap td {{
            border: 1px solid white;
            padding: 1px;
            text-align: center;
            min-width: 8px;
            max-width: 10px;
            height: 14px;
            font-size: 7px;
        }}
        
        .heatmap th {{
            background-color: #f0f0f0;
            font-weight: bold;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .heatmap .recipe-label {{
            background-color: #f0f0f0;
            font-weight: bold;
            text-align: left;
            padding: 2px 4px;
            white-space: nowrap;
            position: sticky;
            left: 0;
            z-index: 15;
            max-width: 200px;
            min-width: 180px;
            width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            font-size: 7px;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            border-right: 2px solid #ccc;
        }}
        
        .recipe-button {{
            position: absolute;
            right: 4px;
            top: 2px;
            bottom: 2px;
            width: 16px;
            background-color: #e0e0e0;
            border: 1px solid #888;
            border-radius: 2px;
            cursor: pointer;
            font-size: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.2s;
            z-index: 16;
        }}
        
        .recipe-button:hover {{
            background-color: #d0d0d0;
        }}
        
        .recipe-button.selected {{
            background-color: #4CAF50;
            color: white;
        }}
        
        .recipe-text {{
            padding-right: 24px;
            display: block;
            width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .sensory-group-header {{
            font-weight: bold;
            font-size: 16px;
            color: #000000;
            background-color: rgba(255,255,255,0.9);
            border: 2px solid #000080;
            padding: 2px 4px;
            text-align: center;
        }}
        
        .ingredient-header {{
            writing-mode: vertical-rl;
            text-orientation: mixed;
            font-size: 7px;
            max-width: 10px;
            min-width: 8px;
            height: 100px;
            overflow: visible;
            text-overflow: clip;
            background-color: #f0f0f0;
            border: 1px solid white;
            padding: 1px;
            white-space: nowrap;
            vertical-align: top;
        }}
        
        .heatmap-cell {{
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .heatmap-cell:hover {{
            border: 2px solid #333;
        }}
        
        .sweet {{ border-top: 3px solid #FF0000; border-left: 2px solid #FF0000; }}
        .dry {{ border-top: 3px solid #00FF00; border-left: 2px solid #00FF00; }}
        .rich {{ border-top: 3px solid #FF0000; border-left: 2px solid #FF0000; }}
        .light {{ border-top: 3px solid #00FF00; border-left: 2px solid #00FF00; }}
        .smooth {{ border-top: 3px solid #FF0000; border-left: 2px solid #FF0000; }}
        .harsh {{ border-top: 3px solid #00FF00; border-left: 2px solid #00FF00; }}
        .cooling {{ border-top: 3px solid #FF0000; border-left: 2px solid #FF0000; }}
        .ungrouped {{ border-top: 3px solid #808080; border-left: 2px solid #808080; }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            z-index: 1000;
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="top-controls">
            <div class="threshold-section">
                <div class="threshold-label">Threshold:</div>
                <input type="number" id="threshold-input" class="threshold-input" 
                       value="0.4" min="0" max="1" step="0.01">
            </div>
        </div>
        
        <div class="heatmap-container">
            <div class="heatmap-wrapper">
                <table class="heatmap" id="heatmap-table">
                    <!-- Heatmap will be populated by JavaScript -->
                </table>
            </div>
            
            <div class="color-scale">
                <div class="color-scale-title">Value Scale</div>
                <div style="display: flex; align-items: flex-start;">
                    <div class="color-scale-bar"></div>
                    <div class="color-scale-labels">
                        <div class="color-scale-label">1.0</div>
                        <div class="color-scale-label">0.8</div>
                        <div class="color-scale-label">0.6</div>
                        <div class="color-scale-label">0.4</div>
                        <div class="color-scale-label">0.2</div>
                        <div class="color-scale-label">0.0</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>

    <script>
        // Data embedded from Python processing
        const heatmapData = {json.dumps(heatmap_data)};
        const recipeOrder = {json.dumps(recipe_order)};
        const ingredientOrder = {json.dumps(ingredient_order)};
        const groupedRecipes = {json.dumps(grouped_recipes)};
        const groupedIngredients = {json.dumps(grouped_ingredients)};
        const groupHeaders = {json.dumps(group_headers)};
        
        let selectedRecipes = new Set();
        let currentThreshold = 0.4;
        
        // Color scale function (viridis-like)
        function getColor(value, opacity = 1) {{
            if (value <= 0 || isNaN(value)) return `rgba(240, 240, 240, ${{opacity}})`;
            
            // Viridis color scale approximation
            const colors = [
                [68, 1, 84],      // Dark purple
                [59, 82, 139],    // Blue-purple  
                [33, 144, 141],   // Teal
                [94, 201, 98],    // Green
                [253, 231, 37]    // Yellow
            ];
            
            const scaledValue = Math.min(Math.max(value, 0), 1);
            const index = scaledValue * (colors.length - 1);
            const lowerIndex = Math.floor(index);
            const upperIndex = Math.ceil(index);
            const fraction = index - lowerIndex;
            
            if (lowerIndex === upperIndex) {{
                const [r, g, b] = colors[lowerIndex];
                return `rgba(${{r}}, ${{g}}, ${{b}}, ${{opacity}})`;
            }}
            
            const [r1, g1, b1] = colors[lowerIndex];
            const [r2, g2, b2] = colors[upperIndex];
            
            const r = Math.round(r1 + (r2 - r1) * fraction);
            const g = Math.round(g1 + (g2 - g1) * fraction);
            const b = Math.round(b1 + (b2 - b1) * fraction);
            
            return `rgba(${{r}}, ${{g}}, ${{b}}, ${{opacity}})`;
        }}
        
        // Helper functions for sensory group borders
        function getIngredientGroup(ingredient) {{
            for (const [groupName, ingredients] of Object.entries(groupedIngredients)) {{
                if (ingredients.includes(ingredient)) {{
                    return groupName;
                }}
            }}
            return 'Ungrouped';
        }}
        
        function isFirstInGroup(ingredient, colIndex) {{
            if (colIndex === 0) return true;
            const currentGroup = getIngredientGroup(ingredient);
            const prevIngredient = ingredientOrder[colIndex - 1];
            const prevGroup = getIngredientGroup(prevIngredient);
            return currentGroup !== prevGroup;
        }}
        
        function getGroupColor(groupName) {{
            const colors = {{
                'Sweet': '#FF0000',
                'Dry': '#00FF00', 
                'Rich': '#FF0000',
                'Light': '#00FF00',
                'Smooth': '#FF0000',
                'Harsh': '#00FF00',
                'Cooling': '#FF0000',
                'Ungrouped': '#808080'
            }};
            return colors[groupName] || '#808080';
        }}
        
        function getRecipeGroup(recipe) {{
            for (const [groupName, recipes] of Object.entries(groupedRecipes)) {{
                if (recipes.includes(recipe)) {{
                    return groupHeaders[groupName] || groupName;
                }}
            }}
            return '';
        }}
        
        function getDisplayRecipeName(recipe) {{
            const groupPrefix = getRecipeGroup(recipe);
            return groupPrefix ? `${{groupPrefix}}-${{recipe}}` : recipe;
        }}
        
        function toggleRecipe(recipe, button) {{
            if (selectedRecipes.has(recipe)) {{
                selectedRecipes.delete(recipe);
                button.classList.remove('selected');
            }} else {{
                selectedRecipes.add(recipe);
                button.classList.add('selected');
            }}
            updateHeatmap();
        }}
        
        function createHeatmap() {{
            const table = document.getElementById('heatmap-table');
            table.innerHTML = '';
            
            // Create sensory header row
            const sensoryHeaderRow = document.createElement('tr');
            
            // Empty cell for recipe column
            const emptyHeader = document.createElement('td');
            emptyHeader.className = 'recipe-label';
            emptyHeader.textContent = '';
            emptyHeader.style.position = 'sticky';
            emptyHeader.style.left = '0';
            emptyHeader.style.zIndex = '20';
            emptyHeader.style.backgroundColor = '#f0f0f0';
            emptyHeader.style.boxShadow = '2px 0 5px rgba(0,0,0,0.1)';
            emptyHeader.style.borderRight = '2px solid #ccc';
            sensoryHeaderRow.appendChild(emptyHeader);
            
            // Add sensory group headers
            Object.entries(groupedIngredients).forEach(([groupName, ingredients]) => {{
                if (ingredients.length === 0) return;
                
                const groupHeader = document.createElement('td');
                groupHeader.className = `sensory-group-header ${{groupName.toLowerCase()}}`;
                groupHeader.colSpan = ingredients.length;
                groupHeader.textContent = groupName;
                groupHeader.style.textAlign = 'center';
                groupHeader.style.fontWeight = 'bold';
                groupHeader.style.fontSize = '16px';
                groupHeader.style.color = 'black';
                groupHeader.style.borderBottom = '2px solid #ddd';
                sensoryHeaderRow.appendChild(groupHeader);
            }});
            table.appendChild(sensoryHeaderRow);
            
            // Create data rows
            recipeOrder.forEach((recipe, rowIndex) => {{
                const row = document.createElement('tr');
                
                // Recipe label with button
                const labelCell = document.createElement('td');
                labelCell.className = 'recipe-label';
                labelCell.title = getDisplayRecipeName(recipe);
                
                // Create recipe text span
                const recipeText = document.createElement('span');
                recipeText.className = 'recipe-text';
                recipeText.textContent = getDisplayRecipeName(recipe);
                
                // Create recipe button
                const recipeButton = document.createElement('button');
                recipeButton.className = 'recipe-button';
                recipeButton.textContent = '●';
                recipeButton.title = `Click to select/deselect ${{getDisplayRecipeName(recipe)}}`;
                recipeButton.onclick = () => toggleRecipe(recipe, recipeButton);
                
                labelCell.appendChild(recipeText);
                labelCell.appendChild(recipeButton);
                row.appendChild(labelCell);
                
                // Data cells
                ingredientOrder.forEach((ingredient, colIndex) => {{
                    const cell = document.createElement('td');
                    cell.className = 'heatmap-cell';
                    cell.dataset.recipe = recipe;
                    cell.dataset.ingredient = ingredient;
                    cell.dataset.value = heatmapData[rowIndex][colIndex];
                    
                    // Add sensory group border styling
                    const ingredientGroup = getIngredientGroup(ingredient);
                    if (ingredientGroup) {{
                        cell.classList.add(ingredientGroup.toLowerCase());
                    }}
                    
                    // Add left border for first ingredient in each group
                    if (isFirstInGroup(ingredient, colIndex)) {{
                        cell.style.borderLeft = `3px solid ${{getGroupColor(ingredientGroup)}}`;
                    }}
                    
                    // Add tooltip functionality
                    cell.addEventListener('mouseenter', showTooltip);
                    cell.addEventListener('mouseleave', hideTooltip);
                    cell.addEventListener('mousemove', moveTooltip);
                    
                    row.appendChild(cell);
                }});
                
                table.appendChild(row);
            }});
            
            // Create ingredient names row at the bottom
            const ingredientRow = document.createElement('tr');
            
            // Empty cell for recipe column
            const emptyFooter = document.createElement('td');
            emptyFooter.className = 'recipe-label';
            emptyFooter.textContent = '';
            emptyFooter.style.position = 'sticky';
            emptyFooter.style.left = '0';
            emptyFooter.style.zIndex = '20';
            emptyFooter.style.backgroundColor = '#f0f0f0';
            emptyFooter.style.boxShadow = '2px 0 5px rgba(0,0,0,0.1)';
            emptyFooter.style.borderRight = '2px solid #ccc';
            ingredientRow.appendChild(emptyFooter);
            
            // Add ingredient names
            ingredientOrder.forEach(ingredient => {{
                const ingredientCell = document.createElement('td');
                ingredientCell.className = 'ingredient-header';
                ingredientCell.textContent = ingredient;
                ingredientCell.title = ingredient;
                ingredientCell.style.fontSize = '10px';
                ingredientCell.style.textAlign = 'center';
                ingredientCell.style.writingMode = 'vertical-rl';
                ingredientCell.style.textOrientation = 'mixed';
                ingredientCell.style.padding = '4px 2px';
                ingredientRow.appendChild(ingredientCell);
            }});
            
            table.appendChild(ingredientRow);
        }}
        
        function updateHeatmap() {{
            const cells = document.querySelectorAll('.heatmap-cell');
            
            cells.forEach(cell => {{
                const recipe = cell.dataset.recipe;
                const value = parseFloat(cell.dataset.value);
                const isSelected = selectedRecipes.has(recipe);
                const isAboveThreshold = value >= currentThreshold;
                
                if (isAboveThreshold) {{
                    if (selectedRecipes.size > 0 && isSelected) {{
                        // Show in full color only if selected
                        cell.style.backgroundColor = getColor(value, 1);
                        cell.textContent = '';
                    }} else {{
                        // Show gray for deactivated rows
                        cell.style.backgroundColor = '#d3d3d3';
                        cell.textContent = '';
                    }}
                }} else {{
                    // Below threshold - light gray
                    cell.style.backgroundColor = '#f0f0f0';
                    cell.textContent = '';
                }}
            }});
        }}
        
        function showTooltip(event) {{
            const tooltip = document.getElementById('tooltip');
            const recipe = event.target.dataset.recipe;
            const ingredient = event.target.dataset.ingredient;
            const value = event.target.dataset.value;
            
            tooltip.innerHTML = `
                <strong>Recipe:</strong> ${{recipe}}<br>
                <strong>Ingredient:</strong> ${{ingredient}}<br>
                <strong>Value:</strong> ${{value}}
            `;
            tooltip.style.display = 'block';
        }}
        
        function hideTooltip() {{
            const tooltip = document.getElementById('tooltip');
            tooltip.style.display = 'none';
        }}
        
        function moveTooltip(event) {{
            const tooltip = document.getElementById('tooltip');
            tooltip.style.left = event.pageX + 10 + 'px';
            tooltip.style.top = event.pageY + 10 + 'px';
        }}
        
        // Threshold input handler
        document.getElementById('threshold-input').addEventListener('input', function(event) {{
            currentThreshold = parseFloat(event.target.value) || 0;
            updateHeatmap();
        }});
        
        // Initialize the heatmap
        function initialize() {{
            createHeatmap();
            updateHeatmap();
            
            console.log('Interactive Tobacco Heatmap loaded successfully!');
            console.log(`Recipes: ${{recipeOrder.length}}, Ingredients: ${{ingredientOrder.length}}`);
        }}
        
        // Start the application
        initialize();
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """Main function to generate the standalone HTML file"""
    # Load data
    df, sensory_df = load_and_process_data()
    if df is None or sensory_df is None:
        print("❌ Failed to load data. Exiting.")
        return
    
    # Define groups
    tobacco_groups = define_recipe_groups()
    sensory_groups = create_sensory_groups(df, sensory_df)
    
    # Organize data
    recipe_order, ingredient_order, recipe_groups, ingredient_groups = organize_data(
        df, tobacco_groups, sensory_groups
    )
    
    # Generate HTML
    print("\n🌐 GENERATING HTML FILE")
    print("-" * 40)
    
    html_content = generate_html_file(
        df, recipe_order, ingredient_order, recipe_groups, ingredient_groups, tobacco_groups
    )
    
    # Save HTML file
    output_file = 'tobacco_heatmap_standalone.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = os.path.getsize(output_file) / 1024  # KB
    
    print(f"✅ HTML file generated: {output_file}")
    print(f"📁 File size: {file_size:.1f} KB")
    print(f"📊 Data included:")
    print(f"   - {len(recipe_order)} recipes")
    print(f"   - {len(ingredient_order)} ingredients")
    print(f"   - {len(tobacco_groups)} recipe groups")
    print(f"   - {len([g for g in sensory_groups.values() if g])} sensory groups")
    
    print("\n" + "=" * 70)
    print("🎉 STANDALONE HEATMAP READY!")
    print(f"📂 Open '{output_file}' in any web browser")
    print("💡 Features:")
    print("   - Click recipe buttons to highlight rows")
    print("   - Adjust threshold to filter low values")
    print("   - Hover over cells for detailed information")
    print("   - No Python installation required!")
    print("=" * 70)

if __name__ == "__main__":
    main()
