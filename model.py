import os
import sys



class Step():
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Article(Base, id, title, max):
  id = 
  title = 
  max_lenght = 
  step = relationship("Step")
  content = 
  author = 
  exergue = 
  due_date = 


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

