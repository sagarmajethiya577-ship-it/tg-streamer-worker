import os
import re

POSTS_DIR = "Posts"

# Isme humne Google Analytics aur Naye EffectiveCPM Ad Code ko ek saath jod diya hai
TOTAL_INJECT_CODE = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XRNB9X1DJ2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XRNB9X1DJ2');
</script>

<script src="https://bleatbehind.com/77/19/55/7719558a2ddf75875325865ff105e8f4.js"></script>
"""

def clean_and_inject_all():
    processed_count = 0
    print(f"🧹 Clearing everything and injecting Analytics + Combo Ads in: {POSTS_DIR}...")

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                try:
                    # 1. Purana time (mtime) save karo
                    stat = os.stat(path)
                    original_times = (stat.st_atime, stat.st_mtime)

                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # 2. Saare purane script tags (chahe ad ho ya analytics) sab ko saaf karo
                    cleaned_content = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', '', content)
                    
                    # Extra safety: Google tag ke bache-khuche comments ko bhi clear karne ke liye
                    cleaned_content = cleaned_content.replace("", "")

                    # 3. Fresh inject karo </body> ke upar (Dono cheezein ek saath chali jayengi)
                    if "</body>" in cleaned_content:
                        new_content = cleaned_content.replace("</body>", f"{TOTAL_INJECT_CODE}\n</body>")
                        
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)

                        # 4. Wahi purana time wapas set karo
                        os.utime(path, original_times)
                        processed_count += 1

                except Exception as e:
                    print(f"❌ Error in {file}: {e}")

    print("-" * 30)
    print(f"✨ Perfect! Total {processed_count} files cleaned & updated with Ads + Analytics.")
    print("-" * 30)

if __name__ == "__main__":
    clean_and_inject_all()
