
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
    """Retrieve Hawaii's previous year precipitation amount"""
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
        """list of the Hawaiian stations"""
        stations_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

        stations = []
        for result in results:
            station_dict = {}
            station_dict['station'] = result.station
            station_dict['name'] = result.name
            station_dict['latitude'] = result.latitude
            station_dict['longitude'] = result.longitude
            station_dict['elevation'] = result.elevation
            stations.append(station_dict)

        return jsonify(stations)


@app.route("/api/v1.0/temperature")

def temperature():
    #Obtain databases last date:
    last_date_measurement = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date_measurement = last_date_measurement[0]
    # Calculate a date one year before the databases last date:
    one_year_ago = dt.datetime.strptime(last_date_measurement, '%Y-%m-%d') - dt.timedelta(days=365)   
    
    # Design a query to retrieve temperature observations (tobs) for the databases last year:  
    last_year_temp_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(Measurement.date > one_year_ago).all()

    last_year_temp_list = []
    for temp_result in last_year_temp_results:
        temp_dict = {}
        temp_dict['date'] = temp_result[0]
        temp_dict['station'] = temp_result[1]
        temp_dict['tobs'] = float(temp_result[2])

        last_year_temp_list.append(temp_dict)

    return jsonify(last_year_temp_list) 

@app.route("/api/v1.0/<start>")

def temp_start_to_last_date(start = 'temp_start'):
    """Obtain Hawaii's temp_min, temp_avg and temp_max for designated dates: """
    # Search to retrieve temperature observations for all dates greater than or equal to temp_start:
      
    if start is None:
        return jsonify({"error": f"Enter a start date"}), 404

    temp_start =  dt.datetime.strptime(start, "%Y-%m-%d").date() 
    temp_start_to_last_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= temp_start).all()
    
    temp_start_to_last_list = []
    for temp_start_to_last_result in temp_start_to_last_results:
        temp_start_to_last_dict = {}
        temp_start_to_last_dict['date'] = temp_start_to_last_result[0]
        temp_start_to_last_dict['station'] = temp_start_to_last_result[1]
        temp_start_to_last_dict['tobs'] = float(temp_start_to_last_result[2])

        temp_start_to_last_list.append(temp_start_to_last_dict)
    return jsonify(temp_start_to_last_list)

@app.route("/api/v1.0/<start>/<end>")
  
def temp_start_to_end_date(start = 'temp_start_date', end = 'temp_end_date'):
    """Obtain Hawaii's temp_min, temp_avg and temp_max for designated dates"""
    # Obtain temperature observations for all dates BETWEEN the designated start and end dates:
    if start or end is None:
        return jsonify({"error": f"Please enter a start and/or end date"}), 404

    # Start date: 
    temp_start_date =  dt.datetime.strptime(start, "%Y-%m-%d").date()

    # End date:
    temp_end_date =  dt.datetime.strptime(end, "%Y-%m-%d").date()
    
    # Obtain temperature observations for all dates BETWEEN <temp_start_date> and <temp_end_date>:
    temp_start_to_end_date_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= temp_start_date).\
        filter(Measurement.date <= temp_end_date).all()

    start_to_end_temp_list = []
    for result in temp_start_to_end_date_results:
        temp_start_to_end_dict = {}
        temp_start_to_end_dict['date'] = result[0]
        temp_start_to_end_dict['station'] = result[1]
        temp_start_to_end_dict['tobs'] = float(result[2])

        start_to_end_temp_list.append(temp_start_to_end_dict)

    return jsonify(start_to_end_temp_list) 


if __name__ == '__main__':
    app.run(debug=True)