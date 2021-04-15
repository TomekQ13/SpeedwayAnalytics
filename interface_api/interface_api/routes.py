from flask import Flask, request, jsonify, Blueprint
from interface_api.models import Heat, Match
from interface_api.utils import Serialize

main = Blueprint('main', __name__)

@main.route('/match', methods = ['GET'])
def match():
    """Returns a list of all matches or accepts parameters which are columns from the match table and create dynamic filter"""
    # Checks if there are no unknown query parameters - only match_id is accepted
    for key in request.args.keys():
        if key not in Match.__dict__:
            return jsonify({'message': 'Unknown query parameter.'})

    match_id = request.args.get('match_id')
    print(request.args.to_dict())
    if match_id:
        return jsonify(Match.query.get(match_id).serialize(excl_list=['heats']))
    else:        
        return jsonify(Serialize.serialize_list(Match.query.filter(request.args.to_dict())))

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
