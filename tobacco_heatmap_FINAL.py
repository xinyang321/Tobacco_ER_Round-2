#!/usr/bin/env python3
"""
TOBACCO HEATMAP - FINAL VERSION
===============================
This is the ONE AND ONLY heatmap file you need!

Features:
- Interactive heatmap with visible dropdown filters
- Recipe groups organized by G1-G4 (no borderlines)
- Ingredients organized by sensory note groups
- Multiple output options: static PNG, interactive HTML
- Clear data analysis and statistics

Usage: python tobacco_heatmap_FINAL.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
import warnings
warnings.filterwarnings('ignore')

def load_and_process_data():
    """Load and process the tobacco data"""
    print("=" * 70)
    print("🚭 TOBACCO HEATMAP - FINAL VERSION")
    print("Loading and processing data...")
    print("=" * 70)
    
    # Load main data
    try:
        df = pd.read_excel('Data_Raw.xlsx', index_col=0)
        print(f"✅ Loaded main data: {df.shape[0]} recipes × {df.shape[1]} ingredients")
    except Exception as e:
        print(f"❌ Error loading Data_Raw.xlsx: {e}")
        return None, None, None, None
    
    # Load sensory notes
    try:
        sensory_df = pd.read_excel('Sensory_Note.xlsx')
        print(f"✅ Loaded sensory notes: {len(sensory_df)} ingredient classifications")
    except Exception as e:
        print(f"❌ Error loading Sensory_Note.xlsx: {e}")
        return None, None, None, None
    
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
            print(f"    Ungrouped ingredients: {', '.join(ingredients)}")
    
    return sensory_groups

def order_data_by_groups(df, tobacco_groups, sensory_groups):
    """Order recipes and ingredients by their groups"""
    print("\n📊 DATA ORGANIZATION")
    print("-" * 40)
    
    # Order recipes by groups
    recipe_order = []
    grouped_recipes = {}
    
    for group_name, recipes in tobacco_groups.items():
        print(f"  {group_name}: {len(recipes)} recipes")
        for recipe in recipes:
            if recipe in df.index:
                recipe_order.append(recipe)
                grouped_recipes[recipe] = group_name
    
    # Order ingredients by sensory groups
    ingredient_order = []
    for group_name in ['Sweet', 'Dry', 'Rich', 'Light', 'Smooth', 'Harsh', 'Cooling']:
        for ingredient in sensory_groups[group_name]:
            if ingredient in df.columns:
                ingredient_order.append(ingredient)
    
    return recipe_order, ingredient_order, grouped_recipes

def create_static_heatmap(df, recipe_order, ingredient_order, save_file=True):
    """Create a static heatmap with matplotlib/seaborn"""
    print("\n🎨 CREATING STATIC HEATMAP")
    print("-" * 40)
    
    # Reorder data
    df_plot = df.loc[recipe_order, ingredient_order]
    
    # Apply threshold (show only values > 0.45)
    df_display = df_plot.copy()
    df_display[df_display <= 0.45] = np.nan
    
    # Create the plot
    plt.figure(figsize=(20, 12))
    
    # Create heatmap
    mask = df_display.isna()
    sns.heatmap(df_display, 
                annot=False, 
                cmap='viridis', 
                mask=mask,
                cbar_kws={'label': 'Concentration'},
                xticklabels=True, 
                yticklabels=True)
    
    plt.title('🚭 Tobacco Recipes Heatmap\nRecipes by G1-G4 Groups × Ingredients by Sensory Notes', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('🧪 Ingredients (Grouped by Sensory Notes)', fontsize=12, fontweight='bold')
    plt.ylabel('🌿 Tobacco Recipes (Grouped by G1-G4)', fontsize=12, fontweight='bold')
    
    # Rotate labels for better readability
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=10)
    
    plt.tight_layout()
    
    if save_file:
        filename = 'tobacco_heatmap_static.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ Static heatmap saved as: {filename}")
    
    plt.show()
    
    # Print statistics
    total_values = df_display.notna().sum().sum()
    total_possible = df_display.shape[0] * df_display.shape[1]
    print(f"📈 Heatmap statistics:")
    print(f"   Total data points shown: {total_values} out of {total_possible} possible")
    print(f"   Data density: {total_values/total_possible:.1%}")
    print(f"   Threshold: Values > 0.45 shown, others hidden")

def create_interactive_heatmap(df, recipe_order, ingredient_order, grouped_recipes, tobacco_groups, save_file=True):
    """Create an interactive heatmap with dropdown filters"""
    print("\n🎯 CREATING INTERACTIVE HEATMAP")
    print("-" * 40)
    
    # Reorder data
    df_plot = df.loc[recipe_order, ingredient_order]
    
    # Apply threshold
    df_display = df_plot.copy()
    df_display[df_display <= 0.45] = np.nan
    
    # Create traces for each group
    traces = []
    
    # All groups trace
    traces.append(
        go.Heatmap(
            z=df_display.values,
            x=df_display.columns,
            y=df_display.index,
            colorscale='viridis',
            showscale=True,
            hovertemplate='<b>Recipe:</b> %{y}<br><b>Ingredient:</b> %{x}<br><b>Value:</b> %{z:.3f}<extra></extra>',
            colorbar=dict(
                title=dict(text="Concentration"),
                tickvals=[0.45, 0.6, 0.75, 0.9, 1.0],
                ticktext=["0.45", "0.6", "0.75", "0.9", "1.0"]
            ),
            zmin=0.45,
            zmax=1.0
        )
    )
    
    # Individual group traces
    for group_name, group_recipes in tobacco_groups.items():
        group_df = df_display.loc[group_recipes]
        traces.append(
            go.Heatmap(
                z=group_df.values,
                x=group_df.columns,
                y=group_df.index,
                colorscale='viridis',
                showscale=True,
                visible=False,
                hovertemplate='<b>Recipe:</b> %{y}<br><b>Ingredient:</b> %{x}<br><b>Value:</b> %{z:.3f}<extra></extra>',
                colorbar=dict(
                    title=dict(text="Concentration"),
                    tickvals=[0.45, 0.6, 0.75, 0.9, 1.0],
                    ticktext=["0.45", "0.6", "0.75", "0.9", "1.0"]
                ),
                zmin=0.45,
                zmax=1.0
            )
        )
    
    # Create figure
    fig = go.Figure(data=traces)
    
    # Create dropdown buttons
    dropdown_buttons = []
    
    # All groups button
    dropdown_buttons.append(
        dict(
            label="📊 ALL GROUPS (18 recipes)",
            method="update",
            args=[
                {"visible": [True] + [False] * len(tobacco_groups)},
                {"title": "🚭 ALL RECIPE GROUPS - Tobacco Heatmap<br><sub>Recipes by G1-G4 Groups × Ingredients by Sensory Notes</sub>"}
            ]
        )
    )
    
    # Individual group buttons
    for i, (group_name, group_recipes) in enumerate(tobacco_groups.items()):
        visible_list = [False] * (len(tobacco_groups) + 1)
        visible_list[i + 1] = True
        
        dropdown_buttons.append(
            dict(
                label=f"🎯 {group_name.upper()} ({len(group_recipes)} recipes)",
                method="update",
                args=[
                    {"visible": visible_list},
                    {"title": f"🚭 {group_name.upper()} - Tobacco Heatmap<br><sub>Recipes by G1-G4 Groups × Ingredients by Sensory Notes</sub>"}
                ]
            )
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': "🚭 ALL RECIPE GROUPS - Tobacco Heatmap<br><sub>Recipes by G1-G4 Groups × Ingredients by Sensory Notes</sub>",
            'x': 0.5,
            'font': {'size': 20, 'color': 'darkblue'}
        },
        xaxis=dict(
            title=dict(text="🧪 Ingredients (Grouped by Sensory Notes)", font=dict(size=14, color='darkgreen')),
            tickangle=90,
            tickfont=dict(size=9),
            side="bottom"
        ),
        yaxis=dict(
            title=dict(text="🌿 Tobacco Recipes (Grouped by G1-G4)", font=dict(size=14, color='darkgreen')),
            tickfont=dict(size=10)
        ),
        width=1600,
        height=900,
        margin=dict(t=120, l=150, r=150, b=150),
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction="down",
                showactive=True,
                x=0.01,
                xanchor="left",
                y=0.99,
                yanchor="top",
                bgcolor="lightblue",
                bordercolor="navy",
                borderwidth=2,
                font=dict(size=12, color="navy"),
                pad={"r": 10, "t": 10}
            )
        ],
        annotations=[
            dict(
                text="👆 Use the dropdown menu above to filter recipe groups",
                showarrow=False,
                x=0.01,
                y=0.93,
                xref="paper",
                yref="paper",
                font=dict(size=14, color="red", family="Arial Black"),
                bgcolor="yellow",
                bordercolor="red",
                borderwidth=1
            )
        ]
    )
    
    # Show statistics
    total_values = df_display.notna().sum().sum()
    total_possible = df_display.shape[0] * df_display.shape[1]
    print(f"📈 Heatmap statistics:")
    print(f"   Total data points shown: {total_values} out of {total_possible} possible")
    print(f"   Data density: {total_values/total_possible:.1%}")
    print(f"   Threshold: Values > 0.45 shown, others hidden")
    
    # Save the plot
    if save_file:
        filename = 'tobacco_heatmap_interactive_FINAL.html'
        fig.write_html(filename)
        print(f"✅ Interactive plot saved as: {filename}")
    
    fig.show()
    
    return fig

def create_dash_server():
    """Create and configure the Dash server"""
    print("🚀 Starting Tobacco Heatmap Server...")
    
    # Load data
    df, sensory_df = load_and_process_data()
    if df is None:
        print("❌ Failed to load data. Exiting.")
        return None
    
    # Define groups
    tobacco_groups = define_recipe_groups()
    sensory_groups = create_sensory_groups(df, sensory_df)
    
    # Order data
    recipe_order, ingredient_order, grouped_recipes = order_data_by_groups(df, tobacco_groups, sensory_groups)
    
    print(f"\n✅ DATA READY:")
    print(f"   Recipes ordered: {len(recipe_order)}")
    print(f"   Ingredients ordered: {len(ingredient_order)}")
    
    # Initialize Dash app
    app = dash.Dash(__name__)
    
    # Define app layout
    app.layout = html.Div([
        dcc.Graph(
            id='heatmap-graph',
            style={'height': '800px'}
        )
    ], style={'padding': '20px'})
    
    # Create static heatmap figure
    def create_heatmap_figure():
        """Create the static heatmap figure showing all recipes"""
        try:
            # Show all recipes
            filtered_recipes = recipe_order
            title_suffix = "ALL RECIPE GROUPS"
            
            # Filter data for all recipes
            filtered_df = df[df.index.isin(filtered_recipes)]
            filtered_df = filtered_df.reindex(filtered_recipes)
            
            # Create heatmap data
            heatmap_data = filtered_df[ingredient_order].fillna(0)
            
            # Show all ingredient values (no filtering)
            # Keep all values including zeros and low concentrations
            # Convert zeros to NaN for white display
            heatmap_display = heatmap_data.where(heatmap_data > 0, np.nan)
            
            # Create the heatmap
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_display.values,
                x=ingredient_order,
                y=filtered_recipes,
                colorscale='viridis',
                hovertemplate='<b>Recipe:</b> %{y}<br><b>Ingredient:</b> %{x}<br><b>Value:</b> %{z}<extra></extra>',
                colorbar=dict(
                    title="Concentration",
                    tickvals=[0.1, 0.2, 0.4, 0.6, 0.8, 1.0],
                    ticktext=["0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
                ),
                zmin=0.01,  # Start slightly above 0 so the colorscale works properly
                zmax=1.0,
                showscale=True,
                connectgaps=False  # This ensures NaN values appear as gaps (white)
            ))
            
            # Add red vertical lines to separate sensory groups
            sensory_group_order = ['Sweet', 'Dry', 'Rich', 'Light', 'Smooth', 'Harsh', 'Cooling']
            x_position = 0
            
            for group_name in sensory_group_order:
                if group_name in sensory_groups:
                    group_ingredients = [ing for ing in ingredient_order if ing in sensory_groups[group_name]]
                    if group_ingredients and x_position > 0:  # Don't add line before first group
                        fig.add_vline(
                            x=x_position - 0.5,
                            line=dict(color="red", width=2),
                            layer="above"
                        )
                    
                    # Add sensory group title at the top of each block
                    if group_ingredients:
                        # Calculate the center position of the group
                        group_center = x_position + (len(group_ingredients) - 1) / 2
                        
                        fig.add_annotation(
                            x=group_center,
                            y=len(filtered_recipes) - 0.3,  # Position above the heatmap
                            text=f"<b>{group_name}</b>",
                            showarrow=False,
                            font=dict(size=12, color="darkblue"),
                            bgcolor="white",
                            bordercolor="darkblue",
                            borderwidth=1,
                            xanchor="center",
                            yanchor="bottom"
                        )
                    
                    x_position += len(group_ingredients)
            
            # Add red horizontal lines to separate recipe groups (G1-G4)
            y_position = 0
            group_mapping = {
                'G1 - MGO and Filed': 'G1',
                'G2': 'G2', 
                'G3': 'G3',
                'G4 - Unique': 'G4'
            }
            
            for group_name in ['G1 - MGO and Filed', 'G2', 'G3', 'G4 - Unique']:
                if group_name in tobacco_groups:
                    group_recipes = [recipe for recipe in filtered_recipes if recipe in tobacco_groups[group_name]]
                    if group_recipes and y_position > 0:  # Don't add line before first group
                        fig.add_hline(
                            y=y_position - 0.5,
                            line=dict(color="red", width=2),
                            layer="above"
                        )
                    
                    # Add recipe group title on the left side of each block
                    if group_recipes:
                        # Calculate the center position of the group
                        group_center = y_position + (len(group_recipes) - 1) / 2
                        
                        # Use simplified group name
                        simple_name = group_mapping[group_name]
                        
                        fig.add_annotation(
                            x=-2,  # Position to the left of the heatmap
                            y=group_center,
                            text=f"<b>{simple_name}</b>",
                            showarrow=False,
                            font=dict(size=12, color="darkgreen"),
                            bgcolor="white",
                            bordercolor="darkgreen", 
                            borderwidth=1,
                            xanchor="right",
                            yanchor="middle",
                            textangle=90  # Rotate text vertically
                        )
                    
                    y_position += len(group_recipes)
            
            # Update layout
            fig.update_layout(
                xaxis=dict(
                    tickfont={'size': 9},
                    tickangle=90,
                    side='bottom',
                    showgrid=True,
                    gridcolor='white',
                    gridwidth=1,
                    dtick=1,
                    tick0=0
                ),
                yaxis=dict(
                    tickfont={'size': 10},
                    showgrid=True,
                    gridcolor='white',
                    gridwidth=1,
                    dtick=1,
                    tick0=0
                ),
                margin=dict(t=40, l=150, r=150, b=150),
                height=800,
                width=1600
            )
            
            return fig
            
        except Exception as e:
            print(f"❌ Error creating heatmap: {e}")
            return go.Figure().add_annotation(
                text=f"Error: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    
    # Set the static figure
    static_fig = create_heatmap_figure()
    
    # Update the graph component to use the static figure
    app.layout.children[0].figure = static_fig
    
    return app

def main():
    """Main function to run the server"""
    app = create_dash_server()
    if app is None:
        print("❌ Failed to create server. Exiting.")
        return
    
    print("\n" + "=" * 70)
    print("🎉 TOBACCO HEATMAP SERVER READY!")
    print("📡 Server starting on: http://localhost:8050")
    print("🌐 Open your browser and navigate to the URL above")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 70)
    
    # Run the server
    app.run(debug=True, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    main()
