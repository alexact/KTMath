import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from layouts.app import app
from layouts.SVM import layout_SVM
# from layouts.component_upload_view import layout_upload
from layouts.StatisticsLayout import layout_statistics
# import callbacks

app.layout = html.Div([

    html.Div([
    html.Div([
        html.H1("Analiza el conocimiento de tu equipo"),
        dcc.Link('  Generar estadísticas  ', href='/ktmath/statistics'),
        dcc.Link('  Generar predicción    ', href='/ktmath/vmAlgorithm'),
        html.Img(src="../assets/logopdg1.png")
        ]),
    ], className="banner"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ktmath/svmAlgorithm':
         return layout_SVM
    elif pathname == '/ktmath/statistics':
        return layout_statistics
    else:
        return layout_SVM

if __name__ == '__main__':
    app.run_server(debug=True)