from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
import os
import json
import datetime

# TODO Create Model
# TODO Iterate through JSON files loading date

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'anawd.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
db = SQLAlchemy(app)


class DailyForecast(db.Model):
    __tablename__ = 'daily_forecasts'
    id = db.Column(db.Integer, primary_key=True)
    retrieved_date = db.Column(db.String(8), unique=False, index=True)
    forecast_date = db.Column(db.String(8), index=True)
    max_temp = db.Column(db.Numeric)
    min_temp = db.Column(db.Numeric)
    precip_prob = db.Column(db.Numeric)

    def __repr__(self):
        return '<DailyForecast %r>' % self.retrieved_date


class ForecastsForDay(db.Model):
    __tablename__ = 'forecasts_for_day'
    id = db.Column(db.Integer, primary_key=True)
    forecast_date = db.Column(db.String(8), unique=True, index=True)
    max_temp = db.Column(db.Numeric)
    min_temp = db.Column(db.Numeric)
    precip_prob = db.Column(db.Numeric)

    def __repr__(self):
        return '<DailyForecast %r>' % self.retrieved_date


def julian(timesecs):
    return timesecs.strftime('%Y%j')


def summarize_weather(filename):
    filename = os.path.join(basedir, 'static', 'forecasts', filename)
    file = open(filename, "r")
    forecast = json.load(file)
    # print(forecast["daily"]["data"])
    for day in forecast["daily"]["data"]:
        daytime = datetime.datetime.fromtimestamp(day["time"])
        print(daytime.strftime('%Y%j'), "Min=", day["temperatureMin"], "Max=", day["temperatureMax"],
              "Precip%=", day["precipProbability"], "fndate=", filename[-12:-5])
        fc = DailyForecast(retrieved_date=filename[-12:-5], forecast_date=daytime.strftime('%Y%j'),
                           max_temp=day["temperatureMax"], min_temp=day["temperatureMin"],
                           precip_prob=day["precipProbability"])
        db.session.add(fc)


def list_data():
    forecast_files = os.listdir(app.static_folder + "/forecasts/")
    for fn in forecast_files:
        summarize_weather(fn)


def make_shell_context():
    return dict(app=app, db=db, DailyForecast=DailyForecast)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    # manager.run()
    list_data()
    db.session.commit()
