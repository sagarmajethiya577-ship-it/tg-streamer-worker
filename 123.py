import os
from bs4 import BeautifulSoup

POSTS_DIR = "Posts"

# 1. SCAN AND CLEAN POSTS
all_posts_data = []
for file in os.listdir(POSTS_DIR):
    if file.endswith(".html"):
        path = os.path.join(POSTS_DIR, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                
                # Title aur Image nikaalna
                img_tag = soup.find("img")
                img_src = img_tag["src"] if img_tag else ""
                h1_tag = soup.find("h1")
                title = h1_tag.get_text(strip=True) if h1_tag else file.replace(".html", "")

                # Purane Buttons, Header aur Footer ko delete karna (Clean Up)
                for extra in soup(['header', 'footer', 'button', 'script', 'nav']):
                    extra.decompose()
                # Purane shop-buttons div ko bhi hatana agar hai toh
                for old_div in soup.find_all("div", class_=["shop-buttons", "post-container", "post-details"]):
                    old_div.unwrap()

                # Sirf description aur price ka text bachega
                content = str(soup.body.decode_contents()).strip() if soup.body else str(soup)

                all_posts_data.append({
                    "path": path,
                    "title": title,
                    "image": img_src,
                    "content": content
                })
        except: continue

# 2. MASTER LAYOUT (OSTIN Brand)
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

# 3. RE-GENERATE CLEAN POSTS
for post in all_posts_data:
    post_body = f"""
    <div class="post-container">
        <img src="{post['image']}" class="post-header-img">
        <div class="post-details">
            <h1>{post['title']}</h1>
            {post['content']}
            <div class="shop-buttons">
                <a href="#" class="btn-amazon">Buy on Amazon</a>
                <a href="#" class="btn-flipkart">Buy on Flipkart</a>
                <a href="#" class="btn-whatsapp">Order on WhatsApp</a>
            </div>
        </div>
    </div>"""
    with open(post['path'], "w", encoding="utf-8") as f:
        f.write(get_layout(post['title'], post_body))

# 4. RE-GENERATE HOME PAGE (index.html)
cards_html = "".join([f'''
    <a class="post-card" href="{p['path']}">
        <img src="{p['image']}">
        <div class="post-info"><h2>{p['title']}</h2><p class="price">₹9,995</p><span class="view-btn">VIEW DETAILS</span></div>
    </a>''' for p in all_posts_data])

home_body = f"""
    <div class="hero-slider"><div class="slide"><img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000"></div></div>
    <div class="section-header"><h3>Latest Collection</h3></div>
    <main class="home-container">{cards_html}</main>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(get_layout("Home", home_body, is_index=True))

print("✅ Sab fix ho gaya! Design clean hai.")
