import requests
import csv

# Файлы для чтения и записи
wallets_file = 'wallets.txt'
results_file = 'results.csv'

# Открываем файл с кошельками и читаем адреса
with open(wallets_file, 'r') as f:
    wallet_addresses = [line.strip() for line in f if line.strip()]

# Открываем файл для записи результатов в формате CSV
with open(results_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Адрес', 'Раунд 2 (токены)', 'Статус']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for address in wallet_addresses:
        url = f'https://layerzero.foundation/api/proof/{address}'
        response = requests.get(url)
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
                'Статус': 'Ошибка при получении данных'
            })

print(f"Проверка завершена. Результаты сохранены в файле {results_file}.")
