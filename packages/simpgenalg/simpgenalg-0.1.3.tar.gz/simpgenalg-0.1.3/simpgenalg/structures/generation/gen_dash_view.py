# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import scipy.stats
import random

app = Dash(__name__)
dfs = {'indvs':None, 'stats':None}
cols = {'indvs':None, 'stats':None}

class generationViewer():

    def __init__(self, indvs=None, stats=None, rslts=None):

        def load(input):
            if isinstance(input, str):
                df = pd.read_csv(input)
            elif isinstance(input, dict):
                df = pd.DataFrame(input)
            elif isinstance(input, pd.DataFrame):
                df = input
            df = df.select_dtypes(include=\
                ('int16','int32','int64','boolean'\
                 'float16','float32','float64'))

        if indvs is not None:
            indvs = load(indvs)
        if stats is not None:
            stats = load(indvs)
        if rslts is not None:
            indvs, stats = rslts.to_df()

        dfs['indvs'] = indv
        cols['indvs'] = indv.cols
        dfs['stats'] = stats
        cols['stats'] = stats.cols

        # Raise an error if min/max don't match
        if indvs is not None and stats is not None:
            gen_min, gen_max = stats['_gen'].min(), stats['_gen'].max()
            run_min, run_max = stats['_run'].min(), stats['_run'].max()

            if gen_min != indv['_gen'].min():
                raise ValueError
            if gen_max != indv['_gen'].max():
                raise ValueError
            if run_min != indv['_run'].min():
                raise ValueError
            if run_max != indv['_run'].max():
                raise ValueError


        app.layout = html.Div([\
            dcc.Graph(id='data-graph'),
            html.Div([
                html.Div(children=[
                    html.Br(),
                    html.Label('Graph Name: '),
                    dcc.Input(value='', type='text', id='graph_name_input'),

                    html.Br(),
                    html.Label('Run'),
                    dcc.RangeSlider(run_min, run_max, 1, value=[run_min, run_max],\
                                    id='run-slider', tooltip={"placement": "bottom",\
                                    "always_visible": True}),
                    html.Br(),
                    html.Label('Generation'),
                    dcc.RangeSlider(gen_min, gen_max, value=[gen_min, gen_max],\
                                    id='gen-slider', tooltip={"placement": "bottom",\
                                    "always_visible": True})
                ], style={'padding': 10, 'flex-direction': 'column'}),

                html.Div(children=[
                    html.Label('X-Axis'),
                    dcc.Dropdown(sorted(list(cols),\
                                    '',\
                                    id='x-axis-selector'),

                    html.Br(),
                    html.Label('Y-Axis'),
                    dcc.Dropdown(sorted(list(cols)),
                                 [''],
                                 multi=True,\
                                 id='y-axis-selector'),

                    html.Br(),
                    html.Label('Color'),
                    dcc.Dropdown(sorted(list(cols)+[None]),
                                 '',\
                                 id='color-selector'),

                    html.Br(),
                    html.Label('Graph Type'),
                    dcc.Dropdown(['Bar', 'Line', 'Scatter'], 'Line',\
                                        id='graph-type-selector'),
                ], style={'padding': 10, 'flex-direction': 'row'})
            ], style={'display': 'flex', 'flex-direction': 'column'})],
        style={'display': 'flex', 'flex-direction': 'column'})

        app.run_server(debug=True)

def _get_m_and_CI(grp):
    m, CI = grp.mean(), grp.std() / grp.count()
    CI = CI.fillna(0)
    return m, m + CI,  m - CI

@app.callback(
    Output('data-graph', 'figure'),
    Input('run-slider', 'value'),
    Input('gen-slider', 'value'),
    Input('x-axis-selector', 'value'),
    Input('y-axis-selector', 'value'),
    Input('color-selector', 'value'),
    Input('graph-type-selector','value'))
def update_figure(run, gen, x, y, clr, graph_type):

    df = df_lst[0]

    df_axis = ['_run', '_gen']
    if x not in df_axis:
        df_axis.append(x)

    # Filter the new data
    filtered_df = df[df_axis+list(y)]

    # Filter out runs and gens
    filtered_df = filtered_df[filtered_df._run >= run[0]]
    filtered_df = filtered_df[filtered_df._run <= run[1]]
    filtered_df = filtered_df[filtered_df._gen >= gen[0]]
    filtered_df = filtered_df[filtered_df._gen <= gen[1]]

    filtered_df.sort_values(by=x)


    # Create new figure
    fig = go.Figure()
    if graph_type == 'None':
        pass
    elif graph_type == 'Line':

        # Group by x-axis
        grouped_by = filtered_df.groupby(by=x)

        # Get x_axis
        x_vals = np.array(list(grouped_by.groups.keys()))

        x_vals_plus_rev = np.append(x_vals, x_vals[::-1])
        # Get the mean, bottom, and top
        m, b, t = _get_m_and_CI(grouped_by)

        for y_val in y:
            c1,c2,c3 = random.randint(0,255), \
                       random.randint(0,255), \
                       random.randint(0,255)
            fig.add_trace(go.Scatter(
                x=x_vals_plus_rev,
                y=np.append(t[y_val].to_numpy(), b[y_val].to_numpy()[::-1]),
                fill='toself',
                fillcolor=f'rgba({c1},{c2},{c3},0.25)',
                line_color=f'rgba({c1},{c2},{c3},0.5)',
                showlegend=True
            ))
            fig.add_trace(go.Scatter(x=x_vals, \
                                     y=m[y_val],\
                                     mode='lines', \
                                     name=y_val,\
                                     line_color=f'rgba({c1},{c2},{c3},1)',\
                                     showlegend=True))
    elif graph_type == 'Scatter':
        for y_val in y:
            if clr is None:
                c1,c2,c3 = random.randint(0,255), \
                           random.randint(0,255), \
                           random.randint(0,255)
                fig.add_trace(go.Scatter(x=filtered_df[x], \
                                         y=filtered_df[y_val],\
                                         mode='markers', \
                                         name=y_val,\
                                         line_color=f'rgba({c1},{c2},{c3},1)',\
                                         showlegend=True))
            else:
                c1,c2,c3 = random.randint(0,255), \
                           random.randint(0,255), \
                           random.randint(0,255)
                fig.add_trace(go.Scatter(x=filtered_df[x], \
                                         y=filtered_df[y_val],\
                                         mode='markers', \
                                         name=y_val,\
                                         color=clr
                                         showlegend=True))

    fig.update_layout(legend_title_text = "Legend")
    fig.update_xaxes(title_text=x)
    fig.update_layout(transition_duration=500)

    return fig
