import dash
import dash_table
import plotly.express as px
import pandas as pd
from Service.StatisticsController import StatisticsController
from layouts.app import app
import layouts.ComponentsView as drc
import base64
import io
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime


class UploadClass:
    severity_df = StatisticsController( )
    df_data = severity_df.init_table( )
    df_frecuency = df_data
    titles_frec = []
    titles_dropdown = []
    print(df_data)
    if not df_data.empty:
        df_frecuency = pd.DataFrame({'title': ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']})
        df_frecuency = df_frecuency + df_data
        titles_frec = [{'name': 'title', 'id': 'title'}]
        print(df_frecuency)

    for i in list(df_data):
        titles_frec.append({'name': i, 'id': i})

    for i in list(df_data):
        titles_dropdown.append({'label': i, 'value': i})

    def parse_contents(self, filename, date):
        content_type, content_string = self.split(',')
        decoded = base64.b64decode(content_string)

        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df_X = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
                UploadClass.df_frecuency = UploadClass.severity_df.generate_statistics(df_X)
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df_X = pd.read_excel(io.BytesIO(decoded))
                UploadClass.df_frecuency = UploadClass.severity_df.generate_statistics(df_X)

        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            html.Hr( ),  # horizontal line
        ])


df = UploadClass.df_data

colX = 0
colY = 1

fig_correlation = px.scatter(df,
                             x=df.iloc[:, 0], y=df.iloc[:, 1],
                             title="Gráfica de correlación",
                             )

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}

# grafica de corelación
layout_statistics = html.Div([
    html.Div([
        drc.Card_markdown([
            dcc.Markdown('''
                # **Tabla de frecuencia**
                En ella puedes verificar cual es la media, la desviación, los máximos y minimos de los datos.

                ## * Qué es 25%, 50% y 75% * ? *
                Son percentiles y permite saber cómo está situado un valor en función de una muestra.

                Se divide el 100% de la muestra en 3, dando como resultado 25%, 50% y 75%.
                El 50% es la mediana.
                ### Interpretación:
                - El 25% de los trabajadores consideran que para la variable "Disinterest" existe una severidad de...
                - El 50% de los trabajadores consideran que para la variable "Disinterest" existe una severidad de...
                - El 75% de los trabajadores consideran que para la variable "Disinterest" existe una severidad de...
            '''
                         )
        ]),
        html.Div([dcc.Upload(
            id='upload-datas',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
            html.Div(id='output-data-uploads'),

        ]),
        html.Div([
            dash_table.DataTable(
                id='frec_table',
                data=UploadClass.df_frecuency.to_dict('records'),
                columns=UploadClass.titles_frec,
                style_as_list_view=True,
                style_header=table_header_style,
                style_data_conditional=[
                    {
                        "if": {"column_id": "param"},
                        "textAlign": "right",
                        "paddingRight": 10,
                    },
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "white",
                    },
                ],
            ),

            html.Hr( )
        ]),
        html.Div([
            dcc.Graph(
                id="correlation-Graph",
                config={'displaylogo': False}
            ),

        ], className="six_columns"),
        html.Div([dcc.Dropdown(id='var_XSev', options=UploadClass.titles_dropdown,
                               value=UploadClass.titles_dropdown[2]['value'])], className="titlesXSev_Dropdown"),
        html.Div([dcc.Dropdown(id='var_YSev', options=UploadClass.titles_dropdown,
                               value=UploadClass.titles_dropdown[3]['value'])], className="titlesYSev_Dropdown")
    ]),

], className="row")


@app.callback(Output('frec_table', 'data'),
              [Input('output-data-uploads', 'children')], )
def update_table(childrenUpload):
    if UploadClass.df_data is None:
        print(UploadClass.df_frecuency.to_dict('records'))
        return UploadClass.df_frecuency.to_dict('records')


@app.callback(dash.dependencies.Output("correlation-Graph", "figure"),
              [Input('frec_table', 'data'),
               dash.dependencies.Input("var_XSev", "value"),
               dash.dependencies.Input("var_YSev", "value")])
def update_fig_corr(data_df, input_value, var_YSev, ):
    print(" carga correlación ")
    title = [i for i in list(UploadClass.df_data)]
    colX = title.index(input_value)
    colY = title.index(var_YSev)
    if data_df is not None:
        data = []
        data.append(dict(
            x=data_df[title[colX]],
            y=data_df[title[colY]],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }))
        layout = dict(
            title="Gráfica de correlación",
            xaxis={'type': 'log', 'title': title[colX]},
            yaxis={'title': title[colY]},
            legend={'x': 'a', 'y': 0},
            hovermode='closest'
        )

        print('You have selected for X corr"{}"'.format(input_value))
        r = {"data": data,
             "layout": layout}
        return r
    layout = dict(
        title="Gráfica de correlación",
        xaxis={'type': 'log', 'title': title[colX]},
        yaxis={'title': title[colY]},
        legend={'x': 'a', 'y': 0},
        hovermode='closest'
    )
    data = []
    data.append(dict(
        x=0,
        y=0,
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        }))
    r = {"data": data,
         "layout": layout}
    return r


@app.callback(Output('output-data-uploads', 'children'),
              [Input('upload-datas', 'contents')],
              [State('upload-datas', 'filename'),
               State('upload-datas', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            UploadClass.parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
