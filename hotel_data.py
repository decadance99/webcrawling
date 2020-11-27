import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:decadance99@localhost/prac')
engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)

driver = webdriver.Chrome("C:/Users/eugene/chromedriver.exe")

driver.get('https://www.agoda.com/ko-kr/pages/agoda/default/DestinationSearchResult.aspx?asq=rp7c5epycLthZ0hHoORGnpufa9Vwpz6XltTHq4n%2B9gN3dKLJ2CSXy2MFQ4mXIPMkG8mkPiCChFumqFZwERSiKVCFcPsjdKRWeTMp2t6jQpMNYJ%2FcCWv%2F24SObsMFxXBeq%2F%2BbkS51iQs%2FzvQsTUxKZQ%2Foa8qaSyQrg61mdIzB86KPzSkK9fKrnjwxW6q6lPcIzPx3p8UWZS2iN1I3SW%2BqojVI1hfLTktOcN3QfCrx%2FY0%3D&city=16901&cid=1732639&tag=a85f57f6-f4b0-5117-39ff-f69b8b36db1a&gclid=Cj0KCQjwkIzlBRDzARIsABgXqV9474e-pU1st8ZdlFWySlL168eYxXpRblOaoy9bxbsHGkWD5Xwh6eUaAtLFEALw_wcB&tick=636898847383&isdym=true&searchterm=%EC%A0%9C%EC%A3%BC%EB%8F%84%EB%8F%84&txtuuid=62401b76-c320-499e-81f9-ce04e8f77881&languageId=9&userId=d668e3a1-5c83-493c-9b69-118608c89cab&sessionId=4fjgaxujjqkkm4i0l24hq2g2&pageTypeId=1&origin=KR&locale=ko-KR&aid=81837&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-KR&ckuid=d668e3a1-5c83-493c-9b69-118608c89cab&prid=0&checkIn=2019-04-12&checkOut=2019-04-13&rooms=1&adults=2&children=0&priceCur=KRW&los=1&textToSearch=%EC%A0%9C%EC%A3%BC%EB%8F%84%EB%8F%84&productType=-1&travellerType=1&familyMode=off')
sleep(5)

driver.find_element_by_class_name('CalendarAlertMessage__close').click()
sleep(5)

driver.find_element_by_css_selector("a[data-element-name='search-sort-price']").click()
sleep(5)

actions = ActionChains(driver)
last_height = driver.execute_script("return document.body.scrollHeight")
while(True):
    for _ in range(15):
        actions.send_keys(Keys.SPACE).perform()
        sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
print("loading complete")
driver.execute_script("window.scrollTo(0, 0);")
sleep(3)

content = BeautifulSoup(driver.page_source, 'html.parser')
list_items = content.findAll('li',{'class':["PropertyCardItem","ssr-search-result"]})

class Hotel(Base):

    __tablename__ = 'newhotels'

    name = Column(String(30), primary_key=True)
    price = Column(String(10))

    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def __str__(self):
        return self.name + " = " + self.price

    def __repr__(self):
        return str(self)


hotels = []
for item in list_items:
    hotel_name = item.find('h3', class_="InfoBox__HotelTitle")
    price = item.find('span', class_="price-box__price__amount")

    if hotel_name is not None and price is not None:
        new_hotel_data = Hotel(hotel_name.text, price.text)
        hotels.append(new_hotel_data)

print(hotels)
sleep(5)
driver.quit()

session = Session()

for i in range(len(hotels)):
    session.add(hotels[i])

Base.metadata.create_all(engine)
session.commit()
temp = session.query(Hotel).all()
print(temp)

for item in temp:
    session.delete(item)

temp = session.query(Hotel).all()
print(temp)