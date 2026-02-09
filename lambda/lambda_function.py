import json
import boto3
import uuid

SESSION_ID = str(uuid.uuid4()) + str(uuid.uuid4())

# Placeholder ARN - needs to be updated with the actual watering agent ARN
AGENT_RUNTIME_ARN = 'arn:aws:bedrock-agentcore:us-west-2:533267235251:runtime/plant_watering-0u0rMsAxuN'
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
    
    # No more cron processing needed for the simplified output

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
