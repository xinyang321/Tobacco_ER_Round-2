#!/usr/bin/env python3
import dash
from dash import dcc, html
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

def create_dash_server():
    """Create and configure the Dash server"""
    print("🚀 Starting Tobacco Heatmap Server...")

    # Initialize Dash app FIRST
    app = dash.Dash(__name__)

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
    
    # Create heatmap figure with row/column highlighting
    def create_heatmap_figure(selected_recipes=None):
        if selected_recipes is None:
            selected_recipes = []
        
        # Use global threshold toggle if available
        threshold = getattr(create_heatmap_figure, "threshold", 0.4)
        
        filtered_recipes = recipe_order
        heatmap_data = df[df.index.isin(filtered_recipes)]
        heatmap_data = heatmap_data.reindex(filtered_recipes)
        
        # Apply threshold filtering
        z_df = heatmap_data[ingredient_order].copy()
        if threshold > 0:
            z_df[z_df < threshold] = np.nan
        z = z_df.values
        
        # Create masks for highlighting
        mask = np.ones(z.shape, dtype=bool)
        highlight_mask = np.zeros(z.shape, dtype=bool)
        for i, y_val in enumerate(filtered_recipes):
            if y_val in selected_recipes:
                for j, x_val in enumerate(ingredient_order):
                    highlight_mask[i, j] = True
                    mask[i, j] = False
        
        # Create figure
        fig = go.Figure()
        
        # Add faded trace
        faded_z = np.where(mask, z, np.nan)
        fig.add_trace(go.Heatmap(
            z=faded_z,
            x=ingredient_order,
            y=filtered_recipes,
            colorscale=[
                [0, 'rgb(240,240,240)'],
                [1, 'rgb(200,200,200)']
            ],
            showscale=False,
            hoverinfo='skip',
            zmin=0.01,
            zmax=1.0,
            name='Faded',
            ygap=1
        ))
        
        # Add highlighted trace
        highlight_z = np.where((highlight_mask) & (~np.isnan(z)), z, np.nan)
        fig.add_trace(go.Heatmap(
            z=highlight_z,
            x=ingredient_order,
            y=filtered_recipes,
            colorscale='viridis',
            hovertemplate='<b>Recipe:</b> %{y}<br><b>Ingredient:</b> %{x}<br><b>Value:</b> %{z}<extra></extra>',
            colorbar=dict(
                title="Concentration",
                tickvals=[0.1, 0.2, 0.4, 0.6, 0.8, 1.0],
                ticktext=["0.1", "0.2", "0.4", "0.6", "0.8", "1.0"]
            ),
            zmin=0.01,
            zmax=1.0,
            showscale=True,
            name='Highlight',
            ygap=1
        ))
        
        # Add colored borderlines for each sensory group
        sensory_group_order = ['Sweet', 'Dry', 'Rich', 'Light', 'Smooth', 'Harsh', 'Cooling']
        # Define border colors for different group pairs
        border_colors = {
            'Sweet': 'red', 'Dry': 'green',  # Sweet-Dry boundary will be green
            'Rich': 'red', 'Light': 'green',  # Rich-Light boundary will be green
            'Smooth': 'red', 'Harsh': 'green',  # Smooth-Harsh boundary will be green
            'Cooling': 'red'
        }
        x_position = 0
        for group_name in sensory_group_order:
            group_ingredients = [ing for ing in ingredient_order if ing in sensory_groups.get(group_name, [])]
            if group_ingredients:
                start_x = x_position - 0.5
                end_x = x_position + len(group_ingredients) - 0.5
                # Use specific color for this group
                border_color = border_colors.get(group_name, 'red')
                # Draw rectangle with specific border color around the sensory group
                fig.add_shape(
                    type="rect",
                    xref="x",
                    yref="paper",
                    x0=start_x,
                    x1=end_x,
                    y0=0,
                    y1=1,
                    line=dict(color=border_color, width=3),
                    fillcolor="rgba(0,0,0,0)",
                    layer="above"
                )
                # Add sensory group title annotation above the group
                group_center = x_position + (len(group_ingredients) - 1) / 2
                fig.add_annotation(
                    x=group_center,
                    y=1.02,  # Reduced spacing - closer to the heatmap
                    xref="x",
                    yref="paper",
                    text=f"<b>{group_name}</b>",
                    showarrow=False,
                    font=dict(size=16, color="darkblue", family="Arial Black"),
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="darkblue",
                    borderwidth=2,
                    borderpad=4,
                    xanchor="center",
                    yanchor="bottom"
                )
                x_position += len(group_ingredients)
        
        # Update layout
        fig.update_layout(
            xaxis=dict(
                tickfont={'size': 9},
                tickangle=90,
                side='bottom',
                showgrid=True,
                gridcolor='white',
                gridwidth=1
            ),
            yaxis=dict(
                tickfont={'size': 10},
                showgrid=True,
                gridcolor='white',
                gridwidth=1
            ),
            margin=dict(t=80, l=150, r=150, b=150),  # Reduced top margin for less spacing
            height=800,
            width=1600
        )
        
        return fig
    
    # Helper function for button styles
    def get_button_styles(n_clicks_list):
        return [
            {'margin': '2px', 'fontSize': '10px', 'display': 'block', 'width': '140px',
             'backgroundColor': '#bdbdbd' if n_clicks % 2 == 1 else '#f5f5f5',
             'color': 'black', 'border': '1px solid #888'}
            for n_clicks in n_clicks_list
        ]
    
    # Create button groups
    group_headers = {
        'G1 - MGO and Filed': 'G1',
        'G2': 'G2',
        'G3': 'G3',
        'G4 - Unique': 'G4'
    }
    button_groups = []
    btn_index = 0
    for group_name in ['G1 - MGO and Filed', 'G2', 'G3', 'G4 - Unique']:
        group_recipes = tobacco_groups.get(group_name, [])
        if group_recipes:
            button_groups.append(html.Div([
                html.Div(f"{group_headers[group_name]}", style={
                    'fontWeight': 'bold', 'fontSize': '13px', 'color': 'darkred', 'margin': '8px 0 2px 0', 'textAlign': 'right'}),
                html.Div([
                    html.Button(recipe, id={'type': 'recipe-btn', 'index': btn_index + i}, n_clicks=0,
                                style={'margin': '2px', 'fontSize': '10px', 'display': 'block', 'width': '140px', 'backgroundColor': '#f5f5f5', 'color': 'black', 'border': '1px solid #888'})
                    for i, recipe in enumerate(group_recipes)
                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-end'})
            ], style={'marginBottom': '10px'}))
            btn_index += len(group_recipes)
    
    # Create initial figure
    initial_fig = create_heatmap_figure()
    
    # Create app layout
    app.layout = html.Div([
        html.Div([
            html.Div(button_groups, id='recipe-btn-container', style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-end', 'height': '800px', 'justifyContent': 'center', 'marginRight': '0px'}),
            html.Div([
                html.Label("Threshold:", style={'fontSize': '12px', 'fontWeight': 'bold', 'color': 'black', 'marginBottom': '5px'}),
                dcc.Input(
                    id="threshold-input",
                    type="number",
                    value=0.4,
                    min=0,
                    max=1,
                    step=0.01,
                    style={'width': '140px', 'fontSize': '12px', 'padding': '5px', 'border': '2px solid #888'}
                )
            ], style={'margin': '10px 0 0 0'})
        ], style={'position': 'absolute', 'left': '0px', 'top': '60px', 'zIndex': 2}),
        html.Div([
            dcc.Graph(
                id='heatmap-graph',
                figure=initial_fig,
                style={'height': '800px', 'marginLeft': '150px'}
            )
        ], style={'position': 'relative'})
    ], style={'padding': '20px', 'position': 'relative', 'height': '900px'})

    # Callback to update button styles
    from dash.dependencies import Input, Output, State, ALL
    @app.callback(
        Output('recipe-btn-container', 'children'),
        [Input({'type': 'recipe-btn', 'index': ALL}, 'n_clicks')]
    )
    def update_button_styles(n_clicks_list):
        styles = get_button_styles(n_clicks_list)
        button_groups = []
        btn_index = 0
        for group_name in ['G1 - MGO and Filed', 'G2', 'G3', 'G4 - Unique']:
            group_recipes = tobacco_groups.get(group_name, [])
            if group_recipes:
                button_groups.append(html.Div([
                    html.Div(f"{group_headers[group_name]}", style={
                        'fontWeight': 'bold', 'fontSize': '13px', 'color': 'darkred', 'margin': '8px 0 2px 0', 'textAlign': 'right'}),
                    html.Div([
                        html.Button(recipe, id={'type': 'recipe-btn', 'index': btn_index + i}, n_clicks=n_clicks_list[btn_index + i],
                                    style=styles[btn_index + i])
                        for i, recipe in enumerate(group_recipes)
                    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-end'})
                ], style={'marginBottom': '10px'}))
                btn_index += len(group_recipes)
        return button_groups

    # Callback for threshold input
    @app.callback(
        Output('heatmap-graph', 'figure'),
        [Input('threshold-input', 'value'),
         Input({'type': 'recipe-btn', 'index': ALL}, 'n_clicks')]
    )
    def update_threshold(threshold_value, recipe_n_clicks):
        # Set the threshold based on input value
        if threshold_value is not None and threshold_value >= 0:
            create_heatmap_figure.threshold = threshold_value
        else:
            create_heatmap_figure.threshold = 0
        
        # Determine selected recipes
        selected_recipes = [recipe_order[i] for i, clicks in enumerate(recipe_n_clicks) if clicks % 2 == 1]
        fig = create_heatmap_figure(selected_recipes)
        return fig

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
