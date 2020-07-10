#from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html

print(dcc.__version__) # 0.6.0 or above is required

external_css = ["https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/chriddyp/pen/bWLwgP.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

app = dash.Dash(external_stylesheets=external_css)

