from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base

def main():
    engine = create_engine("sqlite:///lostthings.db", echo=True)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()