"""
Seed script to populate MongoDB with comprehensive mock data
Includes 5 athletes, 2 coaches, posts, training videos, and opportunities
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import get_settings
import hashlib

settings = get_settings()

# Login credentials for all users
# Password for all users: "password123" (hashed below)
def hash_password(password: str) -> str:
    """Simple hash for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

# Mock login credentials
MOCK_CREDENTIALS = {
    "athlete1": {"username": "pvsindhu", "password": hash_password("password123"), "email": "pv.sindhu@podium.com"},
    "athlete2": {"username": "kmomota", "password": hash_password("password123"), "email": "k.momota@podium.com"},
    "athlete3": {"username": "cseyoung", "password": hash_password("password123"), "email": "an.seyoung@podium.com"},
    "athlete4": {"username": "vaxelsen", "password": hash_password("password123"), "email": "v.axelsen@podium.com"},
    "athlete5": {"username": "lcwei", "password": hash_password("password123"), "email": "lc.wei@podium.com"},
    "coach1": {"username": "pmgopichand", "password": hash_password("password123"), "email": "p.gopichand@podium.com"},
    "coach2": {"username": "parkjungbong", "password": hash_password("password123"), "email": "park.jungbong@podium.com"},
}

# Mock users data
MOCK_USERS = [
    # Athlete 1: PV Sindhu
    {
        "_id": "athlete1",
        "name": "PV Sindhu",
        "role": "athlete",
        "sport": "Badminton",
        "headline": "Olympic Gold & Silver Medalist | BWF World Champion",
        "bio": "Two-time Olympic medalist and one of India's most successful badminton players. Former World Champion and multiple-time World Championship medalist.",
        "location": "Hyderabad, India",
        "category": "Singles",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/P_V_Sindhu_in_2018.jpg/800px-P_V_Sindhu_in_2018.jpg",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 28,
        "weight": "65 kg",
        "height": "179 cm",
        "playing_hand": "Right",
        "years_of_experience": 18,
        "age_category": "Senior",
        "academy": "Prakash Padukone Badminton Academy",
        "skills": [
            {"name": "Smash", "endorsements": 2100},
            {"name": "Drop Shot", "endorsements": 1800},
            {"name": "Defense", "endorsements": 1650},
            {"name": "Stamina", "endorsements": 1900}
        ],
        "experience": [
            {
                "role": "National Team Player",
                "org": "Badminton Association of India",
                "years": "2009 - Present",
                "description": "Olympic Gold (Tokyo 2020) and Silver (Rio 2016) medalist. BWF World Champion 2019."
            },
            {
                "role": "Brand Ambassador",
                "org": "Li-Ning",
                "years": "2014 - Present",
                "description": "Global brand ambassador for Li-Ning badminton equipment and apparel."
            }
        ],
        **MOCK_CREDENTIALS["athlete1"]
    },
    
    # Athlete 2: Kento Momota
    {
        "_id": "athlete2",
        "name": "Kento Momota",
        "role": "athlete",
        "sport": "Badminton",
        "headline": "Former World No. 1 | BWF World Champion 2018 & 2019",
        "bio": "Two-time World Champion known for exceptional court coverage and tactical gameplay. Comeback king who overcame major setbacks.",
        "location": "Tokyo, Japan",
        "category": "Singles",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Kento_Momota_2022.jpg/800px-Kento_Momota_2022.jpg",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 29,
        "weight": "68 kg",
        "height": "175 cm",
        "playing_hand": "Right",
        "years_of_experience": 16,
        "age_category": "Senior",
        "academy": "NTT East Badminton Club",
        "skills": [
            {"name": "Net Play", "endorsements": 2400},
            {"name": "Defense", "endorsements": 2200},
            {"name": "Court Coverage", "endorsements": 2100},
            {"name": "Deception", "endorsements": 1950}
        ],
        "experience": [
            {
                "role": "Professional Player",
                "org": "NTT East",
                "years": "2013 - Present",
                "description": "World Champion 2018 & 2019. Multiple BWF Super Series titles."
            },
            {
                "role": "Brand Ambassador",
                "org": "Yonex",
                "years": "2015 - Present",
                "description": "Official Yonex ambassador representing badminton equipment."
            }
        ],
        **MOCK_CREDENTIALS["athlete2"]
    },
    
    # Athlete 3: An Se Young
    {
        "_id": "athlete3",
        "name": "An Se Young",
        "role": "athlete",
        "sport": "Badminton",
        "headline": "World No. 1 | BWF World Champion 2023",
        "bio": "Rising star of women's badminton. Known for aggressive attacking style and exceptional speed on court.",
        "location": "Seoul, South Korea",
        "category": "Singles",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/An_Se-young_2022.jpg/800px-An_Se-young_2022.jpg",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 21,
        "weight": "59 kg",
        "height": "169 cm",
        "playing_hand": "Right",
        "years_of_experience": 9,
        "age_category": "Senior",
        "academy": "Samsung Electro-Mechanics Sports Team",
        "skills": [
            {"name": "Smash", "endorsements": 1850},
            {"name": "Speed", "endorsements": 2050},
            {"name": "Attack", "endorsements": 1920},
            {"name": "Footwork", "endorsements": 1780}
        ],
        "experience": [
            {
                "role": "Professional Player",
                "org": "Samsung Electro-Mechanics",
                "years": "2019 - Present",
                "description": "BWF World Champion 2023. Multiple BWF Tour titles."
            },
            {
                "role": "National Team Member",
                "org": "Korea Badminton Association",
                "years": "2018 - Present",
                "description": "Representing South Korea in international competitions."
            }
        ],
        **MOCK_CREDENTIALS["athlete3"]
    },
    
    # Athlete 4: Viktor Axelsen
    {
        "_id": "athlete4",
        "name": "Viktor Axelsen",
        "role": "athlete",
        "sport": "Badminton",
        "headline": "Olympic Gold Medalist | World No. 1 | BWF World Champion",
        "bio": "Dominant force in men's singles badminton. Olympic champion with exceptional power and technical precision.",
        "location": "Dubai, UAE",
        "category": "Singles",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Viktor_Axelsen_2022.jpg/800px-Viktor_Axelsen_2022.jpg",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 30,
        "weight": "88 kg",
        "height": "194 cm",
        "playing_hand": "Right",
        "years_of_experience": 17,
        "age_category": "Senior",
        "academy": "Dubai Badminton Academy",
        "skills": [
            {"name": "Smash", "endorsements": 2600},
            {"name": "Power", "endorsements": 2450},
            {"name": "Technique", "endorsements": 2300},
            {"name": "Endurance", "endorsements": 2100}
        ],
        "experience": [
            {
                "role": "Professional Player",
                "org": "Independent",
                "years": "2012 - Present",
                "description": "Olympic Gold (Tokyo 2020), World Champion 2017 & 2022. Multiple major titles."
            },
            {
                "role": "Brand Ambassador",
                "org": "Li-Ning",
                "years": "2018 - Present",
                "description": "Elite Li-Ning sponsored athlete."
            }
        ],
        **MOCK_CREDENTIALS["athlete4"]
    },
    
    # Athlete 5: Lee Chong Wei
    {
        "_id": "athlete5",
        "name": "Lee Chong Wei",
        "role": "athlete",
        "sport": "Badminton",
        "headline": "3x Olympic Silver Medalist | Former World No. 1 for 349 weeks",
        "bio": "Legendary Malaysian player widely regarded as one of the greatest badminton players of all time. Retired but still active in coaching and mentoring.",
        "location": "Kuala Lumpur, Malaysia",
        "category": "Singles",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Lee_Chong_Wei_at_French_Open_2013.jpg/800px-Lee_Chong_Wei_at_French_Open_2013.jpg",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 41,
        "weight": "60 kg",
        "height": "172 cm",
        "playing_hand": "Right",
        "years_of_experience": 25,
        "age_category": "Veteran",
        "academy": "Bukit Jalil Sports School",
        "skills": [
            {"name": "Smash", "endorsements": 3200},
            {"name": "Net Play", "endorsements": 2900},
            {"name": "Defense", "endorsements": 2750},
            {"name": "Footwork", "endorsements": 3100}
        ],
        "experience": [
            {
                "role": "National Team Player",
                "org": "Badminton Association of Malaysia",
                "years": "2000 - 2019",
                "description": "Olympic Silver (2008, 2012, 2016). 69 international titles."
            },
            {
                "role": "Mentor & Coach",
                "org": "Lee Chong Wei Academy",
                "years": "2019 - Present",
                "description": "Mentoring next generation of Malaysian badminton players."
            }
        ],
        **MOCK_CREDENTIALS["athlete5"]
    },
    
    # Coach 1: Pullela Gopichand
    {
        "_id": "coach1",
        "name": "Pullela Gopichand",
        "role": "coach",
        "sport": "Badminton",
        "headline": "Chief National Coach of India | Padma Bhushan Awardee",
        "bio": "Former All England Champion and one of India's most successful badminton coaches. Trained Olympic medalists PV Sindhu, Saina Nehwal, and many others.",
        "location": "Hyderabad, India",
        "category": "Singles & Coaching",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Pullela_Gopichand.jpg/800px-Pullela_Gopichand.jpg",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 50,
        "weight": "75 kg",
        "height": "178 cm",
        "playing_hand": "Right",
        "years_of_experience": 30,
        "age_category": "Coach",
        "academy": "Gopichand Badminton Academy",
        "skills": [
            {"name": "Coaching", "endorsements": 3500},
            {"name": "Technique Analysis", "endorsements": 3200},
            {"name": "Mental Training", "endorsements": 2900},
            {"name": "Strategy", "endorsements": 3100}
        ],
        "experience": [
            {
                "role": "Chief National Coach",
                "org": "Badminton Association of India",
                "years": "2006 - Present",
                "description": "Coached multiple Olympic medalists including PV Sindhu and Saina Nehwal."
            },
            {
                "role": "Director",
                "org": "Gopichand Badminton Academy",
                "years": "2008 - Present",
                "description": "Founded and runs one of India's premier badminton training facilities."
            }
        ],
        **MOCK_CREDENTIALS["coach1"]
    },
    
    # Coach 2: Park Joo-bong
    {
        "_id": "coach2",
        "name": "Park Joo-bong",
        "role": "coach",
        "sport": "Badminton",
        "headline": "Legendary Doubles Champion | National Coach",
        "bio": "Former badminton legend who dominated the doubles category. Now coaching the next generation of Korean champions.",
        "location": "Seoul, South Korea",
        "category": "Doubles & Coaching",
        "profile_image": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800",
        "cover_image": "https://images.unsplash.com/photo-1626224583764-847890e0e99b?q=80&w=2070",
        "age": 58,
        "weight": "72 kg",
        "height": "175 cm",
        "playing_hand": "Right",
        "years_of_experience": 40,
        "age_category": "Coach",
        "academy": "Korea National Training Center",
        "skills": [
            {"name": "Doubles Strategy", "endorsements": 3800},
            {"name": "Coaching", "endorsements": 3600},
            {"name": "Net Play", "endorsements": 3400},
            {"name": "Footwork", "endorsements": 3200}
        ],
        "experience": [
            {
                "role": "National Coach",
                "org": "Korea Badminton Association",
                "years": "2005 - Present",
                "description": "Head coach for Korean national team. Multiple world champions under guidance."
            },
            {
                "role": "Professional Player",
                "org": "Korean National Team",
                "years": "1984 - 2000",
                "description": "Multiple World Championship titles in men's and mixed doubles."
            }
        ],
        **MOCK_CREDENTIALS["coach2"]
    }
]

