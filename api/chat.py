"""
Vercel Serverless Function - ChatGPT API Proxy
يحمي مفتاح API ويمرر الطلبات لـ OpenRouter
"""

import json
import os
import urllib.request
import urllib.error

def handler(request):
    """Handle POST requests to /api/chat"""
    
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }

    # Handle OPTIONS (CORS preflight)
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": headers,
            "body": json.dumps({"error": "Method not allowed"})
        }

    # Get API key from environment variable
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": "API key not configured"})
        }

    try:
        # Parse request body
        body = json.loads(request.body)
        model = body.get("model", "openai/gpt-4o")
        messages = body.get("messages", [])
        temperature = body.get("temperature", 0.7)
        max_tokens = body.get("max_tokens", 4096)

        # Build OpenRouter request
        payload = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }).encode('utf-8')

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://gpt-beta-eight.vercel.app",
                "X-Title": "ChatGPT Agent"
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=120) as response:
            response_data = response.read().decode('utf-8')

        return {
            "statusCode": 200,
            "headers": headers,
            "body": response_data
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            "statusCode": e.code,
            "headers": headers,
            "body": error_body
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
