import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("thesis_data.xlsx")
sorted_data = data.sort_values('Speciality')

speciality_counts = sorted_data['Speciality'].value_counts()
total = speciality_counts.sum() 

threshold_percent = 2
threshold = total * threshold_percent / 100

filtered_counts = {}
others_sum = 0

for specialty, count in speciality_counts.items():
    if count >= threshold:
        filtered_counts[specialty] = count
    else:
        others_sum += count

if others_sum > 0:
    filtered_counts['Другие'] = others_sum

plt.figure(figsize=(10, 8))
plt.pie(filtered_counts.values(), 
        labels=filtered_counts.keys(),
        autopct='%1.1f%%',
        startangle=90)
plt.title(f'Распределение по специальностям (< {threshold_percent}% объединены)', fontsize=16)
plt.axis('equal')
plt.show()