# Mock posts data
MOCK_POSTS = [
    # PV Sindhu's posts
    {
        "_id": "post1",
        "author_id": "athlete1",
        "content": "Amazing training session today! Working on new attack strategies for the upcoming tournament. Feeling stronger every day! 🏸💪 #Badminton #Training",
        "media_url": None,
        "type": "text",
        "likes": 1245,
        "comments": 67
    },
    {
        "_id": "post2",
        "author_id": "athlete1",
        "content": "Grateful for all the support! Another intense week of preparation. Thank you to my coach and team! 🙏",
        "media_url": None,
        "type": "text",
        "likes": 2103,
        "comments": 92
    },
    
    # Kento Momota's posts
    {
        "_id": "post3",
        "author_id": "athlete2",
        "content": "Back on court after recovery. Every day is a new opportunity to improve. Let's go! 🔥",
        "media_url": None,
        "type": "text",
        "likes": 1876,
        "comments": 134
    },
    {
        "_id": "post4",
        "author_id": "athlete2",
        "content": "Working on defensive strategies. The key to winning is not just attack, but knowing when to defend. #BadmintonTactics",
        "media_url": None,
        "type": "text",
        "likes": 1523,
        "comments": 78
    },
    
    # An Se Young's posts
    {
        "_id": "post5",
        "author_id": "athlete3",
        "content": "World Champion feeling! 🏆 Thank you everyone for the support. This is just the beginning!",
        "media_url": None,
        "type": "text",
        "likes": 3421,
        "comments": 245
    },
    {
        "_id": "post6",
        "author_id": "athlete3",
        "content": "Speed training day! Footwork is everything in badminton. 🏃‍♀️⚡",
        "media_url": None,
        "type": "text",
        "likes": 1687,
        "comments": 89
    },
    
    # Viktor Axelsen's posts
    {
        "_id": "post7",
        "author_id": "athlete4",
        "content": "Olympic champion mentality: Train like you've never won. Compete like you've never lost. 🥇",
        "media_url": None,
        "type": "text",
        "likes": 2934,
        "comments": 156
    },
    {
        "_id": "post8",
        "author_id": "athlete4",
        "content": "Perfect training weather in Dubai! Working on power and precision. #BadmintonLife",
        "media_url": None,
        "type": "text",
        "likes": 2145,
        "comments": 98
    },
    
    # Lee Chong Wei's posts
    {
        "_id": "post9",
        "author_id": "athlete5",
        "content": "Mentoring the next generation at my academy. Passing on the knowledge is the best feeling! 🎓🏸",
        "media_url": None,
        "type": "text",
        "likes": 4521,
        "comments": 312
    },
    {
        "_id": "post10",
        "author_id": "athlete5",
        "content": "Throwback to my Olympic days. Every match taught me something valuable. Never stop learning! 📚",
        "media_url": None,
        "type": "text",
        "likes": 5234,
        "comments": 421
    },
    
    # Gopichand's posts
    {
        "_id": "post11",
        "author_id": "coach1",
        "content": "Proud of all my students at the academy! Their dedication and hard work inspire me every day. 🌟",
        "media_url": None,
        "type": "text",
        "likes": 3145,
        "comments": 187
    },
    {
        "_id": "post12",
        "author_id": "coach1",
        "content": "Coaching is not just about technique, it's about building character and mental strength. #CoachingPhilosophy",
        "media_url": None,
        "type": "text",
        "likes": 2876,
        "comments": 143
    },
    
    # Park Joo-bong's posts
    {
        "_id": "post13",
        "author_id": "coach2",
        "content": "Doubles training today! Communication and trust are the foundation of great doubles play. 🤝",
        "media_url": None,
        "type": "text",
        "likes": 1923,
        "comments": 94
    },
    {
        "_id": "post14",
        "author_id": "coach2",
        "content": "The secret to success in badminton: consistency, discipline, and passion. Every champion has these! 💯",
        "media_url": None,
        "type": "text",
        "likes": 2234,
        "comments": 112
    }
]

