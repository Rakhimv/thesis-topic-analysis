import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import os

data = pd.read_excel("thesis_data.xlsx")

from categories import expand_department_name, department_mapping, speciality_mapping

# Пытаемся найти совпадения из словаря
def normalize_speciality(spec): 
    if pd.isna(spec):  # Проверка на пустое
        return ""
    spec = str(spec).strip()  # Удаляем пробелы
    if spec in speciality_mapping:  # Если есть совпадение возвращаем из словаря
        return speciality_mapping[spec]
    return spec  # Если нет, то возвращаем исходное

def safe_filename(name):
    forbidden = r'[\\/*?:"<>|]'
    safe = re.sub(forbidden, '_', str(name)) # Замена всех символов из r на _ 
    safe = safe.strip('. ') # Удаляю . и пробел
    return safe[:200]

def expand_department_name(dept):
    if pd.isna(dept): # Замена пустых на None
        return None
    code = str(dept).strip()
    return department_mapping.get(code, code)

data['Department_Full'] = data['Department'].apply(expand_department_name) # Создаёт доп колонку с полными названиями кафедр

os.makedirs("speciality_wordclouds", exist_ok=True) # Создание папки
dept_stats = [] # Пустой список для хранения облоков

for department in data['Department_Full'].dropna().unique(): # Удаляем пустые и берём только уникальные
    dept_data = data[data['Department_Full'] == department] # Создаёт данные только с одной кафедрой

    #[normalize_speciality(spec) for spec  in dept_data['Speciality'] - берёт специальность и нормализует
    #Затем спомощью filter уберает все пустые  и считает
    spec_counts = Counter(filter(None, [normalize_speciality(spec) for spec  in dept_data['Speciality']]))

    total = len(dept_data)
    unique = len(spec_counts)
    dept_stats.append((department, total, unique)) #Статистика

    if not spec_counts: #Если счётчик пуст, то едем дальше
        continue
    
    #сортируем по количеству и берём первые 25 записей
    top = dict(spec_counts.most_common(25))

    wc = WordCloud(width=1200, height=600, background_color='white', colormap='plasma') #создаёт объект облака
    wc.generate_from_frequencies(top) #генерируем из 25 самых встречаемых
     
    plt.imshow(wc) #отображаем полученное
    plt.axis('off') #отключаем оси
    plt.title(f'Специальности на кафедре\n{department}\n(записей: {total}, спец.: {unique})') #заголовок
    plt.savefig(f'speciality_wordclouds/{safe_filename(department)}.png', bbox_inches='tight', dpi=300) #сохраняем файлик
    plt.close()#закрываем

os.makedirs("advisor_wordclouds", exist_ok=True) # создам папку

data['Advisor'] = data['Advisor'].astype(str).str.strip() # преобразуем в строку и чистим пробелы

for advisor in data['Advisor'].unique(): #цикл по уникальным
    if advisor == 'nan' or advisor == '': 
        continue
    
    adv_data = data[data['Advisor'] == advisor] #создаём для конкретного руководителя
    
    specs = [normalize_speciality(s) for s in adv_data['Speciality'] if pd.notna(s)] # сохраняем в список если не пустые 
    spec_counts = Counter(specs) # считаем
    
    if not spec_counts: # пусто - next
        continue
    
    wc = WordCloud(width=1200, height=600, background_color='white', colormap='viridis') #создание объекта
    wc.generate_from_frequencies(dict(spec_counts.most_common(25))) #генерируем из 25 самых встречаемых
    
    plt.imshow(wc) # Облако отображаем
    plt.axis('off') # Сетку выключаем
    plt.title(f'Направления научных руководителей\n{advisor}\n(всего: {len(adv_data)})') # Заголовок подписываем
    plt.savefig(f'advisor_wordclouds/{safe_filename(advisor)}.png', bbox_inches='tight', dpi=300) # Файл сохраняем
    plt.close() # Фигурку закрываем