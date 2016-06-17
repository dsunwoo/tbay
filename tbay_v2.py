from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    item = relationship("Item", backref="owner")
    bid = relationship("Bid", backref="user")
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bid_id = relationship("Bid", backref="item")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    biduser_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
   
Base.metadata.create_all(engine)

dan = User(name="Daniel", password="12345")
david = User(name="David", password="12345")
ben = User(name="Benjamin", password="12345")

baseball = Item(name="Baseball", description="Heavily used baseball",
                    owner=dan)

davidbid1=Bid(price=100,user=david,item=baseball)
davidbid2=Bid(price=120,user=david,item=baseball)
benbid1=Bid(price=101,user=ben,item=baseball)
benbid2=Bid(price=122,user=ben,item=baseball)

session.add_all([dan, david, ben])

# Query to find highest bidder
bidlist=session.query(Bid.price, Bid.biduser_id).order_by(desc(Bid.price)).all()
print("\n{} is selling a {}!\n".format(baseball.owner.name,baseball.name))
print("The bids are as follow in descending order: \n")
print(bidlist)

session.commit()

