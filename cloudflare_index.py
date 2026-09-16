import os
from bs4 import BeautifulSoup
import math
import json
import re
from collections import defaultdict

POSTS_DIR = "Posts"
POSTS_PER_PAGE = 200

all_files = []
collections = defaultdict(list)

LANGUAGES = ["Hindi", "English", "Gujarati", "Marathi", "Punjabi", "Bengali", "Tamil", "Telugu", "Malayalam", "Bhojpuri", "French", "Spanish"]
GENRES = ["Action", "Comedy", "Horror", "Sci-Fi", "Romance", "Thriller", "Drama", "Fantasy", "Animation", "Crime", "Adventure", "Mystery", "18+ Content"]
INDUSTRIES = ["Bollywood", "Hollywood"]

print("1. Scanning files and extracting data... Please wait.")

for root, dirs, files in os.walk(POSTS_DIR):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    soup = BeautifulSoup(f, "html.parser")
                    img = soup.find("img")
                    img_src = img["src"] if img else ""
                    h1 = soup.find("h1")
                    title = h1.get_text(strip=True) if h1 else os.path.basename(path).replace(".html", "").replace("-", " ").title()
                    
                    full_text = (title + " " + soup.get_text(separator=" ")).lower()
                    mtime = os.path.getmtime(path)
                    
                    # Absolute URL for posts so search works from everywhere
                    movie_data = {"t": title, "u": "/" + path.replace("\\", "/"), "i": img_src}
                    all_files.append((path, movie_data, full_text, mtime))
            except: continue

all_files.sort(key=lambda x: x[3], reverse=True)
search_index = [x[1] for x in all_files]

for path, movie_data, full_text, mtime in all_files:
    years = re.findall(r'\b(19\d\d|20\d\d)\b', full_text)
    if years:
        for y in set(years): collections[y].append(movie_data)
    
    for lang in LANGUAGES:
        if lang.lower() in full_text: collections[lang].append(movie_data)
            
    for genre in GENRES:
        if genre.lower() in full_text: collections[genre].append(movie_data)
            
    if bool(re.search(r'\b(s\d\d?|season|episode|web series)\b', full_text)):
        collections["Web Series"].append(movie_data)
    else:
        collections["Movies"].append(movie_data)
        
    for ind in INDUSTRIES:
        if ind.lower() in full_text: collections[ind].append(movie_data)
    
    if "south" in full_text and ("hindi" in full_text or "dubbed" in full_text):
        collections["South Hindi Dubbed"].append(movie_data)

