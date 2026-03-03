from app.core.database import SessionLocal
from app.models.document import Document

def seed():
    db = SessionLocal()

    exists = db.query(Document).first()
    if exists:
        print("Database already seeded.")
        return

    sample = Document(
        title="Sample Contract",
        source_type="paste",
        raw_text="This is a sample contract."
    )

    db.add(sample)
    db.commit()
    print("Seeded database.")

if __name__ == "__main__":
    seed()
