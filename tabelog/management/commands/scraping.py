from django.core.management.base import BaseCommand
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
#from getpass import getpass
#from bs4 import BeautifulSoup
import time
import re
from tabelog.models import Restaurant
from datetime import datetime #日付上限を設定して新規店舗を抽出

class Command(BaseCommand):
    help = "食べログスクレイピング処理"
    
    def handle(self, *args, **options):
        print("スクレイピング処理")

        # ヘッドレスモードで起動するためのオプションを設定
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        

        # Chromeを立ち上げる
        chrome_driver = webdriver.Chrome(options=chrome_options)

        # 東京都の食べログのトップページにアクセス
        chrome_driver.get('https://tabelog.com/tokyo/')

        # 最大30秒間、トップページが表示されるのを待つ
        wait = WebDriverWait(chrome_driver, 30)

        # エリアを指定して入力する　※同じ駅名の場合どうすればよいか
        station_name = input('駅名を入力してください：')
        pernet_element = chrome_driver.find_element(By.CSS_SELECTOR, '#react-search-header > form > div.sc-fHSyak.sc-dubCtV.ljbUvS.hhzuBp')
        station_input = pernet_element.find_element(By.CLASS_NAME, 'sc-uhnfH.hGDSLA')
        station_input.send_keys(station_name)

        # 該当駅周辺のページへ遷移する
        search_button = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#react-search-header > form > div.sc-ikHGee.JTHPh > button')
        )
                                   )
        search_button.click()
        time.sleep(5)
        

        # ニューオープンに遷移する
        newopen_button = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'li.navi-rstlst__tab.navi-rstlst__tab--new > a')
        )
                                    )
        newopen_button.click()
        time.sleep(10)
        chrome_driver.save_screenshot('screenshot.png')
        
        # 店舗リストを取得（上限日を指定）
        restaurants = chrome_driver.find_elements(By.CSS_SELECTOR, 'div.list-rst__contents')
        limit_date = datetime(2025, 9, 1)
        
        while True:
        
            for restaurant in restaurants:
                try:
                    name = restaurant.find_element(By.CSS_SELECTOR, 'a.list-rst__rst-name-target').text
                    url = restaurant.find_element(By.CSS_SELECTOR, 'a.list-rst__rst-name-target').get_attribute('href')
                
                    # 店舗IDを抽出
                    match = re.search(r'/(\d+)/$', url)
                    restaurant_id = match.group(1) if match else None
                
                    # オープン日を取得
                    open_date_text = restaurant.find_element(By.CSS_SELECTOR, '.list-rst__newopen.is-highlight').text
                    open_date_text = open_date_text.replace("オープン", "").strip()
                    open_date = datetime.strptime(open_date_text, "%Y年%m月%d日")
                 
                    # 条件を満たす場合だけ保存
                    if open_date >= limit_date:
                        Restaurant.objects.get_or_create(
                            restaurant_id=restaurant_id,
                            defaults={
                                "station": station_name,
                                "name": name,
                                "url": url,
                                "open_date": open_date
                            }
                        )
                        print(f"保存: {station_name} -{name} ({restaurant_id} {url} {open_date})")
                    else:
                        print(f"スキップ: {name} - {open_date}")
                        break
                
                except Exception as e:
                    print(f"保存失敗: {e}")
            else:
                # 次のページボタンを押下
                page_no += 1
                continue
            
            break   #  whileループを抜ける(途中でスキップした場合)

                
        chrome_driver.quit()
        print("スクレイピング処理終了")
        
        #ニューオープンが指定日付だけでなければ、次のページへ遷移する
        #ニューオープンの日付を今日の日付から30日前移行の日付にする
        #次のページに押下するのところで、何ページ目のボタンを押下するかを記述する、ページナンバー