from flask import Flask, request, jsonify, Blueprint
from interface_api.models import Heat, Match

main = Blueprint('main', __name__)

@main.route('/match', methods = ['GET'])
def match():
    match_id = request.args.get('match_id')
    if match_id:
        return jsonify(Match.query.get(match_id))
    else:
        matches = [x for x in Match.query.all()]
        return jsonify()

@main.route('/heat', methods = ['GET'])
def heat():
    """Returns a list of all heats or accepts a query to only return the matching ones"""
    pass

@main.route('/new_match', methods = ['POST'])
def new_match():
    """Adds a new match to the match table"""
    pass

@main.route('/new_heat', methods = ['POST'])
def new_heat():
    """Adds a new heat to the heat table"""
    pass

@main.route('/delete_match/<int:match_id>', methods = ['DELETE'])
def delete_match(match_id):
    """Deletes a match"""
    pass

@main.route('/delete_heat/<int:heat_id>', methods = ['DELETE'])
def delete_heat():
    """Deletes a heat"""
    pass
