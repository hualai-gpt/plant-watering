# 植物自动浇水系统 (Plant Watering Project)

本项目利用 AWS SQS、Lambda 和 Bedrock AgentCore 实现了一个植物浇水监测与建议系统。

## 项目流程

项目的核心处理流程如下：

1.  **发送 SQS 消息**:
    -   向输入 SQS 队列 (`plant-watering`) 发送消息。
    -   消息内容通常包含用户的问题 (`user_message`) 和植物照片的链接 (`image_url`)。
    -   发送的 SQS 消息示例：
        ```json
        {
          "uuid": "xxx1",
          "user_message": "这是什么植物？需要怎么浇水？",
          "image_url": "https://s3.xxx.xxx.jpeg"
        }
        ```
    -   示例脚本：`lambda/test_sqs.py`。

2.  **Lambda 处理**:
    -   AWS Lambda 函数 (`lambda/lambda_function.py`) 被输入 SQS 队列中的新消息触发。
    -   Lambda 解析消息内容，为调用 Agent 做好准备。

3.  **Agentcore 处理**:
    -   Lambda 函数调用 **Bedrock AgentCore** 运行时。
    -   Agent (逻辑位于 `agent/src/app.py` 和 `agent/src/agent.py`) 对输入进行分析，识别植物状态并生成浇水建议。

4.  **发送 SQS 结果**:
    -   Lambda 函数获取 Agent 的处理结果。
    -   发送到结果消息队列的内容格式示例：
        ```json
        {
          "uuid": "xxx1",
          "plant_name": "绿萝 (Epipremnum aureum)",
          "plant_water_type": "中等水分植物",
          "soil_moisture_pref": "保持湿润但不要积水",
          "watering_schedule": [
            {
              "time": "08:00",
              "frequency_days": 3,
              "amount_ml": 200
            }
          ],
          "watering_schedule_cron": [
            {
              "cron": "0 8 */3 * *",
              "amount_ml": 200
            }
          ]
        }
        ```
    -   最后，Lambda 将结果发送到输出 SQS 队列 (`watering-result`)，供后续系统使用。
