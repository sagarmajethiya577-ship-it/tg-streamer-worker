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
with open("search_data.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f)

total_pages = math.ceil(len(all_files) / POSTS_PER_PAGE) if all_files else 1

for page in range(total_pages):
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
                    <div class="rating">★★★★☆</div>
                </div>
            </a>'''

    pagination = '<div class="pagination">'
    if current_page > 1:
        prev = "index.html" if current_page == 2 else f"page{current_page-1}.html"
        pagination += f'<a href="{prev}" class="page-btn">← Prev</a>'
    for i in range(1, total_pages + 1):
        active = "active" if i == current_page else ""
        link = "index.html" if i == 1 else f"page{i}.html"
        pagination += f'<a href="{link}" class="page-num {active}">{i}</a>'
    if current_page < total_pages:
        pagination += f'<a href="page{current_page+1}.html" class="page-btn">Next →</a>'
    pagination += "</div>"

    html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>समय - Premium Watch Store</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="site-header">
        <a href="/" class="logo">समय</a>
        <div class="nav-icons"><span>🔍</span> <span>👤</span> <span>🛒</span></div>
    </header>

    <div class="hero-banner">
        <div class="hero-content">
            <h1>समय का सही चयन</h1>
            <p>Discover curated timepieces for every occasion.</p>
            <button class="btn-explore">Explore Now</button>
        </div>
    </div>

    <div class="section-title">
        <h3>Spotlight on Brands</h3>
        <a href="#" class="see-all">See all ></a>
    </div>
    <div class="brand-logos">
        <div class="brand-item">TITAN</div>
        <div class="brand-item">SEIKO</div>
        <div class="brand-item">CASIO</div>
        <div class="brand-item">FAST RACK</div>
    </div>

    <div class="search-container">
        <input type="text" id="searchInput" placeholder="Search for watches, brands...">
    </div>

    <div class="section-title"><h3>Latest Collection</h3></div>
    <main class="home-container" id="postList">{cards_html}</main>
    {pagination}

    <footer class="site-footer">
        <p>© 2026 SAMAY | Premium Watches</p>
        <div class="payment-icons">VISA | MASTER | UPI | GPay</div>
    </footer>

    <script>
    let movieData = [];
    async function loadSearchData() {{ 
        const res = await fetch('search_data.json'); 
        movieData = await res.json(); 
    }}
    loadSearchData();
    const input = document.getElementById("searchInput"), postList = document.getElementById("postList"), original = postList.innerHTML;
    input.addEventListener("input", () => {{
        const val = input.value.toLowerCase().trim();
        if (val.length < 2) {{ postList.innerHTML = original; return; }}
        const res = movieData.filter(m => m.t.toLowerCase().includes(val));
        postList.innerHTML = res.length ? res.map(m => `<a class="post-card" href="${{m.u}}"><img src="${{m.i}}"><div class="post-info"><h2>${{m.t}}</h2><p class="price">₹9,995</p></div></a>`).join("") : "<p style='width:100%; text-align:center;'>No results</p>";
    }});
    </script>
</body>
</html>"""
    
    filename = "index.html" if page == 0 else f"page{page+1}.html"
    with open(filename, "w", encoding="utf-8") as f: f.write(html)

print("✅ Site generated with photo design!")
