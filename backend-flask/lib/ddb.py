import boto3
import sys
from datetime import datetime, timedelta, timezone
import uuid
import os
import botocore.exceptions

class Ddb:
  def client():
    endpoint_url = os.getenv("AWS_ENDPOINT_URL")
    if endpoint_url:
      attrs = { 'endpoint_url': endpoint_url }
    else:
      attrs = {}
    dynamodb = boto3.client('dynamodb',**attrs)
    return 

#list msgs
    def list_messages(client,message_group_uuid):
        year = str(datetime.now().year)
    table_name = 'cruddurmessages'
    query_params = {
      'TableName': table_name,
      'KeyConditionExpression': 'partitionKey = :partitionKey AND begins_with(secondaryKey,:year)',
      'ScanIndexForward': False,
      'Limit': 20,
      'ExpressionAttributeValues': {
        ':year': {'S': year },
        ':partitionKey': {'S': f"MSG#{message_group_uuid}"}
      }
    }

    response = client.query(**query_params)
    items = response['Items']
    items.reverse()
    results = []
    for item in items:
      created_at = item['secondaryKey']['S']
      results.append({
        'uuid': item['message_uuid']['S'],
        'display_name': item['user_display_name']['S'],
        'handle': item['user_handle']['S'],
        'message': item['message']['S'],
        'created_at': created_at
      })
    return results



    #list msg groups
    def list_message_groups(client,my_user_uuid):
        year = str(datetime.now().year)
    table_name = 'cruddurmessages'
    query_params = {
      'TableName': table_name,
      'KeyConditionExpression': 'partitionKey = :partitionKey AND begins_with(secondaryKey,:year)',
      'ScanIndexForward': False,
      'Limit': 20,
      'ExpressionAttributeValues': {
        ':year': {'S': year },
        ':partitionKey': {'S': f"GRP#{my_user_uuid}"}
      }
    }
    print('query-params:',query_params)
    print(query_params)
    # query the table
    response = client.query(**query_params)
    items = response['Items']
    

    results = []
    for item in items:
      last_sent_at = item['secondaryKey']['S']
      results.append({
        'uuid': item['message_group_uuid']['S'],
        'display_name': item['user_display_name']['S'],
        'handle': item['user_handle']['S'],
        'message': item['message']['S'],
        'created_at': last_sent_at
      })
    return results