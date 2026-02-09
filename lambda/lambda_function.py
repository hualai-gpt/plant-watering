import json
import boto3
import uuid
from util import time_to_cron

SESSION_ID = str(uuid.uuid4()) + str(uuid.uuid4())

# Placeholder ARN - needs to be updated with the actual watering agent ARN
AGENT_RUNTIME_ARN = 'arn:aws:bedrock-agentcore:us-west-2:533267235251:runtime/watering_agent-PLACEHOLDER'
SQS_QUEUE_URL = 'https://sqs.sa-east-1.amazonaws.com/533267235251/watering-result'

def lambda_handler(event, context):
    print("event: ", event)
    body = event['Records'][0]['body']
    payload = json.loads(body)
    msg_uuid = payload.get('uuid')
    print("event: ", event)
    print("uuid: ", msg_uuid)

    session_id = SESSION_ID
    print("session_id: ", session_id)

    try:
        client = boto3.client('bedrock-agentcore', region_name='us-west-2')
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=json.dumps(payload),
        )
        response_body = response['response'].read()
        print("response_body type: ", type(response_body))
        response_data = json.loads(response_body)
        print("response_data type: ", type(response_data))
        response_json = json.loads(response_data)
        print("response_json type: ", type(response_json))
    except Exception as e:
        print("Error invoking agent runtime: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    if msg_uuid:
        response_json['uuid'] = msg_uuid
    
    # Process watering schedule to cron
    response_json['watering_schedule_cron'] = []
    if 'watering_schedule' in response_json:
        for schedule in response_json['watering_schedule']:
            time_str = schedule.get('time')
            frequency = schedule.get('frequency_days', 1)
            try:
                cron_expr = time_to_cron(time_str, frequency)
                response_json['watering_schedule_cron'].append({
                    "cron": cron_expr,
                    "amount_ml": schedule.get('amount_ml')
                })
            except ValueError as e:
                print(f"Error converting schedule to cron: {e}")

    # json 格式化输出
    print("response_data: ", json.dumps(response_json, indent=2, ensure_ascii=False))

    # 将 response_data 发送到 SQS
    try:
        sqs = boto3.client('sqs', region_name='sa-east-1')
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(response_json)
        )
        print("Message sent to SQS: ", response)
    except Exception as e:
        print("Error sending message to SQS: ", e)

    return {
        'statusCode': 200,
        'body': json.dumps(response_json)
    }
