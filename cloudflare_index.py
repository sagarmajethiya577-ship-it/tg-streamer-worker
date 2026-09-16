import os
from bs4 import BeautifulSoup
import math
import json
import re
from collections import defaultdict

POSTS_DIR = "Posts"
PLUS_DIR = "18+" # Aapka alag se banaya hua 18+ folder
POSTS_PER_PAGE = 200

all_files = []
collections = defaultdict(list)

LANGUAGES = ["English", "Gujarati", "Marathi", "Punjabi", "Bengali", "Tamil", "Telugu", "Malayalam", "Bhojpuri", "French", "Spanish"]
GENRES = ["Action", "Comedy", "Horror", "Sci-Fi", "Romance", "Thriller", "Drama", "Fantasy", "Animation", "Crime", "Adventure", "Mystery"]
INDUSTRIES = ["Bollywood", "Hollywood"]

print("1. Scanning Posts and 18+ folders... Please wait.")

def scan_directory(directory, is_18plus_folder=False):
    if not os.path.exists(directory):
        return
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                try:
                    file_stat = os.stat(path)
                    original_atime = file_stat.st_atime
                    original_mtime = file_stat.st_mtime
                    
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        # Sirf title aur thoda data nikalenge taaki script fast chale
                        content = f.read()
                        soup = BeautifulSoup(content, "html.parser")
                        img = soup.find("img")
                        img_src = img["src"] if img else ""
                        h1 = soup.find("h1")
                        title = h1.get_text(strip=True) if h1 else os.path.basename(path).replace(".html", "").replace("-", " ").title()
                        
                        full_text = (title + " " + soup.get_text(separator=" ")).lower()
                        
                        movie_data = {"t": title, "u": "/" + path.replace("\\", "/"), "i": img_src}
                        all_files.append((path, movie_data, full_text, original_mtime, original_atime, title, is_18plus_folder))
                except: continue

# Scan dono folders ko karenge
scan_directory(POSTS_DIR, is_18plus_folder=False)
scan_directory(PLUS_DIR, is_18plus_folder=True)

# Sort by Original Modified Time (Newest first)
all_files.sort(key=lambda x: x[3], reverse=True)

# 🔥 SEARCH & HOME PAGE: Sirf Posts folder wali files aayengi (is_18plus_folder == False)
search_index = [x[1] for x in all_files if x[6] == False]

for path, movie_data, full_text, mtime, atime, title, is_18plus_folder in all_files:
    title_lower = title.lower()
    
    # 18+ CHECK: Agar wo 18+ folder se aayi hai, YA fir title mein [18+] likha hai
    if is_18plus_folder or "18+" in title_lower or "18 +" in title_lower or "[18+]" in title_lower:
        collections["18+ Content"].append(movie_data)
        
    # Agar ye file sirf 18+ folder ki hai, toh isko baaki kisi category mein nahi dalna hai!
    if is_18plus_folder:
        continue

    # NORMAL CATEGORIES (Sirf Posts folder wali files ke liye)
    years = re.findall(r'\b(20\d\d)\b', full_text)
    if years:
        for y in set(years):
            if 2000 <= int(y) <= 2026:
                collections[y].append(movie_data)
    
    for lang in LANGUAGES:
        if lang.lower() in full_text: collections[lang].append(movie_data)
            
    for genre in GENRES:
        if genre.lower() in full_text and genre != "18+ Content": 
            collections[genre].append(movie_data)
            
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

def generate_ui():
    genre_links = [f'<a href="/{slugify(g)}.html">{g}</a>' for g in GENRES if len(collections[g]) > 0]
    lang_links = [f'<a href="/{slugify(l)}.html">{l}</a>' for l in LANGUAGES if len(collections[l]) > 0]
    year_keys = sorted([k for k in collections.keys() if re.match(r'^20\d\d$', k)], reverse=True)
    year_links = [f'<a href="/{slugify(y)}.html">{y}</a>' for y in year_keys]

    sidebar_html = ""
    if genre_links: sidebar_html += f'\n<div class="accordion-header"><span>Category / Genre</span><span class="icon">+</span></div>\n<div class="accordion-body">\n' + '\n'.join(genre_links) + '\n</div>'
    if lang_links: sidebar_html += f'\n<div class="accordion-header"><span>Language</span><span class="icon">+</span></div>\n<div class="accordion-body">\n' + '\n'.join(lang_links) + '\n</div>'
    if year_links: sidebar_html += f'\n<div class="accordion-header"><span>Year</span><span class="icon">+</span></div>\n<div class="accordion-body">\n' + '\n'.join(year_links) + '\n</div>'

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

master_template = fr"""<!DOCTYPE html>
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
    <div class="home-container" id="searchResults" style="display:none; padding:0; margin:0; width:100%;"></div>
    <div id="originalContent" style="width:100%;">
        <!-- CONTENT_HTML -->
    </div>
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
const searchResults = document.getElementById("searchResults");
const originalContent = document.getElementById("originalContent");
const paginationWrapper = document.getElementById("paginationWrapper");

function performSearch() {{
    if(!originalContent) return;
    const val = input.value.toLowerCase().trim();
    if (val.length < 2) {{ 
        searchResults.style.display = "none";
        originalContent.style.display = "block";
        if (paginationWrapper) paginationWrapper.style.display = "flex";
        return; 
    }}
    const searchWords = val.split(/\\s+/); 
    const res = movieData.filter(m => {{
        const titleLower = m.t.toLowerCase();
        return searchWords.every(word => titleLower.includes(word));
    }});
    
    originalContent.style.display="none";
    if (paginationWrapper) paginationWrapper.style.display = "none";
    searchResults.style.display = "grid";
    
    if (res.length > 0) {{ 
        searchResults.innerHTML = res.map(m => `<a class="post-card" href="${{m.u}}"><img src="${{m.i}}"><h2>${{m.t}}</h2></a>`).join(""); 
    }} else {{ 
        searchResults.innerHTML = "<p style='color:white; text-align:center; width:100%; grid-column: 1 / -1; margin: 50px 0;'>No movies found!</p>"; 
    }}
}}
if(input) input.addEventListener("input", performSearch);
if(searchBtn) searchBtn.addEventListener("click", performSearch);
</script>
</html>"""

