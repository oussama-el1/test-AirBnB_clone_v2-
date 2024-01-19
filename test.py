from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(50))

# Create an SQLite in-memory database engine
engine = create_engine('sqlite:///:memory:')

# Create a session factory using sessionmaker
Session = sessionmaker(bind=engine)

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Add some data to the tables
user = User(name='John Doe')
product = Product(name='Product C')

# Add the objects to the session
session.add(user)
session.add(product)

# Commit the changes to the database
session.commit()

# Query all objects from all tables
all_objects = []
for table_class in Base._decl_class_registry.values():
    if hasattr(table_class, '__tablename__'):
        objects = session.query(table_class).all()
        all_objects.extend(objects)

# Print the results before deletion
print("Before Deletion:")
for obj in all_objects:
    print(f"{obj.__class__.__name__} - {obj}")

# Delete the user object from the session
session.delete(user)

# Commit the changes to the database
session.commit()

# Query all objects from all tables after deletion
all_objects_after_deletion = []
for table_class in Base._decl_class_registry.values():
    if hasattr(table_class, '__tablename__'):
        objects = session.query(table_class).all()
        all_objects_after_deletion.extend(objects)

# Print the results after deletion
print("\nAfter Deletion:")
for obj in all_objects_after_deletion:
    print(f"{obj.__class__.__name__} - {obj}")

# Close the session
session.close()
