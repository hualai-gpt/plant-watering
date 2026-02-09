import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-west-2')
payload = json.dumps(
    {
        "uuid": "001",
        "video_url": "https://ai-gpt-eval-images.s3.us-west-2.amazonaws.com/2026-02-09-103853.mp4?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjELv%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCT6S%2Bb3mzf9c5VIz6M5apTvQ%2BFmGi%2B4AroRvjNy1YysAIhAOHG9HRy%2FTYGDGFCQSFXnWKDiCPBIG%2FbyJTPlPTE2VIzKtAECIT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMMTk3NTc4MDM3Mjg2Igwd5NouNqfS%2FcS8ay0qpAS6QaKiFGAl%2Bq4uuKgdBQrAJ5AQk40PYstqHJPWpKnhX2xJbilMVEsalxPfNM1%2BPid7b9ULY5QxpjNwbis6aZzJQM7gKLVXNCj%2BPQQqGQM%2B3M8jKoALM3JzUyhMoyCQYeB7dQYSX6oRa6VNXKbAZRyk6HRdIchYEcHtph2epYd5wXTqGNR6tamm60k6cgEPVz4W2yol0N5OOXUr6ewv7w90%2FxUDsix33mr84f4NQrHfrzxzArQi6WaS533%2FRZ8VMgdywEQuDJHklJoblbIxYSIedxOgxJ540GNu75MVz4cO4Z5g5ffyRjMC4GgbR1Ni%2BbdcNfbY79c%2FQp%2BlsCuNXgMnNIpSKMe1Wl%2BdUfU2XX9YhQMcFh2KdHVS%2F5T8cmd3mCwrUAWM%2BPuCp3LvUeTz9EFSAaFV2pnRrdK5CvuO8Nmr63f4ul03tpfMcl01hVHXZljnsgUpGBD1EuID3BRv4tvZm389Q42e%2BNc7kqK6GplaCj%2BZ%2B35pHCk6hKltR9wqQXBRBuKqqmpXBw6Lx0YN7sjlkja9MhLbQgoGNu50pwusp27h74pHLDyfIEhfeH2TPOvWoa1RJUD94CZeEeejyfv3Z8vY14RM%2BGmGDBFODbTDF88uLyAk6amV0wagy%2B2bPXMhE1ubi%2BLKmMdf1y%2BewHYoEtVemii4guqD2uYs4xmik3U5pjsVrpZa488gsE8RC7xxrfAk2W4SHGH5c6LUzpFr5INvgTD3m6XMBjrCAuq4L9TI%2FSr9muIP538oAuCaBzNwA68w3pEE5qhTVtqMpwEZntl6n2Xlh6ESD5xgQs%2FdgLSjXhuElAhJ15q57h01qxvwK1fHt6d4Mziv3Ez0653D8Nio1To1C9Bhq9lj6lLcgfhYBdCssPOlRSUcPWmOZjxO23zpfI7MEWxYwm2XxjLlSVGbJ6CBV6ugf05Iv589aAOKg4GRYIDtBCE9pRg7Vuc0uJcKHfsKbCCh5%2BjNcJ6UnxUAIomuetZ1Jlhw%2FwfbQEhbsTjj17CJhygG8%2F71OiZCFt4y1PLlY8tEjhWHgeugi%2BedXTZRuAECTAfuujoiuJ7Qudt5FZau2qgU%2B2hN8h56osn0EiCnIuiHfzEgjY5iTdmxHpMHZpFcbEb3OwNa8uaUhtJVJT4O0vQWQSXTf1IT1%2Bfhc0D8psKto8Yui04%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAS4AERTATOEIBKENE%2F20260209%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260209T030226Z&X-Amz-Expires=28800&X-Amz-SignedHeaders=host&X-Amz-Signature=4c202dbe57a6849ffe38272760219bcfa3fc1ff98d3ce3678b3f88ab8963cb91"
    }
)
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-west-2:533267235251:runtime/plant_watering-0u0rMsAxuN',
    runtimeSessionId='e37d91c1-8d94-4099-9542-fe249bc7e642', # Must be 33+ char. Every new SessionId will create a new MicroVM
    payload=payload,
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print(response_data)