# Mock training videos
MOCK_TRAINING_VIDEOS = [
    {
        "_id": "v1",
        "title": "Advanced Footwork Drills",
        "author": "An Se Young",
        "description": "Master the court coverage with these essential footwork patterns.",
        "video_url": "QIBIvy9hB8I",
        "thumbnail_url": "https://img.youtube.com/vi/QIBIvy9hB8I/mqdefault.jpg",
        "duration": "10:15",
        "views": "1.2M",
        "type": "link",
        "categories": ["footwork", "technique"],
        "analysis": None
    },
    {
        "_id": "v2",
        "title": "Ultimate Smash Masterclass",
        "author": "Lee Chong Wei",
        "description": "Learn the technique behind one of the fastest smashes in the world.",
        "video_url": "s3cMVBRmySc",
        "thumbnail_url": "https://img.youtube.com/vi/s3cMVBRmySc/mqdefault.jpg",
        "duration": "12:45",
        "views": "3.5M",
        "type": "link",
        "categories": ["technique", "smash"],
        "analysis": None
    },
    {
        "_id": "v3",
        "title": "Net Play Secrets",
        "author": "Kento Momota",
        "description": "Dominate the front court with deceptive net shots.",
        "video_url": "Zj_jdy1GWOc",
        "thumbnail_url": "https://img.youtube.com/vi/Zj_jdy1GWOc/mqdefault.jpg",
        "duration": "08:30",
        "views": "890K",
        "type": "link",
        "categories": ["technique", "net-play"],
        "analysis": None
    },
    {
        "_id": "v4",
        "title": "Master Footwork",
        "author": "Lin Dan",
        "description": "Legendary footwork techniques from the GOAT.",
        "video_url": "yxBVlMncudg",
        "thumbnail_url": "https://img.youtube.com/vi/yxBVlMncudg/mqdefault.jpg",
        "duration": "15:20",
        "views": "2.1M",
        "type": "link",
        "categories": ["footwork"],
        "analysis": None
    },
    {
        "_id": "v5",
        "title": "4 Corner Footwork Tutorial",
        "author": "Badminton Insight",
        "description": "Step-by-step guide to mastering movement to all four corners.",
        "video_url": "R_Qz-D18fV0",
        "thumbnail_url": "https://img.youtube.com/vi/R_Qz-D18fV0/mqdefault.jpg",
        "duration": "09:45",
        "views": "560K",
        "type": "link",
        "categories": ["footwork", "training"],
        "analysis": None
    },
    {
        "_id": "v6",
        "title": "Offensive Net Footwork",
        "author": "Basicfeather",
        "description": "Aggressive footwork to dominate the net area.",
        "video_url": "0V1t2IHEFxQ",
        "thumbnail_url": "https://img.youtube.com/vi/0V1t2IHEFxQ/mqdefault.jpg",
        "duration": "07:12",
        "views": "320K",
        "type": "link",
        "categories": ["footwork", "attack"],
        "analysis": None
    },
    {
        "_id": "v7",
        "title": "Doubles Strategy Masterclass",
        "author": "Park Joo-bong",
        "description": "Learn winning doubles strategies from a legend.",
        "video_url": "dQw4w9WgXcQ",
        "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
        "duration": "14:30",
        "views": "780K",
        "type": "link",
        "categories": ["doubles", "strategy"],
        "analysis": None
    },
    {
        "_id": "v8",
        "title": "Mental Toughness in Badminton",
        "author": "Pullela Gopichand",
        "description": "Building the champion mindset.",
        "video_url": "dQw4w9WgXcQ",
        "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
        "duration": "11:20",
        "views": "650K",
        "type": "link",
        "categories": ["mental", "coaching"],
        "analysis": None
    }
]

