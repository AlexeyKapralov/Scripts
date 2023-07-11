import pandas as pd
from tkinter import Tk, messagebox, filedialog
import os
import pathlib

def show_notification(text):
    root = Tk()
    root.withdraw()  # Скрыть основное окно приложения
    messagebox.showinfo("Внимание", text)
    root.destroy()

# Получаем путь к папке, содержащей скрипт
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Отображаем диалоговое окно выбора продаж
sell_out_path = filedialog.askopenfilename(title="Выберите файл продаж для создания отчета SKU")

# сделать как путь
name_temp = pathlib.WindowsPath(sell_out_path)

name = name_temp.name

# убрать расширение
name = name.replace('.xlsx','')

name = name + "_SKU.xlsx"

osh = pd.read_excel(sell_out_path)


osh['Торговый представитель'] = osh['Торговый представитель'].str.lower()
osh['Код клиента'] = osh['Код клиента'].str.lower()
osh['Сегмент'] = osh['Сегмент'].str.lower()
osh['Клиент'] = osh['Клиент'].str.title()
osh['Адрес доставки'] = osh['Адрес доставки'].str.lower()
osh['Бренд'] = osh['Бренд'].str.title()
osh['Группа'] = osh['Группа'].str.title()
osh['Вкус'] = osh['Вкус'].str.title()

if osh['Дата отгрузки'].dtypes != '<M8[ns]':
    if osh['Дата отгрузки'].astype(str).str.match("\d{4}-\d{2}-\d{2}").all():
        osh['Дата отгрузки'] = pd.to_datetime(osh['Дата отгрузки'], yearfirst = True)
    elif osh['Дата отгрузки'].astype(str).str.match("\d{2}-\d{2}-\d{4}").all():
        osh['Дата отгрузки'] = pd.to_datetime(osh['Дата отгрузки'], dayfirst = True)
    else:
        show_notification("С датой что-то не так, проверьте плз")
        exit()


osh["Год"] = osh["Дата отгрузки"].dt.year
osh["Месяц"] = osh["Дата отгрузки"].dt.month


osh_2 = osh.copy(deep=True)

osh_2.loc[:, 'Месяц название'] = osh_2.loc[:,'Год'].astype(str) + '-' + osh_2.loc[:, 'Месяц'].astype(str)


pivot_table = osh_2.pivot_table(values='ВЕС',
                             index=['Клиент', 'Бренд', 'Вкус', 'Группа'],
                             columns='Месяц название',
                             aggfunc=lambda x: 1 if sum(x) > 0 else 0,
                             fill_value=0).reset_index()

pivot_table['Общая сумма'] = pivot_table.iloc[:, 4:].sum(axis=1)

pivot_table3 = osh_2.pivot_table(values='ВЕС',
                             index=['Клиент', 'Бренд', 'Вкус'],
                             columns='Месяц название',
                             aggfunc=lambda x: 1 if sum(x) > 0 else 0,
                             fill_value=0).reset_index()

pivot_table3['Общая сумма'] = pivot_table3.iloc[:, 3:].sum(axis=1)

pivot_table2 = pivot_table3.pivot_table(values='Клиент',
                             index=['Бренд', 'Вкус'],
                             columns='Общая сумма',
                             aggfunc=pd.Series.count,
                             fill_value=0,
                             margins=False).reset_index()

columns = pivot_table.columns.values

pivot_table['Клиент_2'] = pd.NaT

# Добавление колонки 'Клиент1'
new_column = 'Клиент_2'
columns = [new_column] + [col for col in columns if col != new_column]

pivot_table = pivot_table[columns]

with pd.ExcelWriter(desktop_path + "\\" + name) as writer:  
    pivot_table2.to_excel(writer, sheet_name='1', index=False)  
    pivot_table.to_excel(writer, sheet_name='2', index=False)