import dash_html_components as html
import dash_core_components as dcc
from datetime import date
from util import Util

sidebar = html.Div(
            className="row",
            children=[
                html.Div(
                    className='three columns div-user-controls',
                    children=[
                        html.H2('Activity Data'),
                        html.P('Input Id (1-999)'),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Input(id='actUser', type='text', placeholder='ex)230,232...'),
                            ]
                        ),
                        html.P('Date Range'),
                        html.Div(
                            className="div-for-dropdown",
                            children=[

                                dcc.DatePickerSingle(
                                    id='startDate',
                                    className='div-for-date',
                                    min_date_allowed=date(1990, 1, 1),
                                    max_date_allowed=date(2090, 1, 1),
                                    initial_visible_month=Util.get_previous_month_with_last_date(date.today()).replace(
                                        day=1),
                                    date=Util.get_previous_month_with_last_date(date.today()).replace(day=1),
                                    display_format='YYYY-MM-DD'
                                ),
                                dcc.DatePickerSingle(
                                    id='endDate',
                                    className='div-for-date',
                                    min_date_allowed=date(1990, 1, 1),
                                    max_date_allowed=date(2090, 1, 1),
                                    initial_visible_month=Util.get_previous_month_with_last_date(date.today()),
                                    date=Util.get_previous_month_with_last_date(date.today()),
                                    display_format='YYYY-MM-DD'
                                )
                            ]
                        ),
                        html.P('Activity Choice'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(
                                    id='activity',
                                    options=[
                                        {'label': 'TV', 'value': 'TV'},
                                        {'label': 'KITCHEN', 'value': 'KITCHEN'},
                                        {'label': 'RESTROOM', 'value': 'RESTROOM'},
                                        {'label': 'TOILET', 'value': 'TOILET'},
                                        {'label': 'MEDICATION', 'value': 'MEDICATION'},
                                        {'label': 'ETC', 'value': 'ETC'}
                                    ],
                                    value='TV'
                                ),
                            ]
                        ),
                        html.P('Weekdays'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Checklist(
                                    id='weekdayChoice',
                                    options=[
                                        {'label': 'Mon', 'value': 1},
                                        {'label': 'Tue', 'value': 2},
                                        {'label': 'Wed', 'value': 3},
                                        {'label': 'Thu', 'value': 4},
                                        {'label': 'Fri', 'value': 5},
                                        {'label': 'Sat', 'value': 6},
                                        {'label': 'Sun', 'value': 7},
                                    ],
                                    value=[i for i in range(1, 8, 1)],
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ]
                        ),

                        html.P('Legend'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.RadioItems(
                                    id='legendType',
                                    options=[
                                        {'label': 'WeekDays', 'value': 'weekdays'},
                                        {'label': 'People', 'value': 'people'}
                                    ],
                                    value='weekdays'
                                ),
                            ]
                        ),
                        html.P('limit(min)'),
                        html.Div(
                            className='div-for-slider',
                            children=[
                                dcc.Slider(
                                    id='actLimit',
                                    min=0,
                                    max=600,
                                    step=None,
                                    marks={
                                        i: str(i) for i in range(0, 660, 60)

                                    },
                                    value=60
                                ),
                            ]
                        ),

                        html.Button('start', id='startActivity'),
                    ])
                ])