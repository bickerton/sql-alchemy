
#set dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#Define the path to the hawaii.sqlite database

engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")
    
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/temperature<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end<br>"
        

    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    """Returns precipitation for Hawaii for the past year"""
    one_year_ago = "2016-08-23"
    annual_precipitation = session.query(Measurement.date, Measurement.station, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    annual_precipitation_results = []
    for result in results:
        prcp_dict ={}
        prcp_dict['date'] = result.date
        prcp_dict['station'] = result.station
        prcp_dict['prcp'] = result.prcp
        annual_precipitation_results.append(prcp_dict)

    return jsonify(annual_precipitation_results)

    @app.route('/api/v1.0/stations')

    def stations():
        """lists of Hawaiian stations"""
        stations_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

        stations =[]
        for result in results:
            station_dict = {}
            station_dict['station'] = result.station
            station_dict['name'] = result.name
            station_dict['latitude'] = result.latitude
            station_dict['longitude'] = result.longitude
            station_dict['elevation'] = result.elevation
            stations.append(station_dict)

        return jsonify(stations)