def build_home_pages(data_list):
    total_pages = math.ceil(len(data_list) / POSTS_PER_PAGE)
    for page in range(total_pages):
        current_page = page + 1
        start = page * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        current_data = data_list[start:end]

        cards_html = "".join([f'<a class="post-card" href="{m["u"]}"><img src="{m["i"]}"><h2>{m["t"]}</h2></a>' for m in current_data])
        wrapper_html = f'<div class="home-container" style="padding:0; margin:0;">{cards_html}</div>'

        pagination = '<div class="pagination" id="paginationWrapper">'
        if total_pages > 1:
            if current_page > 1:
                prev_link = "/" if current_page == 2 else f"/page{current_page-1}.html"
                pagination += f'<a href="{prev_link}" class="page-btn">← Previous</a>'
            
            for i in range(1, total_pages + 1):
                active_class = "active" if i == current_page else ""
                link = "/" if i == 1 else f"/page{i}.html"
                pagination += f'<a href="{link}" class="page-num {active_class}">{i}</a>'

            if current_page < total_pages:
                pagination += f'<a href="/page{current_page+1}.html" class="page-btn">Next →</a>'
        pagination += "</div>"

        final_html = master_template.replace("<!-- MAIN_CLASS -->", "home-container")
        final_html = final_html.replace("<!-- PAGE_TITLE -->", "")
        final_html = final_html.replace("<!-- CONTENT_HTML -->", wrapper_html)
        final_html = final_html.replace("<!-- PAGINATION -->", pagination)

        filename = "index.html" if current_page == 1 else f"page{current_page}.html"
        with open(filename, "w", encoding="utf-8") as f: f.write(final_html)

print("2. Generating Home Index Pages...")
build_home_pages(search_index)

def build_single_category_page(data_list, cat_name):
    cards_html = "".join([f'<a class="post-card" href="{m["u"]}"><img src="{m["i"]}"><h2>{m["t"]}</h2></a>' for m in data_list])
    wrapper_html = f'<div class="home-container" style="padding:0; margin:0;">{cards_html}</div>'

    page_title_html = f'<h2 style="text-align:center; color:#00ffd5; margin: 15px 0 20px; text-transform: uppercase; letter-spacing: 2px;">Category: {cat_name}</h2>'

    final_html = master_template.replace("<!-- MAIN_CLASS -->", "home-container")
    final_html = final_html.replace("<!-- PAGE_TITLE -->", page_title_html)
    final_html = final_html.replace("<!-- CONTENT_HTML -->", wrapper_html)
    final_html = final_html.replace("<!-- PAGINATION -->", "")

    filename = f"{slugify(cat_name)}.html"
    with open(filename, "w", encoding="utf-8") as f: f.write(final_html)

print("3. Generating Single Category Pages...")
for cat, items in collections.items():
    if len(items) > 0:
        build_single_category_page(items, str(cat))

print("4. Formatting Post pages and cleaning debug text... (Preserving original exact time!)")
for path, _, _, original_mtime, original_atime, title, _ in all_files:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 🔥 NUCLEAR CLEANING: File padhte hi sabse pehle wo ganda text mita denge
    bad_phrases = [
        "Yahan Search Results Dikhenge (Default Hidden)",
        "Yahan Original Post ya Grid Dikhega",
        "Yahan Search Results Dikhenge",
        "Yahan Original Post"
    ]
    for bad in bad_phrases:
        content = content.replace(bad, "")
        content = content.replace(f"<!-- {bad} -->", "")

    soup = BeautifulSoup(content, "html.parser")
    
    # Baaki bacha kachra (purana header footer) saaf karenge
    for tag in soup.select('.site-header, .top-bar, .sidebar, .sidebar-overlay, .site-footer, script, .back-btn'):
        tag.decompose()
        
    for a in soup.find_all('a'):
        if 'back' in a.get_text().lower() and len(a.get_text().strip()) < 15:
            a.decompose()
            
    post_container = soup.find(class_='post-container')
    if post_container:
        post_content = "".join([str(c) for c in post_container.contents])
    else:
        body = soup.find('body')
        post_content = "".join([str(c) for c in body.contents]) if body else str(soup)

    # Naya chamakta hua layout apply karenge
    post_html = master_template.replace("<!-- MAIN_CLASS -->", "post-container")
    post_html = post_html.replace("<!-- PAGE_TITLE -->", "")
    post_html = post_html.replace("<!-- CONTENT_HTML -->", post_content.strip())
    post_html = post_html.replace("<!-- PAGINATION -->", "")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(post_html)
        
    os.utime(path, (original_atime, original_mtime))

print("✅ Success! 18+ dual logic is working perfectly, and all post pages are 100% clean!")
