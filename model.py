import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Step(Base):
  __tablename__ = 'steps'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  next_step = relationship("Step")


class Article(Base):
  __tablename__ = 'articles'
  id = Column(Integer, primary_key=True)
  title = Column(String(250), nullable=False)
  max_lenght = Column(Integer, nullable=True)
  step = relationship("Step")
  content = Column(String, nullable=True)
  author = Column(String(250), nullable=True)
  exergue = Column(String(255), nullable=True)
  due_date = Column(String(20), nullable=True)


class Pictures(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    path = Column(String(), nullable=True)
    article_id = relationship("Article")


engine = create_engine('sqlite:///sqlalchemy_example.db')
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    'Rédaction'
    'Correction'
    'Intégration'
    'Archive'
    new_step = Step(name=step_name)
    session.add(new_step)
    session.commit()

