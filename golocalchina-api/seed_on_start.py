"""Auto-seed demo data on startup if database is empty."""
import asyncio
import uuid
from app.core.database import create_tables, async_session, engine
from app.models.user import User, GuideProfile, TouristProfile
from app.models.listing import GuideListing
from app.core.security import hash_password
from sqlalchemy import select, func

GUIDES = [
    {
        "name": "Li Wei", "email": "liwei@demo.golocalchina.com",
        "bio": "Born and raised in Beijing. 15 years guiding foreign visitors through hutongs, temples, and hidden restaurants.",
        "languages": ["en", "zh"], "cities": ["Beijing"], "specialties": ["history", "food"],
        "rate": 800, "payment_note": "I accept Alipay, WeChat Pay, or USD/CNY cash.",
        "listings": [
            {"title": "Mock: Hidden Hutongs & Imperial Secrets — Half Day", "summary": "Explore hidden alleys of old Beijing that tourists never find. Drink tea in a 400-year-old courtyard home.", "desc": "We start at 8am at Nanluoguxiang. I take you through alleys that haven't changed in 600 years. We visit my favorite jianbing vendor, drink tea in a courtyard home, explore the Drum and Bell towers, and end with the best roast duck in Beijing.", "city": "Beijing", "price": 800, "unit": "per_half_day", "cover": "/images/Beijing.jpg"},
            {"title": "Mock: Great Wall at Sunrise — Full Day", "summary": "Skip the crowds. We leave at 5am for the Jinshanling section — the most photogenic stretch.", "desc": "I pick you up at 5am. We drive to Jinshanling, arriving before anyone else. Golden hour light on the wall with zero tourists. We hike 10km, I tell you the history of every watchtower. Lunch at a farmhouse.", "city": "Beijing", "price": 1500, "unit": "per_day", "cover": "/images/Beijing.jpg"},
        ]
    },
    {
        "name": "Zhang Mei", "email": "zhangmei@demo.golocalchina.com",
        "bio": "Shanghai native and professional photographer. I show you the city through a camera lens.",
        "languages": ["en", "zh", "ja"], "cities": ["Shanghai"], "specialties": ["art", "photography"],
        "rate": 1000, "payment_note": "Alipay or WeChat Pay preferred.",
        "listings": [
            {"title": "Mock: Shanghai Through the Lens — Full Day Photo Walk", "summary": "From Nanjing Road neon to French Concession quiet lanes. You leave with stunning photos.", "desc": "We start at the Bund at golden hour, walk through the old city, explore hidden art galleries in M50, and end in the French Concession at sunset. I teach you composition along the way.", "city": "Shanghai", "price": 1000, "unit": "per_day", "cover": "/images/Shanghai.jpg"},
        ]
    },
    {
        "name": "Wang Jun", "email": "wangjun@demo.golocalchina.com",
        "bio": "History professor turned guide. Terracotta Warriors specialist with 20 years of research.",
        "languages": ["en", "zh", "ko"], "cities": ["Xian"], "specialties": ["history", "nature"],
        "rate": 600, "payment_note": "Cash CNY or Alipay.",
        "listings": [
            {"title": "Mock: Terracotta Warriors — The Story They Won't Tell You", "summary": "I spent 20 years researching the warriors. I tell you who these soldiers were and the murder mystery behind the tomb.", "desc": "As a history professor, I show you all 3 pits and tell you the real stories — the assassination attempts, the mercury rivers, the curse of the tomb. We also visit the Muslim Quarter for lunch.", "city": "Xian", "price": 600, "unit": "per_half_day", "cover": "/images/Xian.jpg"},
        ]
    },
    {
        "name": "Chen Xiao", "email": "chenxiao@demo.golocalchina.com",
        "bio": "Sichuan food expert and panda enthusiast. Family-friendly tours with lots of spicy snacks!",
        "languages": ["en", "zh", "fr"], "cities": ["Chengdu"], "specialties": ["food", "nature"],
        "rate": 700, "payment_note": "Alipay, WeChat Pay, or cash.",
        "listings": [
            {"title": "Mock: Pandas, Hot Pot & Sichuan Spice — Full Day", "summary": "Morning with giant pandas, afternoon cooking mapo tofu with my grandmother, evening at the best hot pot in Chengdu.", "desc": "I pick you up at 7:30am for the Panda Research Base before the crowds. Afternoon: my grandmother teaches you to cook real Sichuan mapo tofu. Evening: the hot pot restaurant where locals go.", "city": "Chengdu", "price": 700, "unit": "per_day", "cover": "/images/Chengdu.jpg"},
        ]
    },
]



async def seed():
    """Seed demo data if DB is empty."""
    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(GuideListing))
        count = result.scalar() or 0
        if count > 0:
            print(f"[Seed] DB already has {count} listings, skipping seed.")
            return

        print("[Seed] Empty DB — seeding demo data...")
        
        # Seed guides and listings
        for g in GUIDES:
            uid = str(uuid.uuid4())
            user = User(id=uid, email=g["email"], password_hash=hash_password("Demo#2024!"), role="guide", status="active")
            session.add(user)
            await session.flush()

            profile = GuideProfile(
                user_id=uid, legal_name=g["name"], display_name=g["name"], bio=g["bio"],
                languages=g["languages"], service_cities=g["cities"], specialties=g["specialties"],
                default_rate_cny=g["rate"], payment_note=g["payment_note"], accepts_cash=True,
            )
            session.add(profile)

            for l in g["listings"]:
                listing = GuideListing(
                    guide_user_id=uid, title=l["title"], summary=l["summary"],
                    description_md=l["desc"], city=l["city"],
                    price_amount=l["price"], price_currency="CNY", price_unit=l["unit"],
                    cover_image_url=l["cover"], languages=g["languages"], status="published",
                )
                session.add(listing)

            await session.flush()
            print(f"  [Seed] {g['name']} + {len(g['listings'])} listings")

        
        await session.commit()
        print("[Seed] Done — seeded demo data.")


if __name__ == "__main__":
    asyncio.run(seed())
