import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("thesis_data.xlsx")

from categories import get_category

data["category"] = data["Title_ru"].apply(get_category)# Получаем категории

yearly_categories = data.groupby(["Graduation", "category"]).size().unstack(fill_value=0) # группируем строки по году и тематики, считаем, и разворачиваем в таблицу

yearly_categories.plot(kind='bar', stacked=True, figsize=(14, 8)) # Создаём график
plt.xlabel('Год выпуска', fontsize=12) # Подписи
plt.ylabel('Количество работ', fontsize=12) # Ещё подписи 
plt.title('Распределение тематик дипломных работ по годам', fontsize=14) # И ещё чуть чуть
plt.show() # Да будет свет