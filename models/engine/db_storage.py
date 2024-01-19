#!/usr/bin/python3
""""impoted module in DB storage"""
import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """class to save in DataBase"""
    __engine = None
    __session = None

    def __init__(self):
        """constructor create engine"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                        format(os.getenv("HBNB_MYSQL_USER"),
                                os.getenv("HBNB_MYSQL_PWD"),
                                os.getenv("HBNB_MYSQL_HOST"),
                                os.getenv("HBNB_MYSQL_DB")),
                        pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "Test":
            metadata = MetaData()
            metadata.reflect(bind=self.__engine)
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """all object for a classe or for database"""
        objects = {}
        if cls is not None and cls in classes.values():
            cls_objects =  self.__session.query(cls).all()
            for obj in cls_objects:
                key = obj.to_dict()['__class__'] + '.' + obj.id
                objects[key] = obj
        else :
            for classe_table in classes.values():
                if hasattr(classe_table, '__tablename__'):
                    all_objects = self.__session.query(classe_table).all()
                    for obj in all_objects:
                        key = obj.to_dict()['__class__'] + '.' + obj.id
                        objects[key] = obj
        return objects

    def new(self, obj):
        """add obj to session"""
        self.__session.add(obj)

    def save(self):
        """commit change to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an object"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all table and a session for db"""
        Base.metadata.create_all(self.__engine)
        session_factory  = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