# Mock opportunities
MOCK_OPPORTUNITIES = [
    {
        "_id": "opp1",
        "poster_id": "coach1",
        "type": "sponsorship",
        "title": "Sponsorship Opportunity for Rising Stars",
        "description": "Looking for talented young badminton players for sponsorship program at Gopichand Academy. Great support and training facilities provided.",
        "requirements": [
            "Age 14-20",
            "National level player",
            "Dedicated to full-time training",
            "Good academic record"
        ],
        "budget": "Full scholarship + stipend"
    },
    {
        "_id": "opp2",
        "poster_id": "athlete4",
        "type": "training",
        "title": "Training Camp in Dubai",
        "description": "Elite training camp with Viktor Axelsen. Limited spots available for serious athletes looking to elevate their game.",
        "requirements": [
            "International level player",
            "Age 18+",
            "Minimum 5 years experience",
            "Good fitness level"
        ],
        "budget": "$5000 per month"
    },
    {
        "_id": "opp3",
        "poster_id": "coach2",
        "type": "coaching",
        "title": "Doubles Coaching Program",
        "description": "Specialized doubles coaching program with Park Joo-bong. Learn from the best in the business.",
        "requirements": [
            "Experienced doubles player",
            "Good communication skills",
            "Team player mentality",
            "Available for 6-month program"
        ],
        "budget": "₩10,000,000 per season"
    },
    {
        "_id": "opp4",
        "poster_id": "athlete1",
        "type": "sponsorship",
        "title": "Brand Ambassador - Sports Nutrition",
        "description": "Looking for athletes to represent premium sports nutrition brand. Great opportunity for visibility and income.",
        "requirements": [
            "Professional athlete",
            "Social media presence",
            "Passion for fitness and nutrition",
            "Available for promotional events"
        ],
        "budget": "$3000-$5000 per month"
    },
    {
        "_id": "opp5",
        "poster_id": "athlete5",
        "type": "mentorship",
        "title": "Mentorship Program for Young Players",
        "description": "Lee Chong Wei Academy offering mentorship for promising young players. One-on-one sessions with Lee Chong Wei.",
        "requirements": [
            "Age 12-18",
            "State/National level",
            "Commitment to improvement",
            "Parental support"
        ],
        "budget": "Subsidized rates available"
    }
]

