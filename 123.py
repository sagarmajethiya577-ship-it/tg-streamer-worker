import os
from bs4 import BeautifulSoup

POSTS_DIR = "Posts"

all_posts_data = []

# 1. SCAN POSTS (Bina kuch delete kiye)
if os.path.exists(POSTS_DIR):
    for file in os.listdir(POSTS_DIR):
        if file.endswith(".html"):
            path = os.path.join(POSTS_DIR, file).replace("\\", "/")
            try:
                # File ki modification time nikalna sorting ke liye
                mtime = os.path.getmtime(path)
                
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    
                    # Header/Footer/Script pehle se hain toh unhe saaf karna (Overwrite logic)
                    for extra in soup(['header', 'footer', 'script']):
                        extra.decompose()
                    
                    img = soup.find("img")
                    img_src = img["src"] if img else ""
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else file.replace(".html", "")
                    
                    # Content nikalna (Container ke andar wala)
                    content = soup.find("div", class_="post-container")
                    if content:
                        clean_content = content.decode_contents()
                    else:
                        clean_content = soup.body.decode_contents() if soup.body else str(soup)

                    all_posts_data.append({
                        "path": path,
                        "title": title,
                        "image": img_src,
                        "content": clean_content,
                        "time": mtime
                    })
            except: continue

# 2. SORTING: Newest Post First (Naya post sabse upar)
all_posts_data.sort(key=lambda x: x['time'], reverse=True)

# 3. LAYOUT TEMPLATE
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

# 4. UPDATE POST FILES (Bina content kharab kiye)
for post in all_posts_data:
    formatted_post = f'<div class="post-container">{post["content"]}</div>'
    with open(post['path'], "w", encoding="utf-8") as f:
        f.write(get_layout(post['title'], formatted_post))

# 5. GENERATE INDEX.HTML (Hamesha Nayi Create Hogi)
cards_html = ""
for post in all_posts_data:
    cards_html += f'''
    <a class="post-card" href="{post['path']}">
        <img src="{post['image']}">
        <div class="post-info">
            <h2>{post['title']}</h2>
            <p class="price">₹9,995</p>
            <span class="view-btn">VIEW DETAILS</span>
        </div>
    </a>'''

home_content = f"""
    <div class="hero-slider">
        <div class="slide"><img src="https://i.ibb.co/WvtZpK45/1778433434933.png"></div>
	<div class="slide"><img src="https://i.ibb.co/WvtZpK45/1778433434933.png"></div>
    </div>
    <div class="section-header"><h3>Latest Collection</h3></div>
    <main class="home-container">
        {cards_html}
    </main>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(get_layout("Home", home_content, is_index=True))

print(f"✅ Total {len(all_posts_data)} posts processed. Newest ones are at the top!")
