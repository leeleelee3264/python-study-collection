import dash_html_components as html
import dash_core_components as dcc

from datetime import date, timedelta

from dbModule import DataBase
from maindash import my_app
from dash.dependencies import Input, Output, State

# layout for ai_user_choice
dbConnect = DataBase()

layout = html.Div(children=[
    html.Div(children=[html.H3('AI User Choice'),
                       html.Div(
                           className='box_container',
                           children=[
                               html.Div(
                                   className='console_part',
                                   children=[
                                       html.B('Input Id (1-999)'),
                                       html.Br(),
                                       dcc.Input(id='dayUserIdNum', type='text', placeholder='ex)230,232...'),
                                       html.Br(),
                                       html.B('Target'),
                                       html.Br(),
                                       dcc.DatePickerSingle(
                                           id='dayTarget',
                                           min_date_allowed=date(1990, 1, 1),
                                           max_date_allowed=date(2090, 1, 1),
                                           initial_visible_month=date.today(),
                                           date=date.today(),
                                           display_format='YYYY-MM-DDD'
                                       ),
                                       html.Br(),
                                       html.B('Job Type Choice'),
                                       html.Br(),
                                       dcc.Dropdown(
                                           id='aiJobType',
                                           options=[
                                               {'label': 'Auto', 'value': 1},
                                               {'label': 'Individual', 'value': 2},
                                               {'label': 'Individual(Posture)', 'value': 3},
                                               {'label': 'Group', 'value': 4}
                                           ],
                                           value=1
                                       ),
                                       html.Hr(),
                                       html.Button('start', id='dayAiUserChoiceStart', n_clicks=0),
                                       html.Button('result', id='dayAiResultStart')

                                   ]),
                               html.Div(
                                   className='data_part',
                                   children=[
                                        html.B(id='out_test')
                                   ]
                               )
                           ])

                       ]),
    html.Div(children=[html.H3('AI User Choice(Month)'),
                       html.Div(
                           className='box_container',
                           children=[
                               html.Div(
                                   className='console_part',
                                   children=[
                                       html.B('Date Range'),
                                       html.Br(),
                                       dcc.DatePickerRange(
                                           id='date-picker-range',
                                           start_date_placeholder_text='Start Date',
                                           end_date=date.today(),
                                           display_format='YYYY-MM-DDD'
                                       ),
                                       html.Br(),
                                       html.Hr(),
                                       html.Button('start', id='start2')
                                   ]),
                           ]),

                       ])
])


# call back for ai_user_choice
@my_app.callback(
    Output('out_test', 'children'),
    Input('dayAiUserChoiceStart', 'n_clicks'),
    State('dayUserIdNum', 'value'), State('dayTarget', 'date'), State('aiJobType', 'value')
)
def ai_user_choice(n_clicks, userId, targetDate, jobType):
    if userId is None:
        return 'User를 선택해주세요.'

