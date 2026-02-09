# Code Review Report

## Project Overview
A plant grow light advisory system using AWS SQS, Lambda, and Bedrock AgentCore with a Gemini-based agent for analyzing plant images and providing lighting recommendations.

---

## 1. Project Structure

### Current Structure
```
plant-grow-light/
├── agent/
│   ├── src/
│   │   ├── app.py          # Main entrypoint for agent invocation
│   │   ├── agent.py        # Agent creation with Gemini model
│   │   ├── model.py        # Unused/test model file
│   │   └── scheme.py       # Pydantic models for structured output
│   ├── test/
│   │   ├── test_agentcore.py  # AWS Bedrock AgentCore integration test
│   │   └── test_agent_local.py # Local agent test
│   ├── requirements.txt
│   ├── .bedrock_agentcore.yaml
│   └── README.md
├── lambda/
│   ├── lambda_function.py  # AWS Lambda handler for SQS events
│   └── test_sqs.py         # SQS message sender test
├── README.md
└── .gitignore
```

### Structure Issues
1. **model.py appears unused/dead code** - This file contains standalone test code with hardcoded API calls and is never imported elsewhere
2. **No virtual environment setup** - Missing requirements for virtual environment isolation
3. **Tests mixed with test data** - Test directory contains image files (2.jpg, 3.jpg) and .DS_Store
4. **No consistent entry point** - Multiple entry patterns (app.run() vs direct function calls)

---

## 2. Bugs and Issues

### Critical Bugs

#### `lambda/lambda_function.py:5-6`
```python
SESSION_ID = str(uuid.uuid4()) + str(uuid.uuid4())
```
**Issue:** Module-level session ID is created once when the Lambda container is initialized, not per-invocation. This causes session reuse across different requests.

**Fix:** Move session ID generation inside `lambda_handler`:
```python
session_id = str(uuid.uuid4()) + str(uuid.uuid4())
```

#### `lambda/lambda_function.py:9`
```python
body = event['Records'][0]['body']
```
**Issue:** No validation that `Records` exists or has elements. Will raise `KeyError` or `IndexError` on invalid events.

**Fix:** Add proper validation:
```python
if not event.get('Records'):
    return {'statusCode': 400, 'body': json.dumps({'error': 'No Records in event'})}
```

### Medium Severity Bugs

#### `agent/src/agent.py:16`
```python
model_id="gemini-3-flash-preview",
```
**Issue:** Preview model IDs may become unstable. Using preview models in production is risky.

**Fix:** Use stable model IDs or pin to specific versions.

#### `agent/src/model.py:37`
```python
result = asyncio.run(main())
```
**Issue:** Unused test code left in codebase. This file is never imported and contains incomplete/outdated implementation.

**Fix:** Remove or move to proper test directory.

#### `agent/src/app.py:52`
```python
"format": "jpeg",
```
**Issue:** Hardcoded JPEG format regardless of actual image type. The code validates Content-Type but then assumes JPEG.

**Fix:** Detect actual image format from Content-Type or response content.

### Minor Bugs

#### `agent/src/app.py:23-24`
```python
if image_url and not (image_url.startswith("http://") or image_url.startswith("https://")):
    return {"error": "Invalid image URL. Must start with http:// or https://"}
```
**Issue:** URL validation is case-sensitive but protocol schemes can be uppercase.

**Fix:** Use `url.lower().startswith()` or `urllib.parse.urlparse()`.

#### `lambda/test_sqs.py:6`
```python
QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/533267235251/plant-grow-light'
```
**Issue:** Hardcoded queue URL different from lambda_function.py queue URL (sa-east-1).

**Fix:** Use environment variables for configuration.

---

## 3. Security Issues

### Critical Security Issues

#### `.env file referenced but missing`
`agent.py:7-11` loads `.env` file and raises error if `GOOGLE_API_KEY` is missing. This is good, but:
- The `.env` file is listed in `.gitignore` but was checked (per `.DS_Store` having git flag)
- No mention of `.env` in the directory listing means it's not present