async def clear_database(db):
    """Clear all existing data from collections"""
    print("🗑️  Clearing existing data...")
    collections = ["users", "posts", "training_videos", "opportunities"]
    for collection in collections:
        result = await db[collection].delete_many({})
        print(f"  ✓ Deleted {result.deleted_count} documents from {collection}")

async def seed_database():
    """Main seed function"""
    print("\n" + "="*50)
    print("🌱 Starting Database Seeding Process")
    print("="*50 + "\n")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
    db = client[settings.db_name]
    
    try:
        # Test connection
        await client.server_info()
        print("✓ Connected to MongoDB\n")
        
        # Clear existing data
        await clear_database(db)
        print()
        
        # Insert users
        print("👥 Inserting users...")
        result = await db["users"].insert_many(MOCK_USERS)
        print(f"  ✓ Inserted {len(result.inserted_ids)} users")
        print(f"    - 5 Athletes: PV Sindhu, Kento Momota, An Se Young, Viktor Axelsen, Lee Chong Wei")
        print(f"    - 2 Coaches: Pullela Gopichand, Park Joo-bong")
        print()
        
        # Insert posts
        print("📝 Inserting posts...")
        result = await db["posts"].insert_many(MOCK_POSTS)
        print(f"  ✓ Inserted {len(result.inserted_ids)} posts")
        print()
        
        # Insert training videos
        print("🎥 Inserting training videos...")
        result = await db["training_videos"].insert_many(MOCK_TRAINING_VIDEOS)
        print(f"  ✓ Inserted {len(result.inserted_ids)} training videos")
        print()
        
        # Insert opportunities
        print("💼 Inserting opportunities...")
        result = await db["opportunities"].insert_many(MOCK_OPPORTUNITIES)
        print(f"  ✓ Inserted {len(result.inserted_ids)} opportunities")
        print()
        
        # Print login credentials
        print("\n" + "="*50)
        print("🔐 LOGIN CREDENTIALS")
        print("="*50)
        print("\nPassword for ALL users: password123\n")
        print("Athletes:")
        print("-" * 50)
        for user_id, creds in MOCK_CREDENTIALS.items():
            if user_id.startswith("athlete"):
                user = next(u for u in MOCK_USERS if u["_id"] == user_id)
                print(f"  Username: {creds['username']:20} | Email: {creds['email']:30} | Name: {user['name']}")
        
        print("\nCoaches:")
        print("-" * 50)
        for user_id, creds in MOCK_CREDENTIALS.items():
            if user_id.startswith("coach"):
                user = next(u for u in MOCK_USERS if u["_id"] == user_id)
                print(f"  Username: {creds['username']:20} | Email: {creds['email']:30} | Name: {user['name']}")
        
        print("\n" + "="*50)
        print("✅ Database seeding completed successfully!")
        print("="*50 + "\n")
        
        # Summary
        print("📊 Summary:")
        print(f"  • Users: {len(MOCK_USERS)} (5 athletes + 2 coaches)")
        print(f"  • Posts: {len(MOCK_POSTS)}")
        print(f"  • Training Videos: {len(MOCK_TRAINING_VIDEOS)}")
        print(f"  • Opportunities: {len(MOCK_OPPORTUNITIES)}")
        print(f"\n  • All data stored in MongoDB: {settings.db_name}")
        print(f"  • Profile images linked from external sources")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("✓ Disconnected from MongoDB\n")

if __name__ == "__main__":
    asyncio.run(seed_database())
