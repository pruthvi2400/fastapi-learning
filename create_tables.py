from database import engine
from model import Base

Base.metadata.create_all(engine)

print("Tables created successfully!")