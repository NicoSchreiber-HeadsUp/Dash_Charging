##############################
# PACKAGES
##############################
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.express as px
import pandas as pd

##############################
# INITIALIZATION
##############################

# Load data
stations = pd.read_csv('../data/stations_cleaned.csv', encoding="utf-8")
stations_state = stations.groupby('state').size().reset_index(name='count').sort_values(by='count', ascending=False)
stations_state.columns=['State', 'Charging Stations']

# Initialize the Dash app
app = Dash(__name__)

##############################
# FUNCTIONS
##############################

def create_map(selected_id=None):
    df = stations.copy()
    df['color'] = "blue"
    df['size'] = 7
    df['opacity'] = 0.5

    if selected_id in df['id'].values:
        df.loc[df['id'] == selected_id, 'color'] = 'violet'
        df.loc[df['id'] == selected_id, 'size'] = 16
        df.loc[df['id'] == selected_id, 'opacity'] = 1

    fig = px.scatter_map(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='operator',
        hover_data={'latitude': False, 'longitude': False, 'color': False, 'size': False},
        custom_data=['id'],
        zoom=5.4,
        center={'lat': 51.2634, 'lon': 10.4477},
        color='color',
        color_discrete_map={'blue': "#e0ba3b", 'violet': '#82358b'},
    )

    # Update size and opacity
    for trace in fig.data:
        trace_color = trace.name
        mask = df['color'] == trace_color
        trace.marker.size = df.loc[mask, 'size']
        trace.marker.opacity = df.loc[mask, 'opacity']

    fig.update_layout(
        mapbox_style='open-street-map',
        autosize=False,
        width=750,
        height=800,
        margin={'l': 0, 'r': 0, 'b': 50, 't': 30},
        paper_bgcolor="#daceb6",
        showlegend=False
    )
    return fig

def create_info(selected_id=None):
    if selected_id is not None:
        var_operator = str(stations.loc[stations['id'] == selected_id, 'operator'].values[0])
        var_state = str(stations.loc[stations['id'] == selected_id, 'state'].values[0])+"/"+str(stations.loc[stations['id'] == selected_id, 'postal_code'].values[0])
        var_loading_spots = str(stations.loc[stations['id'] == selected_id, 'loading_spots'].values[0])
        var_payment_method = str(stations.loc[stations['id'] == selected_id, 'payment_systems'].values[0])
    else:
        var_operator=""
        var_state=""
        var_loading_spots=""
        var_payment_method=""

    return var_operator, var_state, var_loading_spots, var_payment_method


##############################
# APP LAYOUT
##############################

app.layout = html.Div(
    style={'backgroundColor': "#1e2864", 'minHeight': '100vh', 'padding': '20px'},
    children=[
        # Title
        html.H1("Charging Stations in Germany", style={'textAlign': 'center', 'color': "#daceb6"}),

        # Map and station information
        html.Div([
            # Map
            html.Div([
                dcc.Graph(id='map_german', figure=create_map())
            ], style={'width': '60%', 'padding': '10px'}),
            # Data Information
            html.Div([
                html.P("Selected station",
                       style={'fontSize': '24px','fontWeight':'bold','color':"#82358b"}),

                # Operator
                html.Div([
                    html.Div([
                        html.P("Operator:", style={'fontSize': '18px','fontWeight':'bold','color':"#b6ac98"})
                    ], style={'width': '30%', 'padding': '0px'}),
                    html.Div([
                        html.P(id='operator-info', children="", style={'fontSize': '18px','color':"#b6ac98"})
                    ], style={'width': '70%', 'padding': '0px'}),
                ], style={'display': 'flex', 'flexDirection': 'row'}),

                # State and post code
                html.Div([
                    html.Div([
                        html.P("State / Postal code:", style={'fontSize': '18px','fontWeight':'bold','color':"#b6ac98"})
                    ], style={'width': '30%', 'padding': '0px'}),
                    html.Div([
                        html.P(id='state-info', children="", style={'fontSize': '18px','color':"#b6ac98"})
                    ], style={'width': '70%', 'padding': '0px'}),
                ], style={'display': 'flex', 'flexDirection': 'row'}),

                # Loading spots
                html.Div([
                    html.Div([
                        html.P("Loading spots:", style={'fontSize': '18px','fontWeight':'bold','color':"#b6ac98"})
                    ], style={'width': '30%', 'padding': '0px'}),
                    html.Div([
                        html.P(id='loading-spots-info', children="", style={'fontSize': '18px','color':"#b6ac98"})
                    ], style={'width': '70%', 'padding': '0px'}),
                ], style={'display': 'flex', 'flexDirection': 'row'}),

                # Pyment method
                html.Div([
                    html.Div([
                        html.P("Payment method:", style={'fontSize': '18px','fontWeight':'bold','color':"#b6ac98"})
                    ], style={'width': '30%', 'padding': '0px'}),
                    html.Div([
                        html.P(id='payment-method-info', children="", style={'fontSize': '18px','color':"#b6ac98"})
                    ], style={'width': '70%', 'padding': '0px'}),
                ], style={'display': 'flex', 'flexDirection': 'row'}),

                html.Div([
                    html.H2('Charging stations by state', style={'color': '#82358b'}),
                    dash_table.DataTable(
                        data=stations_state.to_dict('records'),
                        columns=[{"name": i, "id": i} for i in stations_state.columns],
                        style_table={'overflowX': 'auto', 'width': '80%','border': '1px solid #b6ac98'},
                        page_size=16,
                        style_cell={
                            'textAlign': 'left',
                            'fontSize': '18px',
                            'color': '#b6ac98',
                            'backgroundColor': 'transparent'
                        },
                        style_header={
                            'fontWeight': 'bold',
                            'fontSize': '18px',
                            'color': "#000000",
                            'backgroundColor': '#e0ba3b'
                        }
                        
                    )
                ], style={'padding': '10px'})

            ], style={'width': '40%', 'padding': '10px'}),
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]
)

##############################
# CALLBACKS
##############################

@app.callback(
    Output('operator-info', 'children'),
    Output('state-info', 'children'),
    Output('loading-spots-info', 'children'),
    Output('payment-method-info', 'children'),
    Output('map_german', 'figure'),
    Input('map_german', 'clickData')
)
def update_dashboard(clickData):
    if clickData:
        selected_id = clickData['points'][0]['customdata'][0]
    else:
        selected_id = None

    # Get info and map
    operator, state, loading_spots, payment_method = create_info(selected_id)
    fig = create_map(selected_id)

    return operator, state, loading_spots, payment_method, fig

##############################
# RUN APP
##############################

if __name__ == "__main__":
    app.run(debug=True, port=8051)

##############################
##############################
##############################

# HEADS UP colours
# violet   #82358b
# darkblue #1e2864