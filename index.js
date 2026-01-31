export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.split("/").filter(Boolean);
    const msgId = path[0];

    // --- CONFIG ---
    // Aapka channel username aur bot details
    const CHANNEL_USERNAME = "movies_zone_0044"; 
    const BOT_TOKEN = "7963161552:AAGqld1rJiFs7BZJbiBofDUBcvwbvQ9aExc";

    // Agar URL /d/ID format mein hai toh direct redirect karein
    if (path[0] === "d" && path[1]) {
      // ?embed=1 lagane se Telegram Web ka preview mode open hota hai jo download trigger karne mein help karta hai
      return Response.redirect(`https://t.me/${CHANNEL_USERNAME}/${path[1]}?embed=1`, 302);
    }

    // Default UI Page
    return new Response(renderHTML(msgId || "No ID"), {
      headers: { "content-type": "text/html;charset=UTF-8" },
    });
  }
}

function renderHTML(id) {
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movies Zone Download</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; width: 90%; max-width: 400px; }
            h2 { color: #3b82f6; margin-bottom: 20px; }
            .btn { display: inline-block; background: #10b981; color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 18px; transition: 0.3s; margin-top: 20px; width: 100%; box-sizing: border-box; }
            .btn:hover { background: #059669; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4); }
            .info { color: #94a3b8; font-size: 14px; margin-top: 25px; border-top: 1px solid #334155; padding-top: 15px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>File Ready!</h2>
            <div style="background: #0f172a; padding: 12px; border-radius: 8px; font-family: monospace; border: 1px dashed #3b82f6; color: #3b82f6;">Message ID: ${id}</div>
            <a href="/d/${id}" class="btn">🚀 START DOWNLOAD</a>
            <div class="info">Movies Zone 04 • Fast Cloud Stream</div>
        </div>
    </body>
    </html>`;
}
