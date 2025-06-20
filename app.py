import dash
from dash import html, dash_table, dcc, callback, Input, Output, State
import pandas as pd
import plotly.express as px

# Load Excel file
path = "final_output.xlsx"

df = pd.read_excel(path)

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #0f1419 0%, #1a252f 50%, #2c3e50 100%);
                min-height: 100vh;
            }
            
            .main-container {
                background: linear-gradient(135deg, #0f1419 0%, #1a252f 50%, #2c3e50 100%);
                min-height: 100vh;
                padding: 0;
            }
            
            .header-section {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                padding: 2rem 0;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
                position: relative;
                overflow: hidden;
            }
            
            .header-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
                opacity: 0.3;
            }
            
            .main-title {
                color: white;
                font-size: 3rem;
                font-weight: 700;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                position: relative;
                z-index: 1;
            }
            
            .subtitle {
                color: rgba(255,255,255,0.8);
                font-size: 1.2rem;
                margin-top: 0.5rem;
                position: relative;
                z-index: 1;
            }
            
            .stats-container {
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin: 2rem 0;
                flex-wrap: wrap;
            }
            
            .stat-card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 15px;
                padding: 1.5rem;
                text-align: center;
                min-width: 150px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            
            .stat-number {
                font-size: 2rem;
                font-weight: 700;
                color: #4CAF50;
                display: block;
            }
            
            .stat-label {
                color: rgba(255,255,255,0.8);
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }
            
            .table-container {
                margin: 2rem;
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            
            .table-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .table-title {
                color: white;
                font-size: 1.8rem;
                font-weight: 600;
                margin: 0;
            }
            
            .controls-container {
                display: flex;
                align-items: center;
                gap: 1rem;
                flex-wrap: wrap;
                justify-content: flex-end;
            }
            
            .search-input:focus {
                border-color: #4CAF50 !important;
                box-shadow: 0 0 20px rgba(76, 175, 80, 0.3) !important;
            }
            
            .action-button {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                border: none;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                min-width: 140px;
                justify-content: center;
            }
            
            .action-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
            }
            
            .action-button:disabled {
                background: rgba(255,255,255,0.1);
                color: rgba(255,255,255,0.5);
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .secondary-button {
                background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            }
            
            .secondary-button:hover {
                box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
            }
            
            .filter-badge {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 500;
            }
            
            .selection-info {
                background: rgba(76, 175, 80, 0.1);
                border: 1px solid rgba(76, 175, 80, 0.3);
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 1rem;
                color: #4CAF50;
                text-align: center;
                font-weight: 500;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    # Store for filtered data
    dcc.Store(id='filtered-data-store', data=df.to_dict('records')),
    
    # Header Section
    html.Div([
        html.H1("PROJET KEMER", className="main-title"),
        html.P("Custom list AR", className="subtitle"),
        
        # Stats Cards
        html.Div([
            html.Div([
                html.Span(str(len(df)), className="stat-number", id="total-players-stat"),
                html.Div("Total Players", className="stat-label")
            ], className="stat-card"),
            
            html.Div([
                html.Span("0", className="stat-number", id="selected-players-stat"),
                html.Div("Selected", className="stat-label")
            ], className="stat-card"),
            
            html.Div([
                html.Span("algofut", className="stat-number"),
                html.Div("valeur rand 1", className="stat-label")
            ], className="stat-card"),
            
            html.Div([
                html.Span("93%", className="stat-number"),
                html.Div("valeur rand 2", className="stat-label")
            ], className="stat-card"),
        ], className="stats-container")
    ], className="header-section"),
    
    # Main Table Container
    html.Div([
        html.Div([
            html.H2("liste joueurs", className="table-title"),
            html.Div([
                # Search Bar
                html.Div([
                    html.I(className="fas fa-search", style={'position': 'absolute', 'left': '15px', 'top': '50%', 'transform': 'translateY(-50%)', 'color': 'rgba(255,255,255,0.5)', 'zIndex': '1'}),
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Search players...",
                        value="",
                        style={
                            'background': 'rgba(255,255,255,0.1)',
                            'border': '1px solid rgba(255,255,255,0.3)',
                            'borderRadius': '25px',
                            'padding': '0.8rem 1.5rem 0.8rem 3rem',
                            'color': 'white',
                            'fontSize': '0.9rem',
                            'minWidth': '300px',
                            'outline': 'none',
                            'transition': 'all 0.3s ease'
                        }
                    )
                ], style={'position': 'relative', 'display': 'inline-block'}),
                
                html.Button([
                    html.I(className="fas fa-filter", style={'marginRight': '0.5rem'}),
                    "Keep Selected"
                ], id="keep-selected-btn", className="action-button", disabled=True),
                
                html.Button([
                    html.I(className="fas fa-undo", style={'marginRight': '0.5rem'}),
                    "Show All"
                ], id="show-all-btn", className="action-button secondary-button"),
                
                html.A([
                    html.I(className="fas fa-download", style={'marginRight': '0.5rem'}),
                    "Export CSV"
                ], id="export-csv-btn", className="action-button", download="players_data.csv"),
                
                html.Span("Live Data", className="filter-badge"),
            ], className="controls-container")
        ], className="table-header"),
        
        # Selection info
        html.Div(id="selection-info", children=[], style={'display': 'none'}),
        
        # Enhanced DataTable
        dash_table.DataTable(
            id='players-table',
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
            
            # Table functionality
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=20,
            
            # Enhanced styling
            style_table={
                'overflowX': 'auto',
                'border': 'none',
                'borderRadius': '15px',
                'backgroundColor': 'transparent',
            },
            
            style_header={
                'backgroundColor': 'rgba(30, 60, 114, 0.9)',
                'color': 'white',
                'fontWeight': '600',
                'border': '1px solid rgba(255,255,255,0.1)',
                'textAlign': 'center',
                'padding': '15px 8px',
                'fontSize': '0.9rem',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px',
            },
            
            style_cell={
                'backgroundColor': 'transparent',
                'color': 'white',
                'textAlign': 'center',
                'padding': '12px 8px',
                'border': '1px solid rgba(255,255,255,0.05)',
                'minWidth': '120px',
                'width': '150px',
                'maxWidth': '200px',
                'whiteSpace': 'normal',
                'fontSize': '0.85rem',
                'fontWeight': '400',
            },
            
            style_data={
                'backgroundColor': 'rgba(255,255,255,0.02)',
                'border': '1px solid rgba(255,255,255,0.05)',
            },
            
            style_data_conditional=[
                # Alternating row colors
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgba(255,255,255,0.05)'
                },
                # Hover effect
                {
                    'if': {'state': 'active'},
                    'backgroundColor': 'rgba(76, 175, 80, 0.1)',
                    'border': '1px solid rgba(76, 175, 80, 0.3)',
                },
                # Selected rows
                {
                    'if': {'state': 'selected'},
                    'backgroundColor': 'rgba(76, 175, 80, 0.2)',
                    'border': '1px solid rgba(76, 175, 80, 0.5)',
                }
            ],
            
            # Filter styling
            style_filter={
                'backgroundColor': 'rgba(255,255,255,0.1)',
                'border': '1px solid rgba(255,255,255,0.2)',
                'color': 'white',
                'padding': '8px',
                'borderRadius': '5px',
            },
            
            # Pagination styling
            style_as_list_view=True,
        )
    ], className="table-container"),
    
    # Footer info
    html.Div([
        html.P(f"Database last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}", 
               style={'textAlign': 'center', 'color': 'rgba(255,255,255,0.6)', 'margin': '2rem'})
    ])
    
], className="main-container")

