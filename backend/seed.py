from app.database import Base, engine, SessionLocal
from app.models import User, Profile, EmergencyContact, CommunityPost, Mentor, Course, Complaint
from app.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    user = db.query(User).filter_by(email="demo@sherise.com").first()
    if not user:
        user = User(name="Demo User", email="demo@sherise.com", hashed_password=get_password_hash("123456"))
        db.add(user)
        db.commit()
        db.refresh(user)

        db.add(Profile(
            user_id=user.id,
            full_name="Demo User",
            phone="0771234567",
            address="Colombo, Sri Lanka",
            occupation="Undergraduate Student",
            bio="Welcome to SheRise. This demo account shows all core features of the system."
        ))

        contacts = [
            EmergencyContact(user_id=user.id, name="Emergency Services", relationship="Emergency", phone="911", is_primary=True),
            EmergencyContact(user_id=user.id, name="Mom", relationship="Mother", phone="+1 234 567 8901", is_primary=False),
            EmergencyContact(user_id=user.id, name="Best Friend", relationship="Friend", phone="+1 234 567 8902", is_primary=False),
        ]
        db.add_all(contacts)

        posts = [
            CommunityPost(user_id=user.id, title="Welcome to SheRise", content="Share your questions, achievements, and support here.", category="Welcome"),
            CommunityPost(user_id=user.id, title="Career Tip", content="Update your skills consistently and build a strong profile to unlock new opportunities.", category="Career"),
        ]
        db.add_all(posts)

        mentors = [
            Mentor(owner_id=user.id, name="Asha Perera", expertise="Career Guidance", email="asha@example.com", phone="0711111111", description="Helps students plan career paths and personal branding.", availability="Weekends"),
            Mentor(owner_id=user.id, name="Nimali Silva", expertise="Legal Awareness", email="nimali@example.com", phone="0722222222", description="Supports women with legal information and complaint guidance.", availability="Weekdays"),
        ]
        db.add_all(mentors)

        courses = [
            Course(
                owner_id=user.id,
                title="Digital Marketing Fundamentals",
                category="Marketing",
                provider="SheRise Academy",
                instructor="D.R. Ashera",
                description="Learn the basic of digital marketing including SEO, social media, and content marketing.",
                duration="8 weeks",
                level="Beginner",
                image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=900",
                progress=65,
                is_premium=False,
            ),
            Course(
                owner_id=user.id,
                title="Leadership & Management",
                category="Leadership",
                provider="SheRise Academy",
                instructor="D.S. Rshith",
                description="Develop essential leadership skills and learn effective team management strategies.",
                duration="6 week",
                level="Intermediate",
                image_url="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=900",
                progress=35,
                is_premium=False,
            ),
            Course(
                owner_id=user.id,
                title="Web Development Bootcamp",
                category="Technology",
                provider="SheRise Academy",
                instructor="R.M. Sachini",
                description="Complete web development course covering HTML, CSS, JavaScript, and React.",
                duration="12 Week",
                level="Beginner",
                image_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=900",
                progress=0,
                is_premium=True,
            ),
        ]
        db.add_all(courses)

        db.add(Complaint(
            user_id=user.id,
            subject="Sample Complaint",
            description="This is a sample complaint to show CRUD functionality.",
            complaint_type="Awareness",
            status="Submitted",
        ))
        db.commit()
        print("Seed completed. Demo login: demo@sherise.com / 123456")
    else:
        print("Demo user already exists: demo@sherise.com / 123456")
finally:
    db.close()
