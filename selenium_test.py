from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def get_url():
    #https://ranobelib.me/yumemiru-danshi-wa-genjitsushugisha?section=info&ui=5279067
    dirty_url = input("Введите url ранобэ: ")

    index = dirty_url.split("&")[-1]
    ranobe_name = dirty_url.split("?")[0]

    url = ranobe_name + "/v1/c1?" 
    return url


def get_driver(url):
    # Selenium setting
    cf_path = r"C:\Users\kasae\Desktop\Projects\PYTHON_NEW\Telegram bots\botParserGPTwork\chromedriver.exe"
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    options = Options()
    options.add_argument(f'user-agent={ua}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=cf_path, options=options)
    driver.get(url)

    return driver


def parser(driver, url):
    ranobe_name = url.split("ranobelib.me/")[-1].split("/v")[0]

    while True:
        # BS4
        html = driver.page_source
        driver.quit()

        soup=BeautifulSoup(html,'html.parser')
        
        volume = url.split("/v")[-1].split("/")[0]
        chapter = url.split("/c")[-1].split("?")[0]

        #Записываем строки в текстовый файл
        page_text = soup.find("div", class_="reader-container container container_center").children
        
        #Записываем в txt файл
        with open(f'loads/{ranobe_name}.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n\nТом {volume}  Глава {chapter}\n\n\n\n")
            for paragraph in page_text:
                paragraph = str(paragraph).replace("<p>", "").replace("</p>", "\n")

                file.write(paragraph + "\n")
            print(f"Скачано:  Том {volume}  Глава {chapter}")
        


        #Проверка на наличие след. главы
        url = soup.find_all("a", class_="reader-header-action reader-header-action_icon")[-1].get("href")

        if str(url) != "#":
            driver = get_driver(url)
        else:
            print("Все готово!")
            break



    
def main():
    url = get_url()
    driver = get_driver(url)
    parser(driver, url)




try:
    main()
except Exception as e:
    print(e, "Произошла ошибка!")


