# running server

from maindash import my_app
from my_layout import layout

# dash app runner

if __name__ == '__main__':
    my_app.layout = layout
    my_app.run_server(debug=True)