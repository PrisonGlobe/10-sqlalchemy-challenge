import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end"
    )


# Precipitation route & queries
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-8-23").all()
    session.close()

    year_prcp = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        year_prcp.append(precipitation_dict)

    return jsonify(year_prcp)


# Stations route & queries
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# Tobs routes & queries
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281')
    session.close

    year_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        year_tobs.append(tobs_dict)

    return jsonify(year_tobs)


# Start routes & queries
@app.route("/api/v1.0/start")
def start_date():
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close

    start_tobs = []
    for min, max, avg in results:
        start_tobs_dict = {}
        start_tobs_dict["Min"] = min
        start_tobs_dict["Max"] = max
        start_tobs_dict["Avg"] = avg
        start_tobs.append(start_tobs_dict)

    return jsonify(start_tobs)

# Start & end routes & queries
@app.route("/api/v1.0/start/end")
def start_end(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    session.close

    start_end_tobs = []
    for min, max, avg in results:
        start_tobs_dict = {}
        start_tobs_dict["Min"] = min
        start_tobs_dict["Max"] = max
        start_tobs_dict["Avg"] = avg
        start_end_tobs.append(start_tobs_dict)

if __name__ == "__main__":
    app.run(debug=True)