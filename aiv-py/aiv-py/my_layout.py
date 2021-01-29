import dash_core_components as dcc
import dash_html_components as html

# import layouts
from tabs.activity_data import layout as activity_data_layout
from tabs.ai_user_choice import layout as ai_user_choice_layout

layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Activity Data', children=[
            activity_data_layout
        ]),
        dcc.Tab(label='Tag Data', children=[

        ]),
        dcc.Tab(label='Walk Data', children=[

        ]),
        dcc.Tab(label='Move Box Plot', children=[

        ]),
        dcc.Tab(label='AI User Choice', children=[
            ai_user_choice_layout
        ]),
        dcc.Tab(label='Posture Data', children=[

        ]),
        dcc.Tab(label='Physical Activity Index', children=[

        ]),
    ])
])
