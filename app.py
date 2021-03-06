from flask import Flask

app = Flask(__name__)

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base=automap_base()

Base.prepare(engine, reflect=True)

Measurement=Base.classes.measurement
Station=Base.classes.station

session=Session(engine)

@app.route("/")
def home():
    session=Session(engine)
    return (
        "Here are the available routes:<br/>"
        "/precipitation<br/>"
        "/stations<br/>"
        "/tobs"
    )

@app.route("/precipitation")
def precipitation():
    session=Session(engine)
    precipitation_data=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(Measurement.date).all()
    
    output_list=[]
    for each_result in precipitation_data:
        output={}
        output['date']=each_result[0]
        output['precipitation']=each_result[1]
        output_list.append(output)
    
    return jsonify(output_list)

@app.route("/stations")
def stations():
    session=Session(engine)
    station_count=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station)).all()

    stations_output_list=[]
    for each in station_count:
        output={}
        output['Station']=each[0]
        output['Number of Observations']= each[1]
        stations_output_list.append(output)
    
    return jsonify(stations_output_list)

@app.route("/tobs")
def tobs():
    session=Session(engine)
    temp_year=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=="USC00519397").filter(Measurement.date>"2016-08-23").all()
    
    temp_output_list=[]
    for each in temp_year:
        output={}
        output['Date']=each[0]
        output['Temperature']= each[1]
        temp_output_list.append(output)
    
    return jsonify(temp_output_list)

@app.route("/start/<start_date>/<end_date>")
def state(start_date, end_date):
    session=Session(engine)
    def calc_temps(start_date, end_date):
        
        """TMIN, TAVG, and TMAX for a list of dates.
        
        Args:
            start_date (string): A date string in the format %Y-%m-%d
            end_date (string): A date string in the format %Y-%m-%d
            
        Returns:
        TMIN, TAVE, and TMAX
        """
        
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    calcs = calc_temps(start_date, end_date)

    
    output={}
    output['Minimum, Maximum, Average Temperature']=calcs[0]
        

    return jsonify(output)





if __name__ == "__main__":
    app.run(debug=True)