import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import os

data = pd.read_excel("thesis_data.xlsx")

# Импортируем функции
from categories import get_category, department_mapping, speciality_mapping, teacher_eng_mapping

# Пытаемся найти совпадения из словаря (оставлено для совместимости)
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

# Добавляем колонку с полными названиями кафедр
data['Department_Full'] = data['Department'].apply(expand_department_name)

# Добавляем колонку с категориями
data['Category'] = data['Title_ru'].apply(get_category)

os.makedirs("category_wordclouds_by_dept", exist_ok=True) # Создание папки
dept_stats = [] # Пустой список для хранения статистики

for department in data['Department_Full'].dropna().unique(): # Удаляем пустые и берём только уникальные
    dept_data = data[data['Department_Full'] == department] # Создаёт данные только с одной кафедрой
    
    # Исключаем "Прочее" из подсчёта
    dept_data_filtered = dept_data[dept_data['Category'] != "Прочее"]
    
    # Считаем КАТЕГОРИИ 
    cat_counts = Counter(dept_data_filtered['Category'].dropna())

    total = len(dept_data) # Всего работ на кафедре
    total_filtered = len(dept_data_filtered) # Работ не из "Прочего"
    unique = len(cat_counts)
    dept_stats.append((department, total, total_filtered, unique)) # Статистика

    if not cat_counts: # Если счётчик пуст, то едем дальше
        continue
    
    # Сортируем по количеству и берём первые 25 записей
    top = dict(cat_counts.most_common(25))

    wc = WordCloud(width=1200, height=600, background_color='white', 
                   colormap='plasma', min_font_size=20) # Создаёт объект облака
    wc.generate_from_frequencies(top) # Генерируем из 25 самых встречаемых
     
    plt.imshow(wc) # Отображаем полученное
    plt.axis('off') # Отключаем оси
    plt.title(f'Категории работ на кафедре\n{department}\n'
              f'(всего: {total}, без "Прочего": {total_filtered}, категорий: {unique})') # Заголовок
    plt.savefig(f'category_wordclouds_by_dept/{safe_filename(department)}.png', 
                bbox_inches='tight', dpi=300) # Сохраняем файлик
    plt.close() # Закрываем

os.makedirs("category_wordclouds_by_advisor", exist_ok=True) # Создаём папку

data['Advisor'] = data['Advisor'].astype(str).str.strip() # Преобразуем в строку и чистим пробелы
data['Advisor_mapped'] = data['Advisor'].map(teacher_eng_mapping).fillna(data['Advisor'])#Заменяем псевдонимы на ФИО 

for advisor in data['Advisor_mapped'].unique(): # Цикл по уникальным
    if advisor == 'nan' or advisor == '': 
        continue
    
    adv_data = data[data['Advisor_mapped'] == advisor] # Создаём для конкретного руководителя
    
    # Исключаем "Прочее" из подсчёта
    adv_data_filtered = adv_data[adv_data['Category'] != "Прочее"]
    
    # Считаем КАТЕГОРИИ 
    cat_counts = Counter(adv_data_filtered['Category'].dropna())
    
    if not cat_counts: # Пусто - next
        continue
    
    wc = WordCloud(width=1200, height=600, background_color='white', 
                   colormap='viridis', min_font_size=20) # Создание объекта
    wc.generate_from_frequencies(dict(cat_counts.most_common(25))) # Генерируем из 25 самых встречаемых
    
    plt.imshow(wc) # Облако отображаем  
    plt.axis('off') # Сетку выключаем
    total_adv = len(adv_data)
    total_adv_filtered = len(adv_data_filtered)
    plt.title(f'Категории работ руководителя\n{advisor}\n'
              f'(всего: {total_adv}, без "Прочего": {total_adv_filtered})') # Заголовок подписываем
    plt.savefig(f'category_wordclouds_by_advisor/{safe_filename(advisor)}.png', 
                bbox_inches='tight', dpi=300) # Файл сохраняем
    plt.close() # Фигурку закрываем