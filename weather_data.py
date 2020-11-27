import urllib.request as req
from time import sleep
from bs4 import BeautifulSoup
import datetime
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+pymysql://eugene:decadance99@hwdb.cccjpm0ld2pa.us-east-2.rds.amazonaws.com/hwdb')
engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=True)

#request 객체를 사용하여 url을 연다
url = "https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09410120"
res = req.urlopen(url)

#매일 최저 기온과 최고 기온을 저장하기 위한 class
class Weather(Base):

    __tablename__ = 'weathers'

    id = Column(Integer, Sequence('weather_seq'), primary_key=True)
    low_tmp = Column(String(30))
    high_tmp = Column(String(10))
    date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, low_tmp, high_tmp):
        self.low_tmp = low_tmp
        self.high_tmp = high_tmp

    def __repr__(self):
        id = ""
        if self.id is not None:
            id = str(self.id)
        else:
            id = "None"
        return "<Weather('%s', '%s', '%s', '%s')>" % (id, self.date, self.low_tmp, self.high_tmp)


#BeautifulSoup을 사용한다
#기온 텍스트를 가지고 오기 위해 CSS Selector를 사용하여 list로 받아 온 후,
#최저 기온과 최고 기온을 변수에 저장한다
#Weather 객체를 만들고, Session 객체를 만들고 세션에 Weather 객체를 추가한다
#그런 후 데이터베이스에 연결하여 세션을 commit한다
content = BeautifulSoup(res, 'html.parser')
results = content.select("#content > table.tbl_weather.tbl_today3 > tbody > tr > td > div > ul > li.nm > span")
low_tmp = results[0].string
high_tmp = results[1].string
today = Weather(low_tmp, high_tmp)


session = Session()
session.add(today)

Base.metadata.create_all(engine)
session.commit()

# try:
#     session.commit()
# finally:
#     session.flush()
#     session.close()


# new = session.query(Weather).all()
# print(new)

#세션에 저장된 모든 Weather 객체를 temp 변수에 저장하고, 전부 삭제한다
temp = session.query(Weather).all()
print(temp)

for item in temp:
    session.delete(item)

#세션이 비었다는 것을 확인하기 위해 Weather 객체가 있는지 출력해 본다
temp = session.query(Weather).all()
print(temp)