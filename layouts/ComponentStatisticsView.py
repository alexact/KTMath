from textwrap import dedent
import dash_table
import dash_core_components as dcc
import dash_html_components as html


def table_header_style():
    return {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
    }


def table_fecuency(df_frec):
    return html.Div([
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
    ])


def selects_for_table(titles, x_init, id):
    return dcc.Dropdown(id=id, options=titles, value=titles[x_init]['value'])


