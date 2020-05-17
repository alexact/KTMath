import base64
import io
import time
from sklearn import datasets
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import datetime

import layouts.components_view as drc
from layouts.Figures import serve_prediction_plot, serve_roc_curve, \
    serve_pie_confusion_matrix

from Model.Statistics import Statistics
from layouts.app import app
from layouts.component_upload_view import parse_contents
from Service.StatisticsService import StatisticsController
from Model.Data import Data as data
import pandas as pd





def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    severity_df = StatisticsController()
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df_X = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
          #  data.set_df_X(severity_df.get_allData(df_X))
          #  print(data.get_df_X())
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df_X = pd.read_excel(io.BytesIO(decoded))
            data.set_df_X(df_X)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.Hr(),  # horizontal line
    ])


def generate_data():
        df= Statistics().gerenation_df_severity(0,"")
        return df


titles = Statistics().generate_titles()

layout_SVM = html.Div(children=[
    html.Div(children=[html.Div([
        dcc.Upload(
            id='upload-data',
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
        html.Div(id='output-data-upload')],

    )]),
    html.Div(id='body', className='container scalable', children=[
        html.Div(className='row', children=[
            html.Div(
                id='div-graphs',
                children=dcc.Graph(
                    id='graph-sklearn-svm',
                    style={'display': 'none'}
                )
            ),

            html.Div(
                className='three columns',
                style={
                    'min-width': '24.5%',
                    'max-height': 'calc(100vh - 85px)',
                    'overflow-y': 'auto',
                    'overflow-x': 'hidden',
                },
                children=[
                    drc.Card([
                        drc.NamedDropdown(
                            name='Data X values ',
                            id='dropdown-svm-parameter-X',
                            options=titles,
                            value=titles[0]['value'],
                            clearable=False,
                            searchable=False
                        ),
                        drc.NamedDropdown(
                            name='Select Predict Y values',
                            id='dropdown-svm-parameter-Y',
                            options=titles,
                            value=titles[1]['value'],
                            clearable=False,
                            searchable=False
                        ),
                    ]),

                    drc.Card([
                        drc.NamedSlider(
                            name='Threshold',
                            id='slider-threshold',
                            min=0,
                            max=1,
                            value=0.5,
                            step=0.01
                        ),

                        html.Button(
                            'Reset Threshold',
                            id='button-zero-threshold'
                        ),
                    ]),

                    drc.Card([
                        drc.NamedDropdown(
                            name='Kernel',
                            id='dropdown-svm-parameter-kernel',
                            options=[
                                {'label': 'Radial basis function (RBF)',
                                 'value': 'rbf'},
                                {'label': 'Linear', 'value': 'linear'},
                                {'label': 'Polynomial', 'value': 'poly'},
                                {'label': 'Sigmoid', 'value': 'sigmoid'}
                            ],
                            value='rbf',
                            clearable=False,
                            searchable=False
                        ),

                        drc.NamedSlider(
                            name='Cost (C)',
                            id='slider-svm-parameter-C-power',
                            min=-2,
                            max=4,
                            value=0,
                            marks={i: '{}'.format(10 ** i) for i in
                                   range(-2, 5)}
                        ),

                        drc.FormattedSlider(
                            style={'padding': '5px 10px 25px'},
                            id='slider-svm-parameter-C-coef',
                            min=1,
                            max=9,
                            value=1
                        ),

                        drc.NamedSlider(
                            name='Degree',
                            id='slider-svm-parameter-degree',
                            min=2,
                            max=10,
                            value=3,
                            step=1,

                        ),


                        drc.NamedSlider(
                            name='Gamma',
                            id='slider-svm-parameter-gamma-power',
                            min=-5,
                            max=0,
                            value=-1,
                            marks={i: '{}'.format(10 ** i) for i in
                                   range(-5, 1)}
                        ),

                        drc.FormattedSlider(
                            style={'padding': '5px 10px 25px'},
                            id='slider-svm-parameter-gamma-coef',
                            min=1,
                            max=9,
                            value=5
                        ),

                        drc.NamedRadioItems(
                            name='Shrinking',
                            id='radio-svm-parameter-shrinking',
                            labelStyle={
                                'margin-right': '7px',
                                'display': 'inline-block'
                            },
                            options=[
                                {'label': ' Enabled', 'value': 'True'},
                                {'label': ' Disabled', 'value': 'False'},
                            ],
                            value='True',
                        ),
                    ]),

                ]
            ),
        ]),
    ])
])


@app.callback(Output('slider-svm-parameter-gamma-coef', 'marks'),
              [Input('slider-svm-parameter-gamma-power', 'value')])
def update_slider_svm_parameter_gamma_coef(power):
    scale = 10 ** power
    return {i: str(round(i * scale, 8)) for i in range(1, 10, 2)}


@app.callback(Output('slider-svm-parameter-C-coef', 'marks'),
              [Input('slider-svm-parameter-C-power', 'value')])
def update_slider_svm_parameter_C_coef(power):
    scale = 10 ** power
    return {i: str(round(i * scale, 8)) for i in range(1, 10, 2)}


@app.callback(Output('slider-threshold', 'value'),
              [Input('button-zero-threshold', 'n_clicks')],
              [State('graph-sklearn-svm', 'figure')])
def reset_threshold_center(n_clicks, figure):
    if n_clicks:
        Z = np.array(figure['data'][0]['z'])
        value = - Z.min() / (Z.max() - Z.min())
    else:
        value = 0.4959986285375595
    return value


# Disable Sliders if kernel not in the given list
@app.callback(Output('slider-svm-parameter-degree', 'disabled'),
              [Input('dropdown-svm-parameter-kernel', 'value')])
def disable_slider_param_degree(kernel):
    return kernel != 'poly'


@app.callback(Output('slider-svm-parameter-gamma-coef', 'disabled'),
              [Input('dropdown-svm-parameter-kernel', 'value')])
def disable_slider_param_gamma_coef(kernel):
    return kernel not in ['rbf', 'poly', 'sigmoid']


@app.callback(Output('slider-svm-parameter-gamma-power', 'disabled'),
              [Input('dropdown-svm-parameter-kernel', 'value')])
def disable_slider_param_gamma_power(kernel):
    return kernel not in ['rbf', 'poly', 'sigmoid']


@app.callback(Output('div-graphs', 'children'),
              [Input('dropdown-svm-parameter-kernel', 'value'),
               Input('slider-svm-parameter-degree', 'value'),
               Input('slider-svm-parameter-C-coef', 'value'),
               Input('slider-svm-parameter-C-power', 'value'),
               Input('slider-svm-parameter-gamma-coef', 'value'),
               Input('slider-svm-parameter-gamma-power', 'value'),
               Input('radio-svm-parameter-shrinking', 'value'),
               Input('slider-threshold', 'value'),
               Input('dropdown-svm-parameter-X', 'value'),
               Input('dropdown-svm-parameter-Y', 'value')
               ])
def update_svm_graph(kernel,
                     degree,
                     C_coef,
                     C_power,
                     gamma_coef,
                     gamma_power,
                     shrinking,
                     threshold,
                     titleX,
                     titleY
                     ):

    t_start = time.time()
    h = .3  # step size in the mesh
    shrinking= bool(shrinking)
    # Data Pre-processing
    y = generate_data()[titleY]
    #df_X = data.get_df_X().drop([titleY], axis=1)
    #X = df_X
    dataset = datasets.make_moons(
        n_samples=200,
        noise=0.6,
        random_state=0
    )
   # print(X)
    X, y = dataset
    X = StandardScaler().fit_transform(X) # Requere que tenga una matriz con nejemplos y n columnas

    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.4, random_state=42)

    x_min = X[:, 0].min() - .5
    x_max = X[:, 0].max() + .5
    y_min = X[:, 1].min() - .5
    y_max = X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    C = C_coef * 10 ** C_power
    gamma = gamma_coef * 10 ** gamma_power

    # Train SVM
    clf = SVC(
        C=C,
        kernel=kernel,
        degree=degree,
        gamma=gamma,
        shrinking=shrinking
    )
    clf.fit(X_train, y_train)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    # print(np.c_[xx.ravel(), yy.ravel()])
    if hasattr(clf, "decision_function"):
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

    prediction_figure = serve_prediction_plot(
        model=clf,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        Z=Z,
        xx=xx,
        yy=yy,
        mesh_step=h,
        threshold=threshold
    )

    roc_figure = serve_roc_curve(
        model=clf,
        X_test=X_test,
        y_test=y_test
    )

    confusion_figure = serve_pie_confusion_matrix(
        model=clf,
        X_test=X_test,
        y_test=y_test,
        Z=Z,
        threshold=threshold
    )

    print(
        f"Total Time Taken: {time.time() - t_start:.3f} sec")

    return [
        html.Div(
            className='three columns',
            style={
                'min-width': '24.5%',
                'height': 'calc(100vh - 90px)',
                'margin-top': '5px',

                # Remove possibility to select the text for better UX
                'user-select': 'none',
                '-moz-user-select': 'none',
                '-webkit-user-select': 'none',
                '-ms-user-select': 'none'
            },
            children=[
                dcc.Graph(
                    id='graph-line-roc-curve',
                    style={'height': '40%'},
                    figure=roc_figure
                ),

                dcc.Graph(
                    id='graph-pie-confusion-matrix',
                    figure=confusion_figure,
                    style={'height': '60%'}
                )
            ]),

        html.Div(
            className='six columns',
            style={'margin-top': '5px'},
            children=[
                dcc.Graph(
                    id='graph-sklearn-svm',
                    figure=prediction_figure,
                    style={'height': 'calc(100vh - 90px)'}
                )
            ])
    ]



@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children