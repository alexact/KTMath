import dash

external_css = [
    # Normalize the CSS
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    # Fonts
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
]
app = dash.Dash(__name__,  assets_external_path=external_css, assets_folder='../assets/')
server = app.server
app.config.suppress_callback_exceptions = True