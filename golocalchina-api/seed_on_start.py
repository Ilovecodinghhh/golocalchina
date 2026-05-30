"""Auto-seed demo data on startup if database is empty."""
import asyncio
import uuid
from app.core.database import create_tables, async_session, engine
from app.models.user import User, GuideProfile, TouristProfile
from app.models.listing import GuideListing
from app.models.post import TouristPost
from app.core.security import hash_password
from sqlalchemy import select, func

GUIDES = [
    {
        "name": "Li Wei", "email": "liwei@demo.golocalchina.com",
        "bio": "Born and raised in Beijing. 15 years guiding foreign visitors through hutongs, temples, and hidden restaurants.",
        "languages": ["en", "zh"], "cities": ["Beijing"], "specialties": ["history", "food"],
        "rate": 800, "payment_note": "I accept Alipay, WeChat Pay, or USD/CNY cash.",
        "listings": [
            {"title": "Hidden Hutongs & Imperial Secrets — Half Day", "summary": "Explore hidden alleys of old Beijing that tourists never find. Drink tea in a 400-year-old courtyard home.", "desc": "We start at 8am at Nanluoguxiang. I take you through alleys that haven't changed in 600 years. We visit my favorite jianbing vendor, drink tea in a courtyard home, explore the Drum and Bell towers, and end with the best roast duck in Beijing.", "city": "Beijing", "price": 800, "unit": "per_half_day", "cover": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=600&q=80"},
            {"title": "Great Wall at Sunrise — Full Day", "summary": "Skip the crowds. We leave at 5am for the Jinshanling section — the most photogenic stretch.", "desc": "I pick you up at 5am. We drive to Jinshanling, arriving before anyone else. Golden hour light on the wall with zero tourists. We hike 10km, I tell you the history of every watchtower. Lunch at a farmhouse.", "city": "Beijing", "price": 1500, "unit": "per_day", "cover": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=600&q=80"},
        ]
    },
    {
        "name": "Zhang Mei", "email": "zhangmei@demo.golocalchina.com",
        "bio": "Shanghai native and professional photographer. I show you the city through a camera lens.",
        "languages": ["en", "zh", "ja"], "cities": ["Shanghai"], "specialties": ["art", "photography"],
        "rate": 1000, "payment_note": "Alipay or WeChat Pay preferred.",
        "listings": [
            {"title": "Shanghai Through the Lens — Full Day Photo Walk", "summary": "From Nanjing Road neon to French Concession quiet lanes. You leave with stunning photos.", "desc": "We start at the Bund at golden hour, walk through the old city, explore hidden art galleries in M50, and end in the French Concession at sunset. I teach you composition along the way.", "city": "Shanghai", "price": 1000, "unit": "per_day", "cover": "https://images.unsplash.com/photo-1573455494060-c5595004fb6c?w=600&q=80"},
        ]
    },
    {
        "name": "Wang Jun", "email": "wangjun@demo.golocalchina.com",
        "bio": "History professor turned guide. Terracotta Warriors specialist with 20 years of research.",
        "languages": ["en", "zh", "ko"], "cities": ["Xian"], "specialties": ["history", "nature"],
        "rate": 600, "payment_note": "Cash CNY or Alipay.",
        "listings": [
            {"title": "Terracotta Warriors — The Story They Won't Tell You", "summary": "I spent 20 years researching the warriors. I tell you who these soldiers were and the murder mystery behind the tomb.", "desc": "As a history professor, I show you all 3 pits and tell you the real stories — the assassination attempts, the mercury rivers, the curse of the tomb. We also visit the Muslim Quarter for lunch.", "city": "Xian", "price": 600, "unit": "per_half_day", "cover": "https://images.unsplash.com/photo-1591017403286-fd8493524e1e?w=600&q=80"},
        ]
    },
    {
        "name": "Chen Xiao", "email": "chenxiao@demo.golocalchina.com",
        "bio": "Sichuan food expert and panda enthusiast. Family-friendly tours with lots of spicy snacks!",
        "languages": ["en", "zh", "fr"], "cities": ["Chengdu"], "specialties": ["food", "nature"],
        "rate": 700, "payment_note": "Alipay, WeChat Pay, or cash.",
        "listings": [
            {"title": "Pandas, Hot Pot & Sichuan Spice — Full Day", "summary": "Morning with giant pandas, afternoon cooking mapo tofu with my grandmother, evening at the best hot pot in Chengdu.", "desc": "I pick you up at 7:30am for the Panda Research Base before the crowds. Afternoon: my grandmother teaches you to cook real Sichuan mapo tofu. Evening: the hot pot restaurant where locals go.", "city": "Chengdu", "price": 700, "unit": "per_day", "cover": "https://images.unsplash.com/photo-1598887142487-3c854d51eabb?w=600&q=80"},
        ]
    },
]

MOCK_POSTS = [
    {
        "title": "Mock: Best Street Food in Beijing's Hutongs",
        "content": "Just spent 3 days exploring Beijing's hidden hutongs with Li Wei. The jianbing at dawn was incredible, and the tea ceremony in the 400-year-old courtyard was the highlight of my trip. Highly recommend the roast duck at the local spot he took us to — way better than the tourist restaurants!",
        "images": ["/images/Beijing.jpg"],
        "city": "Beijing",
    },
    {
        "title": "Mock: Shanghai Photography Tour — Worth Every Yuan",
        "content": "Zhang Mei's photography walk was amazing. She knows all the hidden spots in the French Concession and taught me composition techniques I never knew. The Bund at golden hour with her guidance resulted in the best photos I've ever taken. If you love photography, this is a must-do!",
        "images": ["/images/Shanghai.jpg"],
        "city": "Shanghai",
    },
    {
        "title": "Mock: Terracotta Warriors — History Comes Alive",
        "content": "Wang Jun's knowledge of the Terracotta Warriors is incredible. He spent 20 years researching them and it shows. The stories about assassination attempts and mercury rivers made the visit so much more engaging than just looking at statues. The Muslim Quarter lunch was also fantastic!",
        "images": ["/images/Xian.jpg"],
        "city": "Xian",
    },
    {
        "title": "Mock: Pandas and Hot Pot — Perfect Chengdu Day",
        "content": "Chen Xiao's full-day tour was the highlight of our China trip. Morning with the pandas before the crowds, afternoon cooking real mapo tofu with his grandmother (she's 82 and still amazing!), and evening at the best hot pot restaurant in Chengdu. Spicy but unforgettable!",
        "images": ["/images/Chengdu.jpg"],
        "city": "Chengdu",
    },
    {
        "title": "Mock: Guilin's Karst Mountains — Breathtaking Views",
        "content": "The Li River cruise through the karst mountains was absolutely stunning. Our guide knew all the best photo spots and told us fascinating stories about the local fishing communities. The rice terraces in the afternoon were equally impressive. Guilin should be on everyone's China itinerary!",
        "images": ["/images/Guilin.jpg"],
        "city": "Guilin",
    },
    {
        "title": "Mock: West Lake and Dragon Well Tea — Hangzhou's Charm",
        "content": "Hangzhou exceeded all expectations. The West Lake boat ride at sunset was magical, and the Dragon Well tea plantation visit was fascinating. Our guide showed us the traditional tea ceremony and we bought some amazing tea to bring home. The silk market was also worth a visit!",
        "images": ["/images/Hangzhou.jpg"],
        "city": "Hangzhou",
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

        # Create a demo tourist user for mock posts
        tourist_uid = str(uuid.uuid4())
        tourist_user = User(
            id=tourist_uid,
            email="tourist@demo.golocalchina.com",
            password_hash=hash_password("Demo#2024!"),
            role="tourist",
            status="active"
        )
        session.add(tourist_user)
        await session.flush()

        tourist_profile = TouristProfile(
            user_id=tourist_uid,
            display_name="Travel Explorer",
            nationality="US",
            preferred_currency="USD",
            preferred_languages=["en"],
        )
        session.add(tourist_profile)
        await session.flush()
        print(f"  [Seed] Demo tourist user created")

        # Seed mock posts
        for mp in MOCK_POSTS:
            post = TouristPost(
                author_user_id=tourist_uid,
                title=mp["title"],
                content=mp["content"],
                images=mp["images"],
                is_done=False,
                view_count=0,
                like_count=0,
            )
            session.add(post)
        
        await session.flush()
        print(f"  [Seed] {len(MOCK_POSTS)} mock posts created")

        await session.commit()
        print("[Seed] Done — seeded demo data.")


if __name__ == "__main__":
    asyncio.run(seed())
