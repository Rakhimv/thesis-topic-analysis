import pandas as pd
from collections import Counter

data = pd.read_excel("thesis_data.xlsx")

from categories import expand_department_name, department_mapping, speciality_mapping, categories, get_category, apply_categories

print(apply_categories(data).value_counts())

stop_words = ["для", "на", "по", "в", "с", "и", "к", "о", "из", "при", "за", "от", "не", "до", "об"]
bigrams = []
for title in data[data["category"] == "Прочее"]["Title_ru"].dropna():
    words = [w for w in title.lower().split() if len(w) > 3]
    for i in range(len(words) - 1):
        bigrams.append(f"{words[i]} {words[i+1]}")

print("\n\n****** топ словосочетаний ******\n")
print(Counter(bigrams).most_common(20))

words = []
for title in data[data["category"] == "Прочее"]["Title_ru"].dropna():
    for word in title.lower().split():
        if word not in stop_words and len(word) > 3:
            words.append(word)

print("\n\n****** топ слов ******\n")      
print(Counter(words).most_common(20))