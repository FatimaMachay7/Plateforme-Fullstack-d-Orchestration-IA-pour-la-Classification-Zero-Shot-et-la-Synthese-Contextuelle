from sqlalchemy import Column, Integer, Text, Float
from database import Base, engine

class classification(Base):
    __tablename__ = "classify"  
    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    category = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
# Création des tables dans PostgreSQL: 
Base.metadata.create_all(bind=engine)
