# 植物浇水行为检测 (Plant Watering Detection Project)

本项目利用 AWS SQS、Lambda 和 Bedrock AgentCore 实现了一个植物浇水行为检测系统。

## 项目流程

项目的核心处理流程如下：

1.  **发送 SQS 消息**:
    -   向输入 SQS 队列 (`plant-watering`) 发送消息。
    -   消息内容包含任务 UUID (`uuid`) 和植物视频链接 (`video_url`)。
    -   发送的 SQS 消息示例：
        ```json
        {
          "uuid": "xxx1",
          "video_url": "https://s3.xxx.xxx.mp4"
        }
        ```
    -   示例脚本：`lambda/test_sqs.py`。

2.  **Lambda 处理**:
    -   AWS Lambda 函数 (`lambda/lambda_function.py`) 被输入 SQS 队列中的新消息触发。
    -   Lambda 解析消息内容，为调用 Agent 做好准备。

3.  **Agentcore 处理**:
    -   Lambda 函数调用 **Bedrock AgentCore** 运行时。
    -   Agent (逻辑位于 `agent/src/app.py` 和 `agent/src/agent.py`) 对输入视频进行分析，**检测视频中是否发生了浇水行为**。

4.  **发送 SQS 结果**:
    -   Lambda 函数获取 Agent 的处理结果。
    -   发送到结果消息队列的内容格式示例：
        ```json
        {
          "uuid": "xxx1",
          "plant_name": "绿萝 (Epipremnum aureum)",
          "is_watering": "1" // "1" 表示检测到浇水动作，"0" 表示未检测到
        }
        ```
    -   最后，Lambda 将结果发送到输出 SQS 队列 (`watering-result`)，供后续系统使用。
