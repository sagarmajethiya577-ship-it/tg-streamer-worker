export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.split("/").filter(Boolean);
    const msgId = path[0];

    // --- CONFIG ---
    const BOT_TOKEN = "7963161552:AAGqld1rJiFs7BZJbiBofDUBcvwbvQ9aExc";

    if (path[0] === "d" && path[1]) {
      // 20MB se chhoti files ke liye yeh direct download link banayega
      const getFile = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getFile?file_id=${path[1]}`);
      const fileData = await getFile.json();
      
      if (fileData.ok) {
        return Response.redirect(`https://api.telegram.org/file/bot${BOT_TOKEN}/${fileData.result.file_path}`, 302);
      } else {
        // Agar file badi hai, toh Telegram Web View par bhej dega
        return Response.redirect(`https://t.me/public_channel_username/${path[1]}`, 302); 
      }
    }

    // Aapka wahi sundar UI
    return new Response(renderHTML(msgId || "No ID"), {
      headers: { "content-type": "text/html;charset=UTF-8" },
    });
  }
}

function renderHTML(id) {
  return `
    <html>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          body { font-family: sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
          .card { background: #1e293b; padding: 30px; border-radius: 15px; text-align: center; border: 1px solid #334155; width: 85%; }
          .btn { display: inline-block; background: #10b981; color: white; padding: 15px 25px; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 20px; }
        </style>
      </head>
      <body>
        <div class="card">
          <h2 style="color: #3b82f6;">File Ready!</h2>
          <p>Message ID: ${id}</p>
          <a href="/d/${id}" class="btn">🚀 START DIRECT DOWNLOAD</a>
        </div>
      </body>
    </html>`;
}