# Callback to update table data and handle selections
@callback(
    [Output('players-table', 'data'),
     Output('filtered-data-store', 'data'),
     Output('keep-selected-btn', 'disabled'),
     Output('selection-info', 'children'),
     Output('selection-info', 'style'),
     Output('selected-players-stat', 'children'),
     Output('total-players-stat', 'children')],
    [Input('keep-selected-btn', 'n_clicks'),
     Input('show-all-btn', 'n_clicks'),
     Input('search-input', 'value')],
    [State('players-table', 'selected_rows'),
     State('players-table', 'data'),
     State('filtered-data-store', 'data')]
)
def update_table_data(keep_clicks, show_all_clicks, search_value, selected_rows, current_data, stored_data):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Initial load
        return (df.to_dict('records'), df.to_dict('records'), True, [], 
                {'display': 'none'}, "0", str(len(df)))
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle search functionality
    if button_id == 'search-input':
        if search_value and search_value.strip():
            # Filter data based on search
            search_df = df.copy()
            search_lower = search_value.lower().strip()
            
            # Create a mask for rows that contain the search term in any column
            mask = search_df.astype(str).apply(lambda x: x.str.lower().str.contains(search_lower, na=False)).any(axis=1)
            filtered_df = search_df[mask]
            
            filtered_data = filtered_df.to_dict('records')
            return (filtered_data, filtered_data, True, [],
                    {'display': 'none'}, "0", str(len(filtered_data)))
        else:
            # If search is empty, show all data
            return (df.to_dict('records'), df.to_dict('records'), True, [],
                    {'display': 'none'}, "0", str(len(df)))
    
    elif button_id == 'keep-selected-btn' and selected_rows:
        # Filter to keep only selected rows
        selected_data = [current_data[i] for i in selected_rows]
        info_msg = f"Showing {len(selected_data)} selected players out of {len(df)} total players"
        return (selected_data, selected_data, True, info_msg,
                {'display': 'block', 'className': 'selection-info'}, 
                str(len(selected_rows)), str(len(selected_data)))
    
    elif button_id == 'show-all-btn':
        # Show all original data and clear search
        return (df.to_dict('records'), df.to_dict('records'), True, [],
                {'display': 'none'}, "0", str(len(df)))
    
    # Update selection count and button state
    selected_count = len(selected_rows) if selected_rows else 0
    button_disabled = selected_count == 0
    current_total = len(current_data)
    
    return (current_data, stored_data, button_disabled, [],
            {'display': 'none'}, str(selected_count), str(current_total))

# Callback to update selected rows count
@callback(
    Output('selected-players-stat', 'children', allow_duplicate=True),
    Input('players-table', 'selected_rows'),
    prevent_initial_call=True
)
def update_selected_count(selected_rows):
    return str(len(selected_rows) if selected_rows else 0)

# Callback to enable/disable keep selected button
@callback(
    Output('keep-selected-btn', 'disabled', allow_duplicate=True),
    Input('players-table', 'selected_rows'),
    prevent_initial_call=True
)
def toggle_keep_button(selected_rows):
    return len(selected_rows) == 0 if selected_rows else True

# Callback to clear search when showing all data
@callback(
    Output('search-input', 'value'),
    Input('show-all-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_search(n_clicks):
    if n_clicks:
        return ""
    return dash.no_update
@callback(
    Output('export-csv-btn', 'href'),
    Input('players-table', 'data')
)
def update_download_link(table_data):
    if not table_data:
        return ""
    
    # Convert data to DataFrame and then to CSV
    df_export = pd.DataFrame(table_data)
    csv_string = df_export.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + csv_string
    
    return csv_string

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)