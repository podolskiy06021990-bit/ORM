import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values
from database.PostgreSQLHandler import save_rates_to_db
from database.PostgreSQLHandler import setup_database
# Настройки подключения к базе данных
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'



def parse_currency_rates():
    url = "https://www.cbr.ru/currency_base/daily/"
    rates = {}
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return rates

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='data')
        if not table:
            print("Таблица с классом 'data' не найдена.")
            return rates

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 6:
                code = cols[1].get_text(strip=True)
                if code in ['USD', 'EUR']:
                    value_text = cols[4].get_text(strip=True).replace(',', '.')
                    try:
                        value = float(value_text)
                    except ValueError:
                        print(f"Не удалось преобразовать значение курса для {code}: {value_text}")
                        continue

                    change_text = cols[5].get_text(strip=True)
                    try:
                        change_value = float(change_text.replace(',', '.'))
                        change_str = f"+{change_value}" if change_value > 0 else str(change_value)
                    except ValueError:
                        print(f"Не удалось преобразовать изменение курса для {code}: {change_text}")
                        change_str = "0.0"

                    rates[code] = {
                        "value": value,
                        "change": change_str
                    }
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")

    return rates

# Основная логика
rates_dict = parse_currency_rates()
if rates_dict:
    setup_database()
    save_rates_to_db(rates_dict)