from imapclient import IMAPClient
import os
import pandas as pd
import datetime
import email
import base64
from email.header import decode_header

# Создание таблицы и сохранение на рабочий стол
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# desktop_path = r"C:\Users\alewk\OneDrive\Desktop"
table_path = os.path.join(desktop_path, 'email_table.xlsx')

# Параметры подключения
imap_server = 'imap.mail.ru'
username = 'reports@burntobacco.com'
# для работы
password = '0X1aKArHY5ESi6z3sZKV'

def get_start_end_date_of_week(week_number, year):
    # Создаем объект datetime с первым днем года
    first_day = datetime.datetime(year, 1, 1)

    # Находим дату первого дня недели (понедельник)
    if first_day.weekday() == 0:  # Если first_day - понедельник
        first_weekday = first_day
    else:
        days_to_previous_monday = 7 - first_day.weekday()
        first_weekday = first_day + datetime.timedelta(days=days_to_previous_monday)

    # Вычисляем количество дней, чтобы достичь нужной недели
    days_offset = datetime.timedelta(weeks=week_number-1)

    # Находим дату начала недели
    start_date = first_weekday + days_offset

    # Находим дату конца недели
    end_date = start_date + datetime.timedelta(days=6)

    return start_date, end_date

# Пример использования
week_number = 26
year = 2023

start_date, end_date = get_start_end_date_of_week(week_number, year)

# Выводим результаты
print(f"Дата начала недели {week_number}: {start_date}")
print(f"Дата конца недели {week_number}: {end_date}")

# для дома
# password = 'MiBi4HjmnAdZ3Qh89stY'

# Подключение к серверу
with IMAPClient(imap_server, ssl=True) as imap_connection:

    # Аутентификация
    imap_connection.login(username, password)

    # выбор подпапки
    folder_name = 'Отчеты'
    imap_connection.select_folder(folder_name)

    # Получение списка папок
    folder_list = imap_connection.list_folders()

    # Список для хранения данных
    data = []

    i = 0
    folder_list_len = len(folder_list)
    # Обработка полученного списка папок
    for folder_info in folder_list:
        folder_name = folder_info[2]
        if folder_name.startswith('Отчеты/') == False:
            i += i
            continue
        print(str(i) + " / " + str(folder_list_len))
        i += 1

        # Переключение на текущую папку
        imap_connection.select_folder(folder_name)

        # Определенная дата, после которой искать сообщения
        target_date = datetime.datetime.strptime('2023-07-01', '%Y-%m-%d')


        

        # Формируем критерий для поиска сообщений
        search_criteria = [
        ['SINCE', start_date.strftime('%d-%b-%Y')],
        ['BEFORE', (end_date + datetime.timedelta(days=1)).strftime('%d-%b-%Y')]  # Добавляем 1 день, чтобы включить конечную дату
]

        # Получение списка писем в текущей папке, удовлетворяющих критерию
        messages = imap_connection.search(search_criteria)

        # Обработка полученного списка писем
        for msg_id in messages:
            # Получение информации о письме
            msg_data = imap_connection.fetch([msg_id], ['ENVELOPE'])

            # Извлечение закодированного заголовка письма
            envelope = msg_data[msg_id][b'ENVELOPE']
            # encoded_subject = envelope.subject.decode('utf-8')

            # Декодирование заголовка письма
            
            # Удаление префикса и суффикса
            # encoded_subject = encoded_subject.replace('=?utf-8?B?', '').replace('?=','')

            # раскодирование заголовка
            # subject = base64.b64decode(encoded_subject).decode('utf-8')
            
            # Получение адреса отправителя
            # sender_mailbox = envelope.from_[0].mailbox.decode('utf-8')
            # sender_host = envelope.from_[0].host.decode('utf-8')
            # sender = f'{sender_mailbox}@{sender_host}'

            # get date
            # date = datetime.datetime.strptime('2023-07-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            # if envelope.date <= start_date or envelope.date >= end_date:
            #     continue
            letter_date = envelope.date

            # Save attachments
            msg_info = imap_connection.fetch([msg_id], ['RFC822'])
            raw_email = msg_info[msg_id][b'RFC822']
            msg = email.message_from_bytes(raw_email)
            attachments_folder = os.path.join(desktop_path, 'attachments')
            os.makedirs(attachments_folder, exist_ok=True)
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()

                    # Используйте функцию decode_header() для декодирования имени файла
                    
                    filename_parts = decode_header(filename)
                    decoded_parts = []

                    for part1, encoding in filename_parts:
                        if isinstance(part1, bytes):
                            if encoding is not None:
                                part1 = part1.decode(encoding)
                            decoded_parts.append(part1)

                    filename = ' '.join(decoded_parts)

                    file_path = os.path.join(attachments_folder, filename)
                    with open(file_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))



            # print('   Письмо:', subject)
            # print('   Папка:', folder_name)
            # print('   Дата:', letter_date)

            folder_name = folder_name.replace('Отчеты/','')
            data.append([folder_name, letter_date])

    # Создание DataFrame из данных
    df = pd.DataFrame(data, columns=['Папка', 'Дата'])

    df.to_excel(table_path, index=False)

    # Закрытие соединения
    imap_connection.logout()

print('Таблица сохранена на рабочий стол:', table_path)