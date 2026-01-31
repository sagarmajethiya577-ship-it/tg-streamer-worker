export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.split("/").filter(Boolean);

    // --- AAPKI DETAILS ---
    const config = {
      api_id: "34330516",
      api_hash: "9693b684498bf93a949bf50ba0573fc3",
      session: "BQIL15QApNzjWWOXBYh9H5zJq7CBxoqgLZfdl9-gMBxmO5U1eK7iTL9ld4e58eBXrGpOQJpC-vR9tNFyMvkoPqGXC90nQwsYqWEDpd18PPsEIBXXx4JJDGVTr-ldAAsl80mWtmJJU4VNwOAzghvk2kS_Ta8Etmb-OlLk_LohJOVheJ4FA0iFoD14YhM_6dsxJBDirilylWY17HocC3OBJwpItcyDI_rA9TBF3qvTMNR1XsXXgzFgc3Tw0Y_TcENE0qJKSOYFH63QqLzbQtLVK7PL_Qhf5TXAcKvVeqKixmnbEB6PHDgB0GiRbD85KQq2BHdP86u1WH02YJyQOpVLUxBdNiSMIQAAAAHLDq_FAA"
    };

    if (path[0] === "d" && path[1]) {
      // Direct Download Logic
      // Hum Telegram ke stream servers ko bypass karke direct link banayenge
      return Response.redirect(`https://t.me/c/me/${path[1]}`, 302);
    }

    // Sundar Theme (Dark Mode)
    return new Response(`
      <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; width: 90%; max-width: 400px; }
            .btn { display: inline-block; background: #10b981; color: white; padding: 15px 30px; border-radius: 12px; text-decoration: none; font-weight: bold; font-size: 18px; transition: 0.3s; margin-top: 20px; }
            .btn:hover { background: #059669; transform: translateY(-2px); }
            h2 { color: #3b82f6; margin-bottom: 10px; }
          </style>
        </head>
        <body>
          <div class="card">
            <h2>File Ready!</h2>
            <p style="color: #94a3b8;">Message ID: ${path[0] || 'Unknown'}</p>
            <a href="/d/${path[0]}" class="btn">🚀 FAST DOWNLOAD</a>
            <p style="font-size: 12px; margin-top: 25px; color: #64748b;">Powered by Cloudflare + GitHub</p>
          </div>
        </body>
      </html>
    `, { headers: { "content-type": "text/html" } });
  }
}
