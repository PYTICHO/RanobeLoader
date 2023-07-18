from bs4 import BeautifulSoup
import requests, os, time


def mkdir_if_not_exist(directory="ranobe_loads"):
    if not os.path.exists(directory):
        os.mkdir(directory)



def is_file(filename, directory='ranobe_loads'):
    filename = filename + '.txt'

    if os.path.isfile(os.path.join(directory, filename)):
        return True
    
    return False





def get_session(login, password, user_agent):
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent})

    #auth
    login_url = r"https://lib.social/login"
    login_response_get = session.get(login_url)
    login_soup = BeautifulSoup(login_response_get.text, "html.parser")
    token = login_soup.find('input', {'name': '_token'}).get('value')
    data = {
        "_token": token,
        "from": "https://ranobelib.me/?section=home-updates",
        "email": login,
        "password": password,
        "remember": "on"
    }
    login_response_post = session.post(login_url, data=data)
    if login_response_post.status_code == 200:
        print("Успешная авторизация!")
    else:
        print("Не удалось авторизоваться!")
    
    return session




def get_url_and_name(session):
    #https://ranobelib.me/yumemiru-danshi-wa-genjitsushugisha?section=info&ui=5279067
    dirty_url = input("Введите url ранобэ: ")

    response = session.get(dirty_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    url = soup.find("a", class_='button button_block button_primary').get("href")
    ranobe_name = soup.find('div', class_='media-name__main').get_text(strip=True)

    return url, ranobe_name





def parser(url, session, directory, ranobe_name):
    if not is_file(ranobe_name, directory):
        while True:
            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            volume = url.split("/v")[-1].split("/")[0]
            chapter = url.split("/c")[-1].split("?")[0]

            #Записываем строки в текстовый файл
            page_text = soup.find("div", class_="reader-container container container_center").children
            
            #Записываем в txt файл
            with open(f'{directory}/{ranobe_name}.txt', 'a', encoding='utf-8') as file:
                file.write(f"Том {volume}  Глава {chapter}\n\n\n\n")
                for paragraph in page_text:
                    paragraph = str(paragraph).replace("\n", ' ').replace("<p>", "").replace("</p>", "\n")
                    
                    if len(str(paragraph)) <= 2:
                        continue

                    file.write(paragraph + "\n")
                file.write("\n\n")
                print(f"Скачано:  Том {volume}  Глава {chapter}")
            



            #Проверка на наличие след. главы
            url = soup.find_all("a", class_="reader-header-action reader-header-action_icon")[-1].get("href")
            url = url.split("?")[0]

            if str(url) == "#":
                print("Готово!")
                break

    else:
        print("Ранобэ уже скачано!")
            



    
def main():
    directory = "ranobe_loads"
    mkdir_if_not_exist(directory)

    #Data
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    login = "kasaev_2006@inbox.ru"
    password = "Qwertyqwerty2006"

    #session
    session = get_session(login, password, user_agent)
    url, ranobe_name = get_url_and_name(session)
    parser(url, session, directory, ranobe_name)


try:
    main()
except Exception as e:
    print(e, "Произошла ошибка!")


time.sleep(10)