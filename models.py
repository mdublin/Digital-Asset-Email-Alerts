from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime


Base = declarative_base()


from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime


class Video(Base):
    __tablename__ = "video_alerts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    bc_id = Column(String, nullable=True)
    sent_date = Column(DateTime, default=datetime.utcnow)
    Google_server_response = Column(String, nullable=False)



engine = create_engine('sqlite:///notifications.db')
Base.metadata.create_all(engine)

