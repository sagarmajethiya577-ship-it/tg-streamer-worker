import os
from bs4 import BeautifulSoup
import math
import json

POSTS_DIR = "Posts"
POSTS_PER_PAGE = 20

all_files = []
search_index = []

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

for root, dirs, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file).replace("\\", "/")
            all_files.append(path)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    img = soup.find("img")
                    img_src = img["src"] if img else ""
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else os.path.basename(path).replace(".html", "").replace("-", " ").title()
                    search_index.append({"t": title, "u": path, "i": img_src})
            except: continue

all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

for page in range(math.ceil(len(all_files) / POSTS_PER_PAGE) if all_files else 1):
    current_page = page + 1
    start, end = page * POSTS_PER_PAGE, (page + 1) * POSTS_PER_PAGE
    current_files = all_files[start:end]

    cards_html = ""
    for path in current_files:
        data = next((item for item in search_index if item["u"] == path), None)
        if data:
            cards_html += f'''
            <a class="post-card" href="{data["u"]}">
                <img src="{data["i"]}" alt="{data["t"]}">
                <div class="post-info">
                    <h2>{data["t"]}</h2>
                    <p class="price">₹9,995</p>
                    <span class="view-btn">VIEW DETAILS</span>
                </div>
            </a>'''

# ... (Baaki scanning logic same rahega jo pehle tha) ...

    # HTML Template Update
    html = f"""<!DOCTYPE html>
<html lang="hi" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSTIN - Premium Store</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="site-header">
        <a href="/" class="logo">OSTIN</a>
        <button id="themeToggle" class="theme-switch">🌙 Dark</button>
    </header>

    <div class="hero-slider">
        <div class="slide"><img src="https://images.unsplash.com/photo-1547996160-81dfa63595aa?q=80&w=1000"></div>
        <div class="slide"><img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000"></div>
    </div>

    <div class="section-header"><h3>Latest Collection</h3></div>
    <main class="home-container" id="postList">
        {cards_html}
    </main>

    <footer class="site-footer">
        <p>© 2026 OSTIN | All Rights Reserved</p>
    </footer>

    <script>
    // Theme Toggle Logic
    const toggleBtn = document.getElementById('themeToggle');
    const htmlTag = document.documentElement;

    toggleBtn.addEventListener('click', () => {{
        if (htmlTag.getAttribute('data-theme') === 'light') {{
            htmlTag.setAttribute('data-theme', 'dark');
            toggleBtn.innerHTML = "☀️ Light";
            localStorage.setItem('theme', 'dark');
        }} else {{
            htmlTag.setAttribute('data-theme', 'light');
            toggleBtn.innerHTML = "🌙 Dark";
            localStorage.setItem('theme', 'light');
        }}
    }});

    // Load Saved Theme
    if (localStorage.getItem('theme') === 'dark') {{
        htmlTag.setAttribute('data-theme', 'dark');
        toggleBtn.innerHTML = "☀️ Light";
    }}
    </script>
</body>
</html>"""
    
    # ... (File writing logic same rahega) ...

    filename = "index.html" if page == 0 else f"page{page+1}.html"
    with open(filename, "w", encoding="utf-8") as f: f.write(html)

print("✅ Site Updated! Brands and Search removed.")
