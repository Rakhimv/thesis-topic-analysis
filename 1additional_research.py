import pandas as pd
import matplotlib.pyplot as plt

from categories import teacher_eng_mapping

data = pd.read_excel("thesis_data.xlsx")

data['Advisor'] = data['Advisor'].astype(str).str.strip() #берём колонки, на строки бъём, удаляем пробелы
data['Advisor_mapped'] = data['Advisor'].map(teacher_eng_mapping).fillna(data['Advisor'])
data['Advisor_mapped'] = data['Advisor_mapped'].replace(['nan', 'None', ''], pd.NA) # Колонка, где пустые заменены на флаг NA 

advisor_counts = data['Advisor_clean'].value_counts().dropna() #считаем и удаляем с маркером NA

top_10 = advisor_counts.head(10) #берём первые 10 

plt.figure(figsize=(12, 8))
plt.barh(range(len(top_10)), top_10.values, color='steelblue') #строим горизонтальные графики
plt.yticks(range(len(top_10)), top_10.index) #подписываем имена преподавателей
plt.xlabel('Количество работ') #подпись оси x
plt.title('Топ-10 преподавателей по количеству работ') #Заголовок
plt.gca().invert_yaxis() #самый частый - сверху

#v + 0.3 — позиция по X 
#i — позиция по Y 
for i, v in enumerate(top_10.values):
    plt.text(v + 0.3, i, str(v), va='center')

plt.tight_layout() #настраивает отступы
plt.show() #запуск