from flask import Flask, Response, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import boto3
import request
from botocore.exceptions import ClientError
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

#Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Path to JSON file for initial board state
INITIAL_BOARD_PATH = "static/checkersboard.json"

# S3 bucket URL for the game template
bucket_url = "https://raw.githubusercontent.com/cs399f24/Checkers/development/templates/index.html"

# S3 bucket name
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# Route to get the game template
@app.route('/test')
def test():
    return "Hello World"

# Route to get the game template
@app.route('/')
def index():
    with open(INITIAL_BOARD_PATH, 'r') as f:
        game = json.load(f)
    # board = game["board"]
    return render_template('index.html', board = game["board"])


# Route to get the board from DynamoDB
@app.route('/getBoard', methods=['GET'])
def get_board():
    response = dynamodb.get_item(
        TableName='CheckersBoard',
        Key={'gameId': {'S': 'defaultBoard'}}
    )
    if 'Item' in response:
        board = response['Item']['board']['S']
        return jsonify({"board": board}), 200
    return jsonify({"error": "Board not found"}), 404

#Websocket to handle game updates
@socketio.on('game_update')
def handle_game_update(data):
    # emit('game_update', data, broadcast=True)
    board = data['board']

    #TODO: add move validation logics here
    is_valid = validate_move(board)
    if is_valid:
        #update board to all clients
        emit ('game_update', {'board': board}, broadcast=True)
    else:
        emit ('invalid_move', {'message' 'Invalid move'}, room = request.sid)

def validate_move(board):
    # add game rules logic to validate the move
    return True

# Websocket to handle chat messages
@socketio.on('connect')
def handle_connect():
    print("Client connected")

# Websocket to handle client disconnect
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)