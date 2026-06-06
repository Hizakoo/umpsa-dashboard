import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# Initialize Dash web engine
app = dash.Dash(__name__)
server = app.server

# --- [CO2: ADOPT DATA EXTRACTION] ---
csv_filename = 'courses.csv'

if os.path.exists(csv_filename):
    master_df = pd.read_csv(csv_filename)
    print(f"[Data Extraction Success] Loaded custom academic modules from '{csv_filename}'.")
else:
    print(f"[Data Extraction Warning] '{csv_filename}' missing! Creating structural runtime backup schema.")
    backup_data = {
        "Course Code": ["BCM3253", "BCN3173"],
        "Course Name": ["DATA ANALYTICS AND VISUALIZATION", "EMBEDDED SYSTEM APPLICATION AND DESIGN"],
        "Section": ["01", "01"], "Day": ["Wednesday", "Wednesday"],
        "Start_Hour": [11, 11], "End_Hour": [13, 14],
        "Lecturer": ["Ts. Aziman", "Dr. Nelson"], "Room": ["Room 302", "Lab 2A"]
    }
    master_df = pd.DataFrame(backup_data)

# Main Application Window Layout Configuration
app.layout = html.Div([
    # Top Banner Header Strip
    html.Div([
        html.H1("CENTRALIZED REGISTRATION DASHBOARD", style={'margin': '0', 'fontSize': '26px', 'letterSpacing': '1px'}),
        html.P("Centralized registration dashboard loop to avoid the 'trial and error' loop", style={'margin': '5px 0 0 0', 'color': '#6c757d', 'fontSize': '14px'})
    ], style={'textAlign': 'center', 'padding': '15px 0', 'borderBottom': '2px solid #dee2e6', 'fontFamily': 'sans-serif'}),
    
    # Scrollable Filter Options Panel (Keeps layout clean with 17 subjects)
    html.Div([
        html.Label("SELECT ACADEMIC SUBJECT BLOCKS TO ASSESS CLASHES:", style={'fontWeight': 'bold', 'fontSize': '13px', 'color': '#495057'}),
        html.Div([
            dcc.Checklist(
                id='course-selector',
                options=[{'label': f" {r['Course Code']} - {r['Course Name']} (Sec {r['Section']})", 'value': r['Course Code']} for _, r in master_df.iterrows()],
                value=["BCM3253", "BCN3173", "BCI2353", "BCN3263"], # Pre-checked to trigger visual clashes instantly
                labelStyle={'display': 'block', 'margin': '5px 0', 'fontSize': '12px'}
            )
        ], style={'maxHeight': '160px', 'overflowY': 'scroll', 'border': '1px solid #ced4da', 'padding': '10px', 'borderRadius': '4px', 'backgroundColor': '#fff', 'marginTop': '8px'}),
    ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderBottom': '1px solid #dee2e6', 'fontFamily': 'sans-serif'}),

    # Three-Pane Split-Screen Layout Flex Container
    html.Div([
        
        # 1. LEFT SIDEBAR: CONFLICT HEATMAP PANE
        html.Div([
            html.H4("CONFLICT HEATMAP", style={'textAlign': 'center', 'fontSize': '13px', 'margin': '0 0 5px 0', 'color': '#212529'}),
            html.P("(LEFT SIDEBAR)", style={'textAlign': 'center', 'fontSize': '10px', 'color': '#868e96', 'margin': '0 0 15px 0'}),
            dcc.Graph(id='heatmap-matrix', config={'displayModeBar': False})
        ], style={'width': '28%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px', 'boxSizing': 'border-box', 'borderRight': '1px dashed #dee2e6'}),
        
        # 2. CENTER PANE: LIVE WEEKLY SCHEDULE TIMETABLE
        html.Div([
            html.H4("THE 'LIVE' WEEKLY SCHEDULE", style={'textAlign': 'center', 'fontSize': '13px', 'margin': '0 0 5px 0', 'color': '#212529'}),
            html.P("(CENTER PANE)", style={'textAlign': 'center', 'fontSize': '10px', 'color': '#868e96', 'margin': '0 0 15px 0'}),
            dcc.Graph(id='gantt-schedule', config={'displayModeBar': False})
        ], style={'width': '44%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px', 'boxSizing': 'border-box'}),
        
        # 3. RIGHT PANE: DYNAMIC DATA SIDEBAR
        html.Div([
            html.H4("DYNAMIC DATA SIDEBAR", style={'textAlign': 'center', 'fontSize': '13px', 'margin': '0 0 5px 0', 'color': '#212529'}),
            html.P("(RIGHT PANE)", style={'textAlign': 'center', 'fontSize': '10px', 'color': '#868e96', 'margin': '0 0 15px 0'}),
            
            # Simulated Server Update Stream Box
            html.Div([
                html.H5("LECTURER UPDATES FEED", style={'fontSize': '11px', 'margin': '0 0 10px 0', 'color': '#495057', 'borderBottom': '1px solid #dee2e6', 'paddingBottom': '3px'}),
                html.Div(id='lecturer-status-feed', style={'fontSize': '12px', 'lineHeight': '1.5'}),
                html.Br(),
                html.Button("Simulate Schedule Shifts", id="live-update-btn", n_clicks=0,
                            style={'width': '100%', 'padding': '8px', 'backgroundColor': '#f1f3f5', 'border': '1px solid #ced4da', 'borderRadius': '4px', 'cursor': 'pointer', 'fontWeight': 'bold', 'fontSize': '12px'})
            ], style={'backgroundColor': '#fff', 'padding': '12px', 'borderRadius': '4px', 'border': '1px solid #dee2e6', 'marginBottom': '15px'}),
            
            # Usability Survey Panel
            html.Div([
                html.H5("DASHBOARD EVALUATION", style={'fontSize': '11px', 'margin': '0 0 10px 0', 'color': '#2b5115', 'borderBottom': '1px solid #bcdab7', 'paddingBottom': '3px'}),
                html.Label("Rate System Interface Usability (1-5):", style={'fontSize': '11px', 'color': '#2b5115'}),
                dcc.Slider(1, 5, 1, value=4, id='eval-slider'),
                html.Button("Submit Score", id='submit-eval', n_clicks=0,
                            style={'width': '100%', 'padding': '6px', 'backgroundColor': '#28a745', 'color': 'white', 'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer', 'marginTop': '5px', 'fontWeight': 'bold'}),
                html.Div(id='live-eval-results', style={'marginTop': '10px', 'fontSize': '11px', 'fontWeight': 'bold', 'color': '#155724'})
            ], style={'backgroundColor': '#e2f0d9', 'padding': '12px', 'borderRadius': '4px', 'border': '1px solid #bcdab7'})
            
        ], style={'width': '28%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px', 'boxSizing': 'border-box', 'borderLeft': '1px dashed #dee2e6', 'fontFamily': 'sans-serif'})
        
    ], style={'width': '100%', 'display': 'flex', 'boxSizing': 'border-box', 'fontFamily': 'sans-serif'})
])

evaluation_records = [4.5, 5.0, 4.0]

# Central Processing Engine Engine Backend Component
@app.callback(
    [Output('heatmap-matrix', 'figure'),
     Output('gantt-schedule', 'figure'),
     Output('lecturer-status-feed', 'children'),
     Output('live-eval-results', 'children')],
    [Input('course-selector', 'value'),
     Input('live-update-btn', 'n_clicks'),
     Input('submit-eval', 'n_clicks')],
    [State('eval-slider', 'value')]
)
def process_three_panes(selected_courses, sync_clicks, eval_clicks, slider_value):
    start_time = time.time() # Start diagnostic execution timer
    current_df = master_df.copy()
    
    feed_items = [
            html.Div("Ts. Aziman: [Confirmed]", style={'color': 'green'}),
            html.Div("Dr. Nelson: [Confirmed]", style={'color': 'green'}),
            html.Div("Dr. Nor: [Confirmed]", style={'color': 'green'}),
            html.Div("Ts. Farid: [Confirmed]", style={'color': 'green'})
        ]
    
    # --- [CO2: SYNCHRONIZE DATASET FOR REAL-TIME UPDATES] ---
    if sync_clicks % 2 != 0:
        # Simulate an unexpected backend change: Shift BCN3323 to clash directly with ULE2332 on Thursday
        current_df.loc[current_df['Course Code'] == 'BCN3323', 'Start_Hour'] = 11
        current_df.loc[current_df['Course Code'] == 'BCN3323', 'End_Hour'] = 13
        feed_items = [
            html.Div("Ts. Amran: [Slot Change - Rescheduled]", style={'color': '#d9534f', 'fontWeight': 'bold'}),
            html.Div("BCN3323 block is flashing red!", style={'color': '#d9534f', 'fontSize': '11px', 'fontStyle': 'italic'}),
            html.Div("Ts. Aziman: [Confirmed]", style={'color': 'green'}),
            html.Div("Dr. Nelson: [Confirmed]", style={'color': 'green'})
        ]

    # Filter records based on selected checklist values
    filtered_df = current_df[current_df['Course Code'].isin(selected_courses)].reset_index(drop=True)
    num_records = len(filtered_df)
    
    # --- [CO2: PRODUCE NEW DATA FROM ORIGINAL DATASET] ---
    matrix_data = [[0]*num_records for _ in range(num_records)]
    conflicts = []
    
    for i in range(num_records):
        for j in range(num_records):
            if i != j:
                r1, r2 = filtered_df.iloc[i], filtered_df.iloc[j]
                if r1['Day'] == r2['Day'] and not (r1['End_Hour'] <= r2['Start_Hour'] or r1['Start_Hour'] >= r2['End_Hour']):
                    matrix_data[i][j] = 1
                    conflicts.append(r1['Course Code'])

    labels = filtered_df['Course Code'].tolist()
    
    # 1. GENERATE LEFT HEATMAP MATRIX
    heatmap_fig = px.imshow(
        matrix_data, x=labels, y=labels,
        color_continuous_scale=[[0, '#e9ecef'], [1, '#FF4655']], # Light gray or high-contrast Red
    )
    heatmap_fig.update_coloraxes(showscale=False)
    heatmap_fig.update_layout(margin=dict(l=40, r=20, t=10, b=20), height=280)
    
    # 2. GENERATE CENTER TIMETABLE GANTT PLOT
    gantt_fig = go.Figure()
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    for _, row in filtered_df.iterrows():
        is_clashing = row['Course Code'] in conflicts
        block_color = 'rgba(255, 70, 85, 0.85)' if is_clashing else 'rgba(54, 162, 235, 0.8)'
        
        # Expanded Hover-to-Detail text formatting block
        hover_text = (
            f"<b>SUBJECT CODE:</b> {row['Course Code']}<br>"
            f"<b>COURSE NAME:</b> {row['Course Name']}<br>"
            f"<b>LECTURER NAME:</b> {row['Lecturer']}<br>"
            f"<b>ROOM NUMBER:</b> {row['Room']}<br>"
            f"<b>TIME:</b> {row['Start_Hour']}:00 - {row['End_Hour']}:00"
            "<extra></extra>"
        )
        
        gantt_fig.add_trace(go.Bar(
            x=[row['End_Hour'] - row['Start_Hour']],
            y=[row['Day']],
            base=[row['Start_Hour']],
            orientation='h',
            name=row['Course Code'],
            marker=dict(color=block_color, line=dict(color='#333', width=1)),
            hovertemplate=hover_text
        ))
    
    gantt_fig.update_layout(
        barmode='stack',
        xaxis=dict(title="Operational Time (24h Scale)", tickvals=list(range(8, 19)), range=[8, 18], fixedrange=True),
        yaxis=dict(categoryorder='array', categoryarray=days_order, fixedrange=True),
        margin=dict(l=60, r=20, t=10, b=40),
        height=340,
        showlegend=False
    )
    
    # 3. COMPUTE RUNNING USABILITY SURVEY AVERAGES
    ctx = dash.callback_context
    if ctx.triggered and 'submit-eval' in ctx.triggered[0]['prop_id']:
        evaluation_records.append(float(slider_value))
        
    avg_score = sum(evaluation_records) / len(evaluation_records)
    eval_text = f"Submissions: {len(evaluation_records)} | Live Average: {avg_score:.2f} / 5.0"
    
    # --- [CO2: VISUALIZE EFFICIENTLY WITH REASONABLE LOADING TIME] ---
    print(f"[Performance Diagnostic Log] Render pipeline executed in {time.time() - start_time:.4f} seconds.")
    
    return heatmap_fig, gantt_fig, feed_items, eval_text

if __name__ == '__main__':
    app.run(debug=True)