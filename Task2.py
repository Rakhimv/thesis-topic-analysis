import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("thesis_data.xlsx")

from categories import get_category

data["category"] = data["Title_ru"].apply(get_category)# Получаем категории

faculty_filter = data['Faculty'] == 'Процессы управления'
data = data[faculty_filter]

yearly_categories = data.groupby(["Graduation", "category"]).size().unstack(fill_value=0) # группируем строки по году и тематики, считаем, и разворачиваем в таблицу

fig, ax = plt.subplots(figsize=(14, 8))
yearly_categories.plot(kind='bar', stacked=True, ax=ax)

ax.set_xlabel('Год выпуска', fontsize=12)
ax.set_ylabel('Количество работ', fontsize=12)
ax.set_title('Распределение тематик дипломных работ по годам', fontsize=14)
ax.tick_params(axis='x', rotation=45)

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.01, 1),  # правее графика, сверху
    borderaxespad=0,
    fontsize=9,
    frameon=True,
)

plt.tight_layout()          # подгоняет всё кроме легенды
plt.savefig("thesis_yearly.png", dpi=150, bbox_inches='tight')  # bbox_inches='tight' захватывает легенду
plt.show()