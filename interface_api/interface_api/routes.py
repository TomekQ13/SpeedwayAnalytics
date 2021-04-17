from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from interface_api import db
from interface_api.models import Heat, Match
from interface_api.utils import Serialize

main = Blueprint('main', __name__)

@main.route('/match', methods = ['GET'])
def match():
    """Returns a list of all matches or accepts parameters which are columns from the match table and create dynamic filter"""
    # if there are no parameters then return all matches
    if not request.args.to_dict():
        return jsonify(Serialize.serialize_list(Match.query.all(), excl_list=['heats']))

    # Checks if there are no unknown query parameters - if there are display a message
    for key in request.args.keys():
        if key not in Match.__dict__:
            return jsonify({'message': 'Unknown query parameter.'})

    # Takes all GET request parameters and translates them to a SQLAlchemy query parameters
    query = Match.query
    for key, value in request.args.items():
        query = query.filter(getattr(Match, key) == value)    
    
    return jsonify(Serialize.serialize_list(query.all(), excl_list=['heats']))

@main.route('/heat', methods = ['GET'])
def heat():
    """Returns a list of all heats or accepts a query to only return the matching ones"""
    # if there are no parameters then return all matches
    if not request.args.to_dict():
        return jsonify(Serialize.serialize_list(Heat.query.all(), excl_list=['match']))

    # Checks if there are no unknown query parameters - if there are display a message
    for key in request.args.keys():
        if key not in Heat.__dict__:
            return jsonify({'message': 'Unknown query parameter.'})

    # Takes all GET request parameters and translates them to a SQLAlchemy query parameters
    query = Heat.query
    for key, value in request.args.items():
        query = query.filter(getattr(Heat, key) == value)    

    return jsonify(Serialize.serialize_list(query.all(), excl_list=['match']))

@main.route('/new_match', methods = ['POST'])
def new_match():
    """Adds a new match to the match table"""
    attributes = request.get_json()
    # check if there are any parameters - if no it would cause a runtime error with **
    if not attributes:
        return jsonify({'message': 'No parameters provided with the request.'})

    match = Match(**attributes)
    db.session.add(match)

    # Tries to add the match to the table, if catches IntegrityError it means that integrity constraint was violated
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'message': 'Integrity constraint violated', 'error_message': str(e)})
    except Exception as e:
        return jsonify({'message': 'Error encountered while trying to add the match', 'error_message': str(e)})

    return jsonify({'message': 'Match added successfully.'})    

@main.route('/new_heat', methods = ['POST'])
def new_heat():
    """Adds a new heat to the heat table"""
    attributes = request.get_json()
    # check if there are any parameters - if no it would cause a runtime error with **
    if not attributes:
        return jsonify({'message': 'No parameters provided with the request.'})
 
    match = Heat(**attributes)
    db.session.add(match)

    # Tries to add the match to the table, if catches IntegrityError it means that integrity constraint was violated
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify({'message': 'Integrity constraint violated', 'error_message': str(e)})
    except Exception as e:
        return jsonify({'message': 'Error encountered while trying to add the match', 'error_message': str(e)})

    return jsonify({'message': 'Match added successfully.'})    

@main.route('/delete_match', methods = ['DELETE'])
def delete_match():
    """Deletes a match"""
    match_id = request.args.get('match_id')
    if not match_id:
        return jsonify({'message': 'Please specify a match_id as a request parameter.'})

    match = Match.query.get(match_id)
    if not match:
        return jsonify({'message': 'Match with this match_id does not exist.'})

    try:
        db.session.delete(match)
        db.session.commit()
        return jsonify({'message': 'Match deleted'})
    except Exception as e:
        return jsonify({'message': 'Error occured during delete', 'error_message': str(e)})


@main.route('/delete_heat', methods = ['DELETE'])
def delete_heat():
    """Deletes a heat"""
    heat_id = request.args.get('heat_id')
    if not heat_id:
        return jsonify({'message': 'Please specify a heat_id as a request parameter.'})

    heat = Match.query.get(heat_id)
    if not match:
        return jsonify({'message': 'Heat with this heat_id does not exist.'})

    try:
        db.session.delete(heat)
        db.session.commit()
        return jsonify({'message': 'Heat deleted'})
    except Exception as e:
        return jsonify({'message': 'Error occured during delete', 'error_message': str(e)})
