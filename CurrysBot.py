from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import re
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from time import strptime
import os

options = Options()
options.add_argument('headless')
options.add_argument("--disable-notifications")
options.add_argument('window-size=1920x1080')
driver=wd.Chrome(executable_path ='C:/chromedriver.exe',chrome_options=options)

__all__=['currys_dong_scraper']
class currys_dong_scraper:

    
    def __init__(self, url):
        self.url=url
        
    def dong_scraper(self):
        try:
            driver.get(self.url)
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="product-main"]/div[1]/div[1]/div/a[1]').click()
            try:
                WebDriverWait(driver, 35).until(
                    # 지정한 한개 요소가 올라면 웨이트 종료
                    EC.presence_of_element_located( (By.CLASS_NAME, 'pagination'))
                )
            except Exception as e:
                print( '오류 발생', e)

            total_reviews=driver.page_source
            ttl_reviewsj=BeautifulSoup(total_reviews,"html.parser")
            number_of_reviews=ttl_reviewsj.find("h3",{'class':"filtered-count summary"})
            abc=number_of_reviews.text.split()
            reviews_total=int(abc[0])

            product_name=ttl_reviewsj.find('span',{'class':'product_name'})
            productName=product_name.text


            score_list=[]
            date_list=[]
            pros_list=[]
            cons_list=[]
            while len(score_list)<=reviews_total:

                bsobj=driver.page_source
                bs_obj=BeautifulSoup(bsobj,"html.parser")

                score=bs_obj.findAll('div',{"class":"overall_score_stars"})  
                for i in range(len(score)):
                    score_list.append(re.findall("\d+",score[i].text)[0])

                Date=bs_obj.findAll('span',{'class':"date date_publish"})
                for j in range(len(Date)):
                    date_list.append(Date[j].text.strip())

                pros=bs_obj.findAll('dd',{'class':'pros'})
                for k in range(len(pros)):
                    pros_list.append(pros[k].text)


                cons=bs_obj.findAll('dd',{'class':'cons'})
                for h in range(len(cons)):
                    cons_list.append(cons[h].text)


                driver.find_element_by_class_name('next_page').click()
                try:
                    WebDriverWait(driver, 35).until(
                    # 지정한 한개 요소가 올라면 웨이트 종료
                        EC.presence_of_element_located( (By.CLASS_NAME, 'pagination'))
                    )

                except Exception as e:
                    print( '오류 발생' + e)
                time.sleep(3)
        except Exception as abc:
            print(abc)

            driver.close()
            driver.quit()
        
            '''score_final=[re.findall("\d+", u)[0] for u in score_list]'''

                
            final=pd.DataFrame({'Rating':score_list,'Date':date_list,'Pros':pros_list,'Cons':cons_list})
            Month=[]
            Year=[]
            Date_2=[]
            for date_x in final['Date']:
                month_ind=datetime.strptime(date_x,'%d %B %Y')
                year_ind=datetime.strptime(date_x,'%d %B %Y')
                int_date=datetime.strptime(date_x,'%d %B %Y')
                Year.append(year_ind.year)
                Month.append(month_ind.month)
                Date_2.append(int_date)
                
            final['Month']=Month
            final['Year']=Year
            final['int Date']=Date_2
            final["Rating"]= final["Rating"].astype(int)
            final.sort_values(by='int Date',ascending=False,inplace=True)
            
            os.chdir('D:/download')
            writer=pd.ExcelWriter('Currys_65Q60.xlsx',engine='xlsxwriter')
            final.to_excel(writer,sheet_name=productName[:15])
            
            writer.save()
