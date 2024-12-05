import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['checkersboard']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Extract HTTP method
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return get_board(event)
    elif http_method == 'POST':
        return update_board(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }

def get_board(event):
    game_id = event['queryStringParameters']['GameID']
    response = table.get_item(Key={'GameID': game_id})
    item = response.get('Item', {})
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

def update_board(event):
    body = json.loads(event['body'])
    game_id = body['GameID']
    board_state = body['BoardState']
    turn = body['Turn']
    table.put_item(
        Item={
            'GameID': game_id,
            'BoardState': board_state,
            'Turn': turn
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Board updated successfully')
    }