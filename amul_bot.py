import sys
import requests

# ==========================================
# 1. TELEGRAM SECRETS
# ==========================================
TELEGRAM_TOKEN = "8419729283:AAGGhT3lHjP3iWLSHtw-XsOH8f0G0yVfGvI"
CHAT_ID = "5762787067"

# ==========================================
# 2. AMUL CONFIGURATION
# ==========================================
PINCODE = "110059"

PRODUCTS = {
    "Amul Whey (Pack of 30)": "https://shop.amul.com/en/product/amul-whey-protein-32-g-or-pack-of-30-sachets",
    "Amul Whey (Pack of 60)": "https://shop.amul.com/en/product/amul-whey-protein-32-g-or-pack-of-60-sachets"
}

# Remember to update this when you get a 403 error text!
COOKIE_STRING = "__cf_bm=9FSRQ2t8Jl5CDr.VhDLhZqerdJqy6hGfrtcvux92kDs-1780826059.0052977-1.0.1.1-vUJOQTND25BlJau4jc0L_pbaCah1TaB15i.xossnOHc8nmo_tb.e6.41qKIw_1qDxZLxuThfpetxpmO3iRfipFW4DI9oV3yRqWaczVcnkLgv.0wxky3EjofjYffrRuQm; _cfuvid=feGvVhQCF.f0PFQB2_6h_Gt1W2Ywnez5VmoMWDxks.I-1780826059.0052977-1.0.1.1-LIBLxZW6w2f8ZV3Z_vVHdJBGBzDpjkNW61QezYhdf_0; jsessionid=s%3AdqmWXMCfwIW1ee9H5EezlclZ.K4Xycaf4fxLYF24MSppTnChrlG2IkkiXFujfnu04tEs;"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Cookie": COOKIE_STRING
}

# ==========================================
# 3. BOT LOGIC
# ==========================================
def send_telegram_error(message):
    """Sends an ERROR alert to your Telegram."""
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"⚠️ BOT BLOCKED ⚠️\n\n{message}"
    }
    requests.post(api_url, data=payload)

def send_telegram_alert(name, url):
    """Sends the SUCCESS alert to your Telegram."""
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🚨 AMUL WHEY IN STOCK! 🚨\n\nPincode: {PINCODE}\nProduct: {name}\nLink: {url}"
    }
    requests.post(api_url, data=payload)

def check_amul_stock(name, url):
    """Scrapes the Amul product page to check for stock."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        
        # --- THE NEW 403 TRIGGER ---
        if response.status_code == 403:
            error_msg = "Cloudflare gave a 403 Forbidden error.\n\nYour __cf_bm cookie has expired. Please open Firefox, get a new cookie string, and update the script!"
            print(error_msg)
            send_telegram_error(error_msg)
            # This 'sys.exit()' kills the script immediately so it doesn't keep checking products and spamming you
            sys.exit() 
            
        if response.status_code != 200:
            print(f"Failed to load {name}. Status Code: {response.status_code}")
            return False

        html_content = response.text.lower()
        
        if "add to cart" in html_content and "sold out" not in html_content:
            return True
            
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"Network error while checking {name}: {e}")
        return False

def main():
    print("Checking Amul Stock...")
    for name, url in PRODUCTS.items():
        if check_amul_stock(name, url):
            print(f"✅ SUCCESS: {name} is IN STOCK! Sending alert...")
            send_telegram_alert(name, url)
        else:
            print(f"❌ {name} is Sold Out.")

if __name__ == "__main__":
    main()
