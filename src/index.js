export default {
  async fetch(request, env) {
    const html = await fetch("https://raw.githubusercontent.com/your-username/your-repo/main/public/index.html").then(res => res.text());
    return new Response(html, { headers: { 'Content-Type': 'text/html' } });
  },
};
