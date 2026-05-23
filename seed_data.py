"""Seed the production database with demo guides and listings."""
import requests
import time

API = "https://golocalchina-production.up.railway.app/api/v1"

GUIDES = [
    {
        "name": "Li Wei", "email": "liwei.guide@golocalchina.com",
        "bio": "Born and raised in Beijing. 15 years guiding foreign visitors through hutongs, temples, and hidden restaurants.",
        "languages": ["en", "zh"], "cities": ["Beijing"], "specialties": ["history", "food"],
        "rate": 800, "payment_note": "I accept Alipay, WeChat Pay, or USD/CNY cash.",
        "listings": [
            {"title": "Hidden Hutongs & Imperial Secrets — Half Day", "summary": "Explore hidden alleys of old Beijing that tourists never find. Drink tea in a 400-year-old courtyard home.", "description": "We start at 8am at Nanluoguxiang. I take you through alleys that haven't changed in 600 years. We visit my favorite jianbing vendor, drink tea in a courtyard home, explore the Drum and Bell towers, and end with the best roast duck in Beijing.", "city": "Beijing", "price": 800, "unit": "per_half_day", "cover": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600&q=80"},
            {"title": "Great Wall at Sunrise — Full Day", "summary": "Skip the crowds. We leave at 5am for the Jinshanling section — the most photogenic stretch.", "description": "I pick you up at your hotel at 5am. We drive 2.5 hours to Jinshanling, arriving before anyone else. You get golden hour light on the wall with zero tourists. We hike 10km along the wall, I tell you the history of every watchtower. Lunch at a farmhouse. Back by 4pm.", "city": "Beijing", "price": 1500, "unit": "per_day", "cover": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=600&q=80"},
        ]
    },
    {
        "name": "Zhang Mei", "email": "zhangmei.guide@golocalchina.com",
        "bio": "Shanghai native and professional photographer. I show you the city through a camera lens.",
        "languages": ["en", "zh", "ja"], "cities": ["Shanghai"], "specialties": ["art", "photography"],
        "rate": 1000, "payment_note": "Alipay or WeChat Pay preferred.",
        "listings": [
            {"title": "Shanghai Through the Lens — Full Day Photo Walk", "summary": "From Nanjing Road neon to French Concession quiet lanes. You leave with stunning photos.", "description": "I am a professional photographer and Shanghai native. We start at the Bund at golden hour, walk through the old city, explore hidden art galleries in M50, and end in the French Concession at sunset. I teach you composition along the way. You leave with 200+ photos.", "city": "Shanghai", "price": 1000, "unit": "per_day", "cover": "https://images.unsplash.com/photo-1573455494060-c5595004fb6c?w=600&q=80"},
        ]
    },
    {
        "name": "Wang Jun", "email": "wangjun.guide@golocalchina.com",
        "bio": "History professor turned guide. Terracotta Warriors specialist with 20 years of research.",
        "languages": ["en", "zh", "ko"], "cities": ["Xian"], "specialties": ["history", "nature"],
        "rate": 600, "payment_note": "Cash CNY or Alipay.",
        "listings": [
            {"title": "Terracotta Warriors — The Story They Won't Tell You", "summary": "I spent 20 years researching the warriors. I tell you who these soldiers were and the murder mystery behind the tomb.", "description": "As a history professor at Xi'an Jiaotong University, I have spent 20 years studying the Qin dynasty. I show you all 3 pits, but more importantly, I tell you the stories — the assassination attempts, the mercury rivers, the curse of the tomb. We also visit the Muslim Quarter for lunch.", "city": "Xian", "price": 600, "unit": "per_half_day", "cover": "https://images.unsplash.com/photo-1591017403286-fd8493524e1e?w=600&q=80"},
        ]
    },
    {
        "name": "Chen Xiao", "email": "chenxiao.guide@golocalchina.com",
        "bio": "Sichuan food expert and panda enthusiast. Family-friendly tours with lots of spicy snacks!",
        "languages": ["en", "zh", "fr"], "cities": ["Chengdu"], "specialties": ["food", "nature"],
        "rate": 700, "payment_note": "Alipay, WeChat Pay, or cash.",
        "listings": [
            {"title": "Pandas, Hot Pot & Sichuan Spice — Full Day", "summary": "Morning with giant pandas, afternoon cooking mapo tofu with my grandmother, evening at the best hot pot in Chengdu.", "description": "I pick you up at 7:30am. We go to the Chengdu Research Base of Giant Panda Breeding before the crowds. I know the quiet paths where you can watch pandas eating bamboo in peace. Afternoon: my grandmother teaches you to cook real Sichuan mapo tofu. Evening: I take you to the hot pot restaurant where locals go — not the tourist one.", "city": "Chengdu", "price": 700, "unit": "per_day", "cover": "https://images.unsplash.com/photo-1598887142487-3c854d51eabb?w=600&q=80"},
        ]
    },
]

for guide in GUIDES:
    print(f"\n=== Seeding: {guide['name']} ===")
    
    # Send code
    r = requests.post(f"{API}/auth/send-code", json={"email": guide["email"]})
    if r.status_code == 409:
        print(f"  Already registered, skipping")
        continue
    if r.status_code != 200:
        print(f"  Send code failed: {r.status_code} {r.text[:100]}")
        continue
    code = r.json()["demo_code"]
    
    # Verify
    requests.post(f"{API}/auth/verify-code", json={"email": guide["email"], "code": code})
    
    # Register
    r = requests.post(f"{API}/auth/register", json={
        "email": guide["email"], "password": "Guide#2024!",
        "role": "guide", "display_name": guide["name"]
    })
    if r.status_code != 201:
        print(f"  Register failed: {r.status_code} {r.text[:100]}")
        continue
    uid = r.json()["user_id"]
    print(f"  Registered: {uid}")
    
    # Update profile
    requests.put(f"{API}/profile/me/guide?user_id={uid}", json={
        "display_name": guide["name"], "bio": guide["bio"],
        "languages": guide["languages"], "service_cities": guide["cities"],
        "specialties": guide["specialties"], "default_rate_cny": guide["rate"],
        "payment_note": guide["payment_note"], "accepts_cash": True,
    })
    print(f"  Profile updated")
    
    # Create listings
    for listing in guide["listings"]:
        r = requests.post(f"{API}/listings?guide_user_id={uid}", json={
            "title": listing["title"], "summary": listing["summary"],
            "description_md": listing["description"], "city": listing["city"],
            "price_amount": listing["price"], "price_currency": "CNY",
            "price_unit": listing["unit"], "cover_image_url": listing["cover"],
            "languages": guide["languages"],
        })
        if r.status_code == 201:
            print(f"  Listing created: {listing['title'][:40]}")
        else:
            print(f"  Listing failed: {r.status_code} {r.text[:100]}")

print("\n✅ Seeding complete!")

# Verify
r = requests.get(f"{API}/explore/listings")
data = r.json()
print(f"\nPublished listings in DB: {data['total']}")
for l in data.get("listings", []):
    print(f"  - {l['title']} by {l['guide']['display_name']} ({l['city']}, ¥{l['price_amount']})")
