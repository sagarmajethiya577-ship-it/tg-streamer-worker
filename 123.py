import os
from bs4 import BeautifulSoup

POSTS_DIR = "Posts"

# 1. PEHLE PURANI HTML FILES DELETE KARNA (Clean Start)
if os.path.exists(POSTS_DIR):
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".html"):
            os.remove(os.path.join(POSTS_DIR, file))
    print("🗑️ Posts folder saaf ho gaya hai. Ab apni nayi HTML files yahan copy karein.")

# Rokne ke liye taaki aap files copy kar sakein, ya fir agar files hain toh aage badhega
all_posts_data = []

# 2. SCAN POSTS (Nayi files jo aapne copy ki hongi)
if os.path.exists(POSTS_DIR):
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".html"):
            path = os.path.join(POSTS_DIR, file).replace("\\", "/")
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    img = soup.find("img")
                    img_src = img["src"] if img else ""
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else file.replace(".html", "")
                    
                    # Sirf body ka content nikalna
                    body_content = soup.body.decode_contents() if soup.body else "No Content"
                    
                    all_posts_data.append({
                        "path": path,
                        "title": title,
                        "image": img_src,
                        "content": body_content
                    })
            except: continue

# 3. DEFINE LAYOUT (OSTIN Branding)
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

# 4. RE-WRITE POST FILES (No extra buttons added here)
for post in all_posts_data:
    formatted_post = f"""<div class="post-container">{post['content']}</div>"""
    with open(post['path'], "w", encoding="utf-8") as f:
        f.write(get_layout(post['title'], formatted_post))

# 5. GENERATE INDEX.HTML (Home Page)
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

home_content = f"""
    <div class="hero-slider">
        <div class="slide"><img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000"></div>
    </div>
    <div class="section-header"><h3>Latest Collection</h3></div>
    <main class="home-container">
        {cards_html if cards_html else "<p style='grid-column: 1/-1; text-align:center;'>Abhi koi post nahi hai. Files copy karke script dubara chalayein.</p>"}
    </main>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(get_layout("Home", home_content, is_index=True))

print("✅ Index file aur Posts update ho gaye hain!")