with open("search_data.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f)

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

# 2. Generate UI (Removed Counts from Links)
def generate_ui():
    # Only names, no length counts like (11)
    genre_links = [f'<a href="/{slugify(g)}.html">{g}</a>' for g in GENRES if len(collections[g]) > 0]
    lang_links = [f'<a href="/{slugify(l)}.html">{l}</a>' for l in LANGUAGES if len(collections[l]) > 0]
    year_keys = sorted([k for k in collections.keys() if re.match(r'^(19|20)\d\d$', k)], reverse=True)
    year_links = [f'<a href="/{slugify(y)}.html">{y}</a>' for y in year_keys]

    sidebar_html = ""
    if genre_links:
        sidebar_html += f'\n<div class="accordion-header"><span>Category / Genre</span><span class="icon">+</span></div>\n<div class="accordion-body">\n' + '\n'.join(genre_links) + '\n</div>'
    if lang_links:
        sidebar_html += f'\n<div class="accordion-header"><span>Language</span><span class="icon">+</span></div>\n<div class="accordion-body">\n' + '\n'.join(lang_links) + '\n</div>'
    if year_links:
        sidebar_html += f'\n<div class="accordion-header"><span>Year</span><span class="icon">+</span></div>\n<div class="accordion-body">\n' + '\n'.join(year_links) + '\n</div>'

    quick_cats = ["18+ Content", "Bollywood", "Hollywood", "South Hindi Dubbed", "Web Series", "Gujarati", "Marathi", "Bengali", "Punjabi"]
    
    buttons_html = f"""
        <a href="https://t.me/moviesrequest044" target="_blank" class="tg-btn">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.96 1.25-5.54 3.67-.52.36-.99.53-1.41.52-.46-.01-1.35-.26-2.01-.48-.81-.27-1.46-.42-1.4-.88.03-.24.36-.48.98-.74 3.84-1.67 6.4-2.77 7.68-3.3 3.63-1.5 4.38-1.76 4.87-1.77.11 0 .35.03.48.14.11.09.14.22.15.31.02.13.01.24 0 .34z"/></svg>
            Join Telegram
        </a>"""
    
    for cat in quick_cats:
        if len(collections[cat]) > 0:
            buttons_html += f'\n        <a href="/{slugify(cat)}.html" class="cat-btn">{cat}</a>'
            
    return sidebar_html, buttons_html

sidebar_html, buttons_html = generate_ui()

# 3. Master HTML Template (Works for Home, Categories AND Posts)
master_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<script src="https://bleatbehind.com/77/19/55/7719558a2ddf75875325865ff105e8f4.js"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XRNB9X1DJ2"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-XRNB9X1DJ2');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Movies Zone</title>
<link rel="stylesheet" href="/style.css">
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
        {sidebar_html}
    </div>
</div>

<div class="top-bar">
    <button class="menu-btn" id="openSidebar">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
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
            {buttons_html}
        </div>
    </div>
</header>

<main class="<!-- MAIN_CLASS -->" style="display:block;">
    <!-- PAGE_TITLE -->
    <!-- CONTENT_HTML -->
</main>
<!-- PAGINATION -->
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

const accHeaders = document.querySelectorAll('.accordion-header');
accHeaders.forEach(header => {{
    header.addEventListener('click', function() {{
        this.classList.toggle('active');
        const body = this.nextElementSibling;
        if (body.style.maxHeight) {{ body.style.maxHeight = null; }} 
        else {{ body.style.maxHeight = body.scrollHeight + "px"; }}
    }});
}});

let movieData = [];
async function loadSearchData() {{ 
    try {{ const res = await fetch('/search_data.json'); movieData = await res.json(); }} 
    catch(e) {{ console.error("Error loading search data", e); }}
}}
loadSearchData();

const input = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const postList = document.getElementById("postList");
const originalContent = postList ? postList.innerHTML : "";

function performSearch() {{
    if(!postList) return; // Prevent search errors inside a post page
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
if(input) input.addEventListener("input", performSearch);
if(searchBtn) searchBtn.addEventListener("click", performSearch);
</script>
</body></html>"""

# 4. Generate Home & Category Pages
def build_pages(data_list, base_slug):
    total_pages = math.ceil(len(data_list) / POSTS_PER_PAGE)
    if total_pages == 0: return
    
    for page in range(total_pages):
        current_page = page + 1
        start = page * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        current_data = data_list[start:end]

        cards_html = "".join([f'<a class="post-card" href="{m["u"]}"><img src="{m["i"]}"><h2>{m["t"]}</h2></a>' for m in current_data])
        wrapper_html = f'<div class="home-container" id="postList" style="padding:0; margin:0;">{cards_html}</div>'

        pagination = '<div class="pagination">'
        def get_link(p):
            if base_slug == "index": return "/" if p == 1 else f"/page{p}.html"
            else: return f"/{base_slug}.html" if p == 1 else f"/{base_slug}-page{p}.html"

        if total_pages > 1:
            if current_page > 1: pagination += f'<a href="{get_link(current_page-1)}" class="page-btn">← Previous</a>'
            visible_pages = []
            if total_pages <= 5: visible_pages = range(1, total_pages + 1)
            else:
                if current_page <= 3: visible_pages = [1, 2, 3, 4, "...", total_pages]
                elif current_page >= total_pages - 2: visible_pages = [1, "...", total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
                else: visible_pages = [1, "...", current_page - 1, current_page, current_page + 1, "...", total_pages]

            for i in visible_pages:
                if i == "...": pagination += '<span class="dots">...</span>'
                else:
                    active_class = "active" if i == current_page else ""
                    pagination += f'<a href="{get_link(i)}" class="page-num {active_class}">{i}</a>'

            if current_page < total_pages: pagination += f'<a href="{get_link(current_page+1)}" class="page-btn">Next →</a>'
        pagination += "</div>"

        page_title_html = ""
        if base_slug != "index":
            display_title = base_slug.replace("-", " ").title()
            page_title_html = f'<h2 style="text-align:center; color:#00ffd5; margin: 15px 0 20px; text-transform: uppercase; letter-spacing: 2px;">Category: {display_title}</h2>'

        final_html = master_template.replace("<!-- MAIN_CLASS -->", "home-container")
        final_html = final_html.replace("<!-- PAGE_TITLE -->", page_title_html)
        final_html = final_html.replace("<!-- CONTENT_HTML -->", wrapper_html)
        final_html = final_html.replace("<!-- PAGINATION -->", pagination)

        filename = get_link(current_page).lstrip("/")
        if filename == "": filename = "index.html"
        with open(filename, "w", encoding="utf-8") as f: f.write(final_html)

print("2. Generating Home and Category Index Pages...")
build_pages(search_index, "index")
for cat, items in collections.items():
    if len(items) > 0: build_pages(items, slugify(str(cat)))

# 5. WRAPPING POSTS (Replaces old scripts!)
print("3. Formatting internal Post pages with the new UI Layout...")
for path, _, _, _ in all_files:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    soup = BeautifulSoup(content, "html.parser")
    
    # 5.1 Remove old existing headers, sidebars, footers, scripts (Clean Slate)
    for tag in soup.select('.site-header, .top-bar, .sidebar, .sidebar-overlay, .site-footer, script'):
        tag.decompose()
        
    # 5.2 REMOVE OLD BACK BUTTON ("<- Back")
    for a in soup.find_all('a'):
        if 'back' in a.get_text().lower() and len(a.get_text().strip()) < 15:
            a.decompose()
            
    # 5.3 Extract clean core post content
    post_container = soup.find(class_='post-container')
    if post_container:
        post_content = "".join([str(c) for c in post_container.contents])
    else:
        body = soup.find('body')
        post_content = "".join([str(c) for c in body.contents]) if body else str(soup)

    # 5.4 Inject core post content into Master Template
    post_html = master_template.replace("<!-- MAIN_CLASS -->", "post-container")
    post_html = post_html.replace("<!-- PAGE_TITLE -->", "")
    post_html = post_html.replace("<!-- CONTENT_HTML -->", post_content)
    post_html = post_html.replace("<!-- PAGINATION -->", "")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(post_html)

print("✅ Success! Site is fully Professional. Posts are wrapped and counts are removed.")
