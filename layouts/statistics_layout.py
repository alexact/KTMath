import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.express as px
import pandas as pd
from Service.StatisticsService import StatisticsController
import layouts.component_statistics_view as csview
from layouts.app import app


file = pd.read_csv('D:\IngenieriadeSistemas\TrabajodeGrado\prueba.csv',
                           encoding='unicode_escape')
titles_file = pd.read_csv('D:\IngenieriadeSistemas\TrabajodeGrado\dataTituloVariablesprueba.csv',
                           encoding='unicode_escape')
df = pd.DataFrame(file)
df_titles = pd.DataFrame(titles_file)
colX=0
colY=1
df_frec = StatisticsController().generate_statistics("")

fig_correlation = px.scatter(df,
                             x=df.iloc[:, 0], y=df.iloc[:, 1],
                             title="Gráfica de correlación",
                             )
titles=[{'label': 'index', 'value': '-'}]
for i in df_titles:
    titles.append({'label': i, 'value': i})

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}
df_frec1 = pd.DataFrame({'-':['count', 'mean','std','min','25%','50%','75%','max']})
#df_frec = df_frec1+df_frec
print(df_frec.to_dict())

# grafica de corelación
layout_statistics = html.Div([
    html.Div([
        html.Div([
            dash_table.DataTable(
                data=df_frec.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in list(df_frec)],
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

            html.Hr()
        ]),
    html.Div([
        dcc.Graph(
            id="correlation-Graph",
            config = {'displaylogo': False}
        ),

    ], className="six_columns"),
        html.Div([dcc.Dropdown(id='var_XSev', options=titles, value=titles[2]['value'])], className="titlesXSev_Dropdown"),
        html.Div([dcc.Dropdown(id='var_YSev', options=titles, value=titles[3]['value'])], className="titlesYSev_Dropdown")
    ]),

], className="row")






@app.callback(dash.dependencies.Output("correlation-Graph", "figure"),
              [dash.dependencies.Input("var_XSev", "value"),
               dash.dependencies.Input("var_YSev", "value")])
def update_fig_corr(input_value,var_YSev):

    print(" holaaaaaaaaa ")
    title=list(df_titles)
    colX = title.index(input_value)
    colY = title.index(var_YSev)

    data=[]
    data.append(dict(
        x=df[title[colX]],
        y=df[title[colY]],
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

    print('You have selected "{}"'.format(input_value))
    r={"data":data,
            "layout":layout}
    return r




if __name__=="__main__":
    app.run_server(debug=True)