export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.split("/").filter(Boolean);
    const msgId = path[0];
    const CHANNEL = "movies_zone_0044";

    if (path[0] === "d" && path[1]) {
      // Yeh header Chrome mein 'Save As' ka option trigger karega
      return new Response(null, {
        status: 302,
        headers: {
          "Location": `https://t.me/${CHANNEL}/${path[1]}?save=1`,
          "Content-Type": "application/octet-stream",
          "Content-Disposition": `attachment; filename="movie_${path[1]}.mkv"`
        }
      });
    }

    return new Response(`
      <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
            body { background: #0f172a; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 30px; border-radius: 20px; text-align: center; border: 1px solid #334155; }
            .btn { background: #10b981; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; }
          </style>
        </head>
        <body>
          <div class="card">
            <h2>Movies Zone 04</h2>
            <p>File Size: 782.5 MB</p>
            <a href="/d/${msgId}" class="btn">⬇️ DOWNLOAD IN CHROME</a>
          </div>
        </body>
      </html>`, { headers: { "Content-Type": "text/html" } });
  }
}
