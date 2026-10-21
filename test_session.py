from database import SessionLocal

db = SessionLocal()

print("Session created successfully!")

db.close()

print("Session closed!")