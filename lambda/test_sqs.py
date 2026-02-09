import boto3
import json

# 配置 AWS SQS 队列 URL
# 请将其替换为您实际的 SQS 队列 URL
QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/533267235251/plant-watering'
QUEUE_URL_RESULT = 'https://sqs.sa-east-1.amazonaws.com/533267235251/watering-result'

def send_test_message():
    # 创建 SQS 客户端
    # 注意：确保您的环境已配置好 AWS 凭证 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    sqs = boto3.client('sqs', region_name='us-west-2')

    # 定义要发送的消息内容
    # 根据 lambda_function.py 和 agent/src/app.py 的逻辑，
    # 消息体应该包含 user_message 和 image_url
    message_body = {
        "uuid": "112233",
        "user_message": "这盆植物需要多久浇一次水？",
        "image_url": "https://x0.ifengimg.com/res/2021/3A0B3E675294EF361660148644661948F43E6417_size141_w1080_h1350.jpeg"
    }

    try:
        # 发送消息
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message_body)
        )
        
        print(f"消息发送成功！MessageId: {response['MessageId']}")
        print(f"发送的消息内容: {json.dumps(message_body, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"消息发送失败: {str(e)}")

if __name__ == "__main__":
    send_test_message()
