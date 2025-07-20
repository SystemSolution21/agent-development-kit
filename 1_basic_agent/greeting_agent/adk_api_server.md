# ADK API Server

The ADK API server provides a RESTful interface to interact with the agents. It's useful for testing and integrating the agents into other applications.

## Running the API Server

To run the API server, use the `adk api_server` command from the parent directory of the agent:

```pwsh
adk api_server
```

This will start the server on `http://localhost:8000`.

## Testing the API Server

To test the API server using `curl` or any other HTTP client. Here's an example of how to send a request to the API server:

**Create a new session:**

```pwsh
curl -X POST http://localhost:8000/apps/greeting_agent/users/u_123/sessions/s_123 -H "Content-Type: application/json" -d '{}'
```

**Send a message to the agent using the /run endpoint:**

```pwsh
curl -X POST http://localhost:8000/run 
-H "Content-Type: application/json" 
-d '{
"appName": "greeting_agent",
"userId": "u_123",
"sessionId": "s_123",
"newMessage": {
    "role": "user",
    "parts": [{
    "text": "Hey! whats up?"
    }]
}
}'
```

The response will be a JSON object containing the agent's response.

[{"content":{"parts":[{"text":"Hello there! Before we get started, what's your name?\n"}],"role":"model"},"usageMetadata":{"candidatesTokenCount":15,"candidatesTokensDetails":[{"modality":"TEXT","tokenCount":15}],"promptTokenCount":65,"promptTokensDetails":[{"modality":"TEXT","tokenCount":65}],"totalTokenCount":80},"invocationId":"e-e5145941-8f2e-400d-9645-6804d842a089","author":"greeting_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"id":"3RTt1ZYw","timestamp":1752990624.663998}]
