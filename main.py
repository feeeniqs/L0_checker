import requests
import csv
from itertools import cycle

# Файлы для чтения и записи
wallets_file = 'wallets.txt'
proxies_file = 'proxies.txt'
results_file = 'results.csv'

# Открываем файл с кошельками и читаем адреса
with open(wallets_file, 'r') as f:
    wallet_addresses = [line.strip() for line in f if line.strip()]

# Открываем файл с прокси и читаем их
with open(proxies_file, 'r') as f:
    proxy_list = [line.strip() for line in f if line.strip()]

# Проверяем, есть ли прокси в списке
if not proxy_list:
    print("Список прокси пуст. Пожалуйста, добавьте прокси в файл proxies.txt.")
    exit()

# Создаем цикл прокси для ротации
proxy_pool = cycle(proxy_list)

# Открываем файл для записи результатов в формате CSV
with open(results_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Адрес', 'Раунд 2 (токены)', 'Статус']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for address in wallet_addresses:
        proxy = next(proxy_pool)
        proxies = {
            'http': proxy,
            'https': proxy
        }

        url = f'https://layerzero.foundation/api/proof/{address}'

        try:
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                data = response.json()
                round2 = int(data.get('round2', 0))

                # Конвертируем сумму из wei в токены
                round2_tokens = round2 / 1e18

                writer.writerow({
                    'Адрес': address,
                    'Раунд 2 (токены)': f"{round2_tokens:.2f}",
                    'Статус': 'Успешно'
                })
            else:
                writer.writerow({
                    'Адрес': address,
                    'Раунд 2 (токены)': '',
                    'Статус': f'Ошибка: статус код {response.status_code}'
                })
        except Exception as e:
            writer.writerow({
                'Адрес': address,
                'Раунд 2 (токены)': '',
                'Статус': f'Ошибка: {e}'
            })

print(f"Проверка завершена. Результаты сохранены в файле {results_file}.")
