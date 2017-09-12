from flask import Flask, render_template
import os

app = Flask(__name__)

forecast_files = os.listdir(app.static_folder + "/forecasts/")


@app.route('/')
def list_forecasts():
    return render_template('index.html', forecast_files=forecast_files)


@app.route('/print/<forecast_file_name>')
def print_json(forecast_file_name):
    with open(app.static_folder + "/forecasts/" + forecast_file_name, 'r') as f:
        return render_template('forecast.html', json_forecast="\n".join(f.readlines()))


if __name__ == '__main__':
    app.run()
dfdfd