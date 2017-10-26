from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

bootstrap = Bootstrap(app)

forecast_files = os.listdir(app.static_folder + "/forecasts/")


@app.route('/')
def list_forecasts():
    print("Entered list_forecasts!\n")
    if len(forecast_files) == 0:
        return "No files found"
    else:
        return render_template('index.html', forecast_files=forecast_files)


@app.route('/print/<forecast_file_name>')
def print_json(forecast_file_name):
    with open(app.static_folder + "/forecasts/" + forecast_file_name, 'r') as f:
        return render_template('forecast.html', json_forecast="\n".join(f.readlines()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
