from flask import Flask
from interface_api import app

@app.route('/match', methods = ['GET'])
def new_match():
    """Returns a list of all matches or accepts a query to only return the matching ones"""
    pass

@app.route('/heat', methods = ['GET'])
def new_heat():
    """Returns a list of all heats or accepts a query to only return the matching ones"""
    pass

@app.route('/new_match', methods = ['POST'])
def new_match():
    """Adds a new match to the match table"""
    pass

@app.route('/new_heat', methods = ['POST'])
def new_heat():
    """Adds a new heat to the heat table"""
    pass

@app.route('/delete_match/<int:match_id>', methods = ['DELETE'])
def delete_match(match_id):
    """Deletes a match"""
    pass

@app.route('/delete_heat/<int:heat_id>', methods = ['DELETE'])
def delete_heat():
    """Deletes a heat"""
    pass
