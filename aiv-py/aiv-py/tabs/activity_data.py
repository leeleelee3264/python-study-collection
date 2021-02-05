import dash_html_components as html
import dash_core_components as dcc

from datetime import date
from maindash import my_app
from dash.dependencies import Input, Output, State

from callBacks import activity_data as ad

from util import Util

import plotly.express as px
import pandas as pd


layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className='two columns div-user-controls',
                    children=[
                        html.H2('Total detail'),
                        html.P('Target User Id'),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Input(id='ownerId', type='text'),
                            ]
                        ),
                        html.P('Date Range'),
                        html.Div(
                            className="div-for-dropdown",
                            children=[

                                dcc.DatePickerRange(
                                    id='targetDate',
                                    start_date=Util.get_previous_month_with_last_date(date.today()).replace(day=1),
                                    start_date_placeholder_text='Start Date',
                                    end_date=Util.get_previous_month_with_last_date(date.today()),
                                    display_format='YYYY-MM-DD'
                                ),
                            ]
                        ),

                        html.P('Activity Choice'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(
                                    id='actType',
                                    options=[
                                        {'label': '수면/기상', 'value': 'SLEEP'},
                                        {'label': '외출', 'value': 'GO_OUT'},
                                        {'label': '용변/화장실', 'value': 'TOILET'},
                                        {'label': '주방', 'value': 'KITCHEN'},
                                        {'label': 'TV', 'value': 'TV'},
                                        {'label': 'MEDICATION', 'value': 'MEDICATION'},
                                        {'label': '운동량', 'value': '?'}
                                    ],
                                    value='SLEEP'
                                ),
                            ]
                        ),
                        html.Button('start', id='startActivity'),
                    ]
                ),

                html.Div(
                    className='nine columns div-for-charts bg-grey',
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='first-graph'
                                ),
                                dcc.Graph(
                                    id='second-graph',
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    ])


# first graph
@my_app.callback(
    Output('first-graph', 'figure'),
    Input('startActivity', 'n_clicks'),
    State('ownerId', 'value'), [State('targetDate', 'start_date'), State('targetDate', 'end_date')], State('actType', 'value'),
)
def activity_data(n_clicks, ownerId, start_date, end_date, actType):

    df = ad.act_duration(ownerId, actType, start_date, end_date)

    # df = pd.DataFrame({
    #     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    #     "Amount": [4, 1, 2, 2, 4, 5],
    #     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    # })

    print(df)
    fig = px.bar(df, x='act_date', y="duration", barmode="group")

    return fig


# second graph