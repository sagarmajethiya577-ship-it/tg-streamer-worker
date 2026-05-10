import os
from bs4 import BeautifulSoup
import math
import json

POSTS_DIR = "Posts"
POSTS_PER_PAGE = 20

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

all_posts_data = []

# 1. SCAN POSTS
for root, dirs, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    img = soup.find("img")
                    img_src = img["src"] if img else ""
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else file.replace(".html", "")
                    
                    # Sirf body ka extra content lene ke liye (img aur h1 ko chhod kar)
                    for tag in soup(['img', 'h1']):
                        tag.decompose()
                    
                    all_posts_data.append({
                        "path": path,
                        "title": title,
                        "image": img_src,
                        "content": str(soup.body.decode_contents()) if soup.body else ""
                    })
            except: continue

# 2. POST TEMPLATE (With Amazon/Flipkart Support)
def get_template(title, body_content):
    return f"""<!DOCTYPE html>
<html lang="hi" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - OSTIN</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header class="site-header">
        <a href="/" class="logo">OSTIN</a>
        <button id="themeToggle" class="theme-switch">🌙 Dark</button>
    </header>
    <div class="post-container">
        {body_content}
    </div>
    <footer class="site-footer">
        <p>© 2026 OSTIN | Premium Store</p>
    </footer>
    <script>
        const toggleBtn = document.getElementById('themeToggle');
        const htmlTag = document.documentElement;
        toggleBtn.addEventListener('click', () => {{
            const theme = htmlTag.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
            htmlTag.setAttribute('data-theme', theme);
            toggleBtn.innerHTML = theme === 'dark' ? "☀️ Light" : "🌙 Dark";
            localStorage.setItem('theme', theme);
        }});
        if (localStorage.getItem('theme') === 'dark') {{
            htmlTag.setAttribute('data-theme', 'dark');
            toggleBtn.innerHTML = "☀️ Light";
        }}
    </script>
</body>
</html>"""

# 3. RE-WRITE POSTS
for post in all_posts_data:
    formatted_content = f"""
    <img src="{post['image']}" class="post-header-img">
    <div class="post-details">
        <h1>{post['title']}</h1>
        {post['content']}
    </div>
    """
    with open(post['path'], "w", encoding="utf-8") as f:
        f.write(get_template(post['title'], formatted_content))

# 4. INDEX PAGE GENERATION
# (Yahan bhi template mein 'OSTIN' update kar dein)
print("✅ OSTIN Brand update complete!")
