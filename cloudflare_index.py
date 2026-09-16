import os
from bs4 import BeautifulSoup
import math
import json

POSTS_DIR = "Posts"
POSTS_PER_PAGE = 200

all_files = []
search_index = []

# 1. Scan and Index
for root, dirs, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            all_files.append(path)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    img = soup.find("img")
                    img_src = img["src"] if img else ""
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else os.path.basename(path).replace(".html", "").replace("-", " ").title()
                    search_index.append({"t": title, "u": path.replace("\\", "/"), "i": img_src})
            except: continue

all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
with open("search_data.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f)

total_pages = math.ceil(len(all_files) / POSTS_PER_PAGE)

for page in range(total_pages):
    current_page = page + 1
    start, end = page * POSTS_PER_PAGE, (page + 1) * POSTS_PER_PAGE
    current_files = all_files[start:end]

    cards_html = ""
    for path in current_files:
        movie_data = next((item for item in search_index if item["u"] == path.replace("\\", "/")), None)
        if movie_data:
            cards_html += f'<a class="post-card" href="{movie_data["u"]}"><img src="{movie_data["i"]}"><h2>{movie_data["t"]}</h2></a>'

    pagination = '<div class="pagination">'
    if current_page > 1:
        prev_link = "index.html" if current_page == 2 else f"page{current_page-1}.html"
        pagination += f'<a href="{prev_link}" class="page-btn">← Previous</a>'

    visible_pages = []
    if total_pages <= 5:
        visible_pages = range(1, total_pages + 1)
    else:
        if current_page <= 3:
            visible_pages = [1, 2, 3, 4, "...", total_pages]
        elif current_page >= total_pages - 2:
            visible_pages = [1, "...", total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
        else:
            visible_pages = [1, "...", current_page - 1, current_page, current_page + 1, "...", total_pages]

    for i in visible_pages:
        if i == "...":
            pagination += '<span class="dots">...</span>'
        else:
            active_class = "active" if i == current_page else ""
            link = "index.html" if i == 1 else f"page{i}.html"
            pagination += f'<a href="{link}" class="page-num {active_class}">{i}</a>'

    if current_page < total_pages:
        pagination += f'<a href="page{current_page+1}.html" class="page-btn">Next →</a>'
    pagination += "</div>"

    html = fr"""<!DOCTYPE html>
<html lang="en">
<head>
<script src="https://bleatbehind.com/77/19/55/7719558a2ddf75875325865ff105e8f4.js"></script>

<script async src="https://www.googletagmanager.com/gtag/js?id=G-XRNB9X1DJ2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-XRNB9X1DJ2');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Movies Zone</title>
<link rel="stylesheet" href="style.css">
<style>
    .pagination {{ display: flex; justify-content: center; align-items: center; gap: 5px; margin: 30px 10px; flex-wrap: wrap; }}
    .page-btn, .page-num {{ padding: 8px 12px; border: 1px solid #00ff88; color: #00ff88; text-decoration: none; border-radius: 4px; font-size: 14px; min-width: 35px; text-align: center; }}
    .page-num.active {{ background: #00ff88; color: #000; font-weight: bold; border-color: #00ff88; }}
    .dots {{ color: #00ff88; padding: 0 5px; }}
    .page-btn:hover, .page-num:hover:not(.active) {{ background: rgba(0, 255, 136, 0.1); }}
    @media (max-width: 600px) {{ .page-btn {{ font-size: 12px; padding: 6px 10px; }} }}
</style>
</head>
<body>

<div class="sidebar-overlay" id="sidebarOverlay"></div>

<div class="sidebar" id="sidebar">
    <button class="close-btn" id="closeSidebar">&times;</button>
    <div class="sidebar-content">
        
        <div class="menu-section">
            <h3>Category / Genre</h3>
            <a href="#">Action</a>
            <a href="#">Comedy</a>
            <a href="#">Horror</a>
            <a href="#">Sci-Fi</a>
            <a href="#">Romance</a>
            <a href="#">Thriller</a>
            <a href="#">18+ Content</a>
        </div>

        <div class="menu-section">
            <h3>Year</h3>
            <a href="#">2026</a>
            <a href="#">2025</a>
            <a href="#">2024</a>
            <a href="#">2023</a>
        </div>

    </div>
</div>

<div class="top-bar">
    <button class="menu-btn" id="openSidebar">
        <!-- SVG Hamburger Icon -->
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
        </svg>
        MENU
    </button>
</div>

<header class="site-header">
    <div class="header-content">
        <a href="/" class="site-title">Movies Zone</a>
        <div class="search-wrapper">
            <input type="text" id="searchInput" placeholder="Search Movies or WEB-Series here">
            <button id="searchBtn">SEARCH</button>
        </div>
        
        <div class="category-container">
            <button class="cat-btn">18+ Content</button>
            
            <!-- NEW TELEGRAM BUTTON (Link is here) -->
            <a href="https://t.me/moviesrequest044" target="_blank" class="tg-btn">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.96 1.25-5.54 3.67-.52.36-.99.53-1.41.52-.46-.01-1.35-.26-2.01-.48-.81-.27-1.46-.42-1.4-.88.03-.24.36-.48.98-.74 3.84-1.67 6.4-2.77 7.68-3.3 3.63-1.5 4.38-1.76 4.87-1.77.11 0 .35.03.48.14.11.09.14.22.15.31.02.13.01.24 0 .34z"/>
                </svg>
                Join Telegram
            </a>

            <button class="cat-btn">Bollywood</button>
            <button class="cat-btn">Hollywood</button>
            <button class="cat-btn">South Hindi Dubbed</button>
            <button class="cat-btn">Web Series</button>
            <button class="cat-btn">Gujarati</button>
            <button class="cat-btn">Marathi</button>
        </div>
        
    </div>
</header>

<main class="home-container" id="postList">{cards_html}</main>
{pagination}
<footer class="site-footer">© 2026 Movies Zone | All Rights Reserved</footer>

<script>
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebarOverlay');
const openBtn = document.getElementById('openSidebar');
const closeBtn = document.getElementById('closeSidebar');

function openMenu() {{ sidebar.classList.add('active'); overlay.classList.add('active'); }}
function closeMenu() {{ sidebar.classList.remove('active'); overlay.classList.remove('active'); }}

openBtn.addEventListener('click', openMenu);
closeBtn.addEventListener('click', closeMenu);
overlay.addEventListener('click', closeMenu);

let movieData = [];
async function loadSearchData() {{ 
    try {{ const res = await fetch('search_data.json'); movieData = await res.json(); }} 
    catch(e) {{ console.error("Error loading search data", e); }}
}}
loadSearchData();

const input = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const postList = document.getElementById("postList");
const originalContent = postList.innerHTML;

function performSearch() {{
    const val = input.value.toLowerCase().trim();
    if (val.length < 2) {{ postList.innerHTML = originalContent; return; }}
    
    const searchWords = val.split(/\s+/); 
    const res = movieData.filter(m => {{
        const titleLower = m.t.toLowerCase();
        return searchWords.every(word => titleLower.includes(word));
    }});
    
    if (res.length > 0) {{ 
        postList.innerHTML = res.map(m => `<a class="post-card" href="${{m.u}}"><img src="${{m.i}}"><h2>${{m.t}}</h2></a>`).join(""); 
    }} else {{ 
        postList.innerHTML = "<p style='color:white; text-align:center; width:100%; margin: 50px 0;'>No movies found!</p>"; 
    }}
}}
input.addEventListener("input", performSearch);
searchBtn.addEventListener("click", performSearch);
</script>
</body></html>"""
    
    filename = "index.html" if page == 0 else f"page{page+1}.html"
    with open(filename, "w", encoding="utf-8") as f: f.write(html)

print("✅ UI fixed! Clean Menu, sleek Sidebar, and solid Telegram button applied.")
