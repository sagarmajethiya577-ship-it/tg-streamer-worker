import os
from bs4 import BeautifulSoup
import math
import json

POSTS_DIR = "Posts"
POSTS_PER_PAGE = 20

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

all_posts_data = []

# 1. SCAN ALL POSTS
for root, dirs, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    # Extract Data
                    img_tag = soup.find("img")
                    img_src = img_tag["src"] if img_tag else ""
                    h1_tag = soup.find("h1")
                    title = h1_tag.get_text(strip=True) if h1_tag else file.replace(".html", "")
                    
                    # Clean body for internal use
                    body_soup = soup.find("body") or soup
                    temp_soup = BeautifulSoup(str(body_soup), "html.parser")
                    for tag in temp_soup(['img', 'h1']):
                        tag.decompose()
                    
                    all_posts_data.append({
                        "path": path,
                        "title": title,
                        "image": img_src,
                        "content": str(temp_soup.decode_contents()).strip()
                    })
            except Exception as e:
                print(f"Error reading {file}: {e}")

# Newest posts first
all_posts_data.sort(key=lambda x: os.path.getmtime(x['path']), reverse=True)

# 2. SHARED TEMPLATE (OSTIN Brand)
def get_layout(title, body_content, is_index=False):
    css_path = "style.css" if is_index else "../style.css"
    return f"""<!DOCTYPE html>
<html lang="hi" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - OSTIN</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <header class="site-header">
        <a href="/" class="logo">OSTIN</a>
        <button id="themeToggle" class="theme-switch">🌙 Dark</button>
    </header>
    {body_content}
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

# 3. GENERATE POST PAGES (Amazon/Flipkart)
for post in all_posts_data:
    post_body = f"""
    <div class="post-container">
        <img src="{post['image']}" class="post-header-img">
        <div class="post-details">
            <h1>{post['title']}</h1>
            {post['content']}
        </div>
    </div>"""
    with open(post['path'], "w", encoding="utf-8") as f:
        f.write(get_layout(post['title'], post_body))

# 4. GENERATE HOME PAGE (index.html)
cards_html = ""
for post in all_posts_data:
    cards_html += f'''
    <a class="post-card" href="{post['path']}">
        <img src="{post['image']}" alt="{post['title']}">
        <div class="post-info">
            <h2>{post['title']}</h2>
            <p class="price">₹9,995</p>
            <span class="view-btn">VIEW DETAILS</span>
        </div>
    </a>'''

home_body = f"""
    <div class="hero-slider">
        <div class="slide"><img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000"></div>
    </div>
    <div class="section-header"><h3>Latest Collection</h3></div>
    <main class="home-container">
        {cards_html if cards_html else "<p style='grid-column: 1/-1; text-align:center;'>No posts found.</p>"}
    </main>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(get_layout("Home", home_body, is_index=True))

print("✅ OSTIN Main Page and Posts Updated Successfully!")