**Risk:** Missing API key causes runtime failures.

#### `agent/src/app.py:42`
```python
response = requests.get(image_url, headers=headers, timeout=10)
```
**Issue:** No limit on response size. Malicious images could cause memory exhaustion.

**Fix:** Add max content length:
```python
response = requests.get(image_url, headers=headers, timeout=10, stream=True)
max_size = 10 * 1024 * 1024  # 10MB
if int(response.headers.get('content-length', 0)) > max_size:
    raise ValueError("Image too large")
```

#### `lambda/lambda_function.py:18-21`
```python
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-west-2:533267235251:runtime/grow_light-2VJhSK5zPc',
    runtimeSessionId=session_id,
    payload=json.dumps(payload),
)
```
**Issue:** Hardcoded ARNs and resource IDs. If compromised, attacker knows exact target.

**Fix:** Use environment variables:
```python
agent_runtime_arn = os.environ['AGENT_RUNTIME_ARN']
```

### Medium Security Issues

#### `lambda/lambda_function.py:29-33`
```python
sqs = boto3.client('sqs', region_name='sa-east-1')
response = sqs.send_message(
    QueueUrl='https://sqs.sa-east-1.amazonaws.com/533267235251/grow-light-result',
```
**Issue:** Region mismatch - SQS client uses `sa-east-1` but Lambda runs in `us-west-2` (from bedrock call). Cross-region SQS calls add latency and potential failures.

**Fix:** Use consistent region or make region configurable.

#### `agent/src/app.py:15-26`
**Positive:** Input sanitization is present but incomplete. Should also validate:
- Maximum message length
- Maximum URL length
- Block data: URLs

#### `agent/src/agent.py:9-11`
```python
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
```
**Good practice:** Validates API key presence. However, error message exposes that API key is expected.

### Minor Security Issues

#### `lambda/test_sqs.py:11`
```python
# 注意：确保您的环境已配置好 AWS 凭证 (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
```
**Issue:** Comments remind about credential configuration, but these should come from IAM roles in Lambda, not hardcoded credentials.

#### Missing security headers in image requests
`agent/src/app.py:38-40` sets User-Agent but no security headers like `Accept`.

---

## 4. Code Quality Issues

### Code Duplication
- `boto3.client('sqs')` setup duplicated in `lambda_function.py` and `test_sqs.py`
- JSON serialization patterns repeated

### Missing Error Handling
- `agent/src/app.py:58-59` catches all exceptions but returns raw error messages
- `lambda/lambda_function.py:35-36` catches exceptions silently (prints only)

### Inconsistent Patterns
- Different session ID formats (UUID strings vs hardcoded in test)
- Mixed return formats (dict with "error" key vs direct result)

### Missing Tests
- No unit tests for Pydantic models in `scheme.py`
- No tests for URL validation logic
- No mock-based tests for external dependencies

---

## 5. Recommendations Summary

### High Priority
1. Fix `SESSION_ID` in lambda_function.py (per-request, not global)
2. Add event validation before accessing Records
3. Implement response size limits for image downloads
4. Move hardcoded ARNs to environment variables
5. Remove or refactor unused `model.py`

### Medium Priority
1. Use stable Gemini model IDs (not preview)
2. Fix region inconsistency in Lambda
3. Add input length validation
4. Implement proper error handling with structured responses
5. Add comprehensive unit tests

### Low Priority
1. Create shared config/utility module
2. Add logging instead of print statements
3. Document all environment variables
4. Add type hints throughout
5. Set up CI/CD pipeline with linting

---

## Files Reviewed
- `agent/src/app.py`
- `agent/src/agent.py`
- `agent/src/model.py`
- `agent/src/scheme.py`
- `lambda/lambda_function.py`
- `lambda/test_sqs.py`
- `agent/requirements.txt`
- `agent/test/test_agentcore.py`
- `agent/test/test_agent_local.py`
- `README.md`
- `agent/README.md`
