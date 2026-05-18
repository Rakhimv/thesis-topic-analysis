import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import os
from collections import Counter

data = pd.read_excel("thesis_data.xlsx")

speciality_mapping = {
    'Фундаментальная информатика и информационные технологии': 'Фундаментальная информатика и ИТ',
    'Фундаментальная информатика и ИТ': 'Фундаментальная информатика и ИТ',
    'Фундаментальные математика и механика': 'Фундаментальные математика и механика',
    'Прикладная математика и информатика': 'Прикладная математика и информатика',
    'Прикладная математика и физика': 'Прикладная математика и физика',
    'Прикладные математика и физика': 'Прикладная математика и физика',
    'Математическое обеспечение и администрирование информационных систем': 'Математическое обеспечение и администрирование ИС',
    'Программная инженерия': 'Программная инженерия',
    'Механика и математическое моделирование': 'Механика и математическое моделирование',
    'Математика': 'Математика',
    'Математика и механика': 'Математика и механика',
    'Математика и компьютерные науки': 'Математика и компьютерные науки',
    'Информатика и вычислительная техника': 'Информатика и вычислительная техника',
    'Компьютерные и информационные науки': 'Компьютерные и информационные науки',
    'Физика и астрономия': 'Физика и астрономия',
    'Астрономия': 'Астрономия',
    'Системный анализ и управление': 'Системный анализ и управление',
    'Прикладная информатика': 'Прикладная информатика',
}

department_mapping = {
    'tp': 'Кафедра технологии программирования',
    'vmmdt': 'Кафедра вычислительных методов механики деформируемого тела',
    'kmms': 'Кафедра компьютерного моделирования и многопроцессорных систем',
    'tsuefa': 'Кафедра теории систем управления электрофизической аппаратурой',
    'mstnmo': 'Кафедра математического моделирования энергетических систем',
    'mems': 'Кафедра моделирования электромеханических и компьютерных систем',
    'kts': 'Кафедра компьютерных технологий и систем',
    'tu': 'Кафедра теории управления',
    'mud': 'Кафедра механики управляемого движения',
    'mes': 'Кафедра математического моделирования энергетических систем',
    'mses': 'Кафедра моделирования социально-экономических систем',
    'vm': 'Кафедра вычислительной математики',
    'is': 'Кафедра информационных систем',
    'ktpa': 'Кафедра космических технологий и прикладной астродинамики',
    'mtmpsu': 'Кафедра математической теории микропроцессорных систем управления',
    'mtmsu': 'Кафедра математической теории моделирования систем управления',
    'umbs': 'Кафедра управления медико-биологическими системами',
    'dfs': 'Кафедра диагностики функциональных систем',
    'mmes': 'Кафедра моделирования экономических систем',
    'mter': 'Кафедра математической теории экономических решений',
}

#Пытаемся найти совпадения из словаря
def normalize_speciality(spec):
    if pd.isna(spec):
        return ""
    spec = str(spec).strip()
    if spec in speciality_mapping:
        return speciality_mapping[spec]
    for key, value in speciality_mapping.items():
        if key in spec or spec in key:
            return value
    return spec

#Чистим строку
def clean_speciality(text):
    if pd.isna(text):
        return ""
    return normalize_speciality(re.sub(r'\s+', ' ', str(text).strip()))

def safe_filename(name):
    forbidden = r'[\\/*?:"<>|]'
    safe = re.sub(forbidden, '_', str(name))
    safe = safe.strip('. ')
    return safe[:200]

def expand_department_name(dept):
    if pd.isna(dept):
        return None
    code = str(dept).strip()
    return department_mapping.get(code, code)

data['Department_Full'] = data['Department'].apply(expand_department_name)

os.makedirs("speciality_wordclouds", exist_ok=True)
dept_stats = []

for department in data['Department_Full'].dropna().unique(): 
    dept_data = data[data['Department_Full'] == department]
    
    spec_counts = Counter(filter(None, [clean_speciality(spec) for spec in dept_data['Speciality']]))
    
    total = len(dept_data)
    unique = len(spec_counts)
    dept_stats.append((department, total, unique))
    
    if not spec_counts:
        continue
    
    top = dict(sorted(spec_counts.items(), key=lambda x: x[1], reverse=True)[:25])
    
    wc = WordCloud(width=1200, height=600, background_color='white', colormap='plasma')
    wc.generate_from_frequencies(top)  
    
    plt.imshow(wc)
    plt.axis('off')
    plt.title(f'Специальности на кафедре\n{department}\n(записей: {total}, спец.: {unique})')
    plt.savefig(f'speciality_wordclouds/{safe_filename(department)}.png', bbox_inches='tight', dpi=300)
    plt.close()