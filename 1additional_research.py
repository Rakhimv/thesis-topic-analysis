import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("thesis_data.xlsx")

data['Advisor'] = data['Advisor'].astype(str).str.strip()
data['Advisor_clean'] = data['Advisor'].replace(['nan', 'None', ''], pd.NA)

advisor_counts = data['Advisor_clean'].value_counts().dropna()

top_10 = advisor_counts.head(10)

plt.figure(figsize=(12, 8))
plt.barh(range(len(top_10)), top_10.values, color='steelblue')
plt.yticks(range(len(top_10)), top_10.index)
plt.xlabel('Количество работ')
plt.title('Топ-10 преподавателей по количеству работ')
plt.gca().invert_yaxis()

for i, v in enumerate(top_10.values):
    plt.text(v + 0.3, i, str(v), va='center')

plt.tight_layout()
plt.show()