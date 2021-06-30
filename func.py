try:
    from bs4 import BeautifulSoup
except Exception:
    print('pip install -r requirements.txt')


def getParsel(Barcode):
    from selenium import webdriver  # Чтобы парсить JS код нам нужен селениум

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Браузер скрыт
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])  # Убираем ненужный логгинг

    browser = webdriver.Chrome(chrome_options=options)  # Создаем браузер

    # Берем ссылку на посылку, йоу
    browser.get(f'https://www.pochta.ru/tracking#{Barcode}')

    generated_html = browser.page_source  # Берем исходный код страницы
    browser.quit()  # Убиваем браузер, т.к. он нам больше не нужен

    soup = BeautifulSoup(generated_html, 'html.parser')  # Подключаем суп

    data = {}  # В эту переменную мы будем записывать данные, которые спарсили

    #  Название посылки
    data['Name'] = soup.find(
        'div', class_='RenameTitle__Title-sc-14slmoz-0 RjSLq').get_text(strip=True)
    #  Примерная дата получения
    if soup.find(
            'div', class_='TrackingCardHistory__HistoryItem-zdvopc-3 TrackingCardHistory__FuturePathHistoryItem-zdvopc-4 kIXBeA gStSWv') != None:
        data['GetDate'] = soup.find(
            'div', class_='TrackingCardHistory__HistoryItem-zdvopc-3 TrackingCardHistory__FuturePathHistoryItem-zdvopc-4 kIXBeA gStSWv').get_text(strip=True)
    else:
        data['GetDate'] = 'Примерная дата получения неизвестна!'
    #  Все операции с посылкой
    operations = soup.find_all(
        'div', class_='TrackingCardHistory__HistoryItem-zdvopc-3 kIXBeA')

    #  Отбираем операции с посылкой в более удобную форму для реализации
    opers = []
    for operation in operations:
        opers.append(operation.get_text(strip=True))

    #  Записываем их в наш dict
    data['Operations'] = opers
    #  Это будет последней операцией над посылкой
    data['LastOperation'] = opers[0]

    return data
