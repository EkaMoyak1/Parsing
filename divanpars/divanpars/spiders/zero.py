from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime

# Настройки
LOGIN_URL = "https://university.zerocoder.ru/cms/system/login?required=true"
TARGET_URL = "https://university.zerocoder.ru/teach/control/stream/view/id/921295709"
USERNAME = "Moyeka@gmail.com"
PASSWORD = "Moyeka17101970"

# Инициализация драйвера
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Раскомментируйте для безголового режима

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def get_hw_status(element):
    """Получаем статус ДЗ через вычисление стилей ::after"""
    script = """
    var element = arguments[0];
    return window.getComputedStyle(element, '::after').getPropertyValue('content');
    """
    status = driver.execute_script(script, element)
    return status.strip('"') if status else "Нет данных"

def get_url_lessons(driver):
    result = []
    result1 = driver.find_elements(By.CLASS_NAME, "col-md-12")
    for res in result1:
        result.append(res.find_elements(By.TAG_NAME, "a").get_attribute("href"))
    return result


try:
    # Авторизация
    driver.get(LOGIN_URL)

    # Ждем появления формы входа
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    # Вводим данные
    driver.find_element(By.NAME, "email").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, 'xdgetr6376_1_1_1_1_1_1_1_1_1_1_1').click()

    # Ждем авторизации (проверяем элемент, который появляется после входа)
    time.sleep(10)

    # Переходим на целевую страницу
    driver.get(TARGET_URL)
    time.sleep(3)  # Даем странице загрузиться

    url_lessons = get_url_lessons(driver)
    print(url_lessons)
    for url_l in url_lessons:
        # Переходим на целевую страницу
        driver.get(url_l)
        time.sleep(3)  # Даем странице загрузиться

        # Создаем CSV файл
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'zero_results_{timestamp}.csv'

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Урок', 'Статус ДЗ', 'URL'])

            # Парсим уроки
            lessons = driver.find_elements(By.CSS_SELECTOR, "div.vmiddle")
            for lesson in lessons:
                try:
                    # Извлекаем данные
                    title = lesson.find_element(By.CSS_SELECTOR, "div.link.title").text
                    url = lesson.find_element(By.CSS_SELECTOR, "div.link.title").get_attribute("href")

                    # Статус ДЗ через ::after
                    hw_status = get_hw_status(lesson)

                    # Записываем в CSV
                    writer.writerow([title,  hw_status, url])
                    print(f"Добавлено: {title} | ДЗ: {hw_status}")

                except Exception as e:
                    print(f"Ошибка при обработке элемента: {e}")
                    continue

finally:
    driver.quit()
    print("Парсинг завершен. Результаты сохранены в", filename)