#Advanced topics in python sql queries 

#imports 
from puppypopulator import Shelter, Puppy
from sqlalchemy import create_engine
from datetime import date, timedelta

engine = create_engine('sql:///puppyshelter.db')
DBSession = sessionmaker(bind = engine)
session = DBSession()

results = session.query(Puppy).all.order_by(Puppy.name)
for pup in results:	
	print pup.name 
#puppies that are less than six months old
results = session.query(Puppy).all.order_by((date.today()-Puppy.dateOfBirth).d>183)
 
