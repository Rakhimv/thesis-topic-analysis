import pandas as pd
from categories import get_category, categories

data = pd.read_excel("thesis_data.xlsx")

proche = data[data['Title_ru'].apply(get_category) == "Прочее"]

print(f"Всего в 'Прочее': {len(proche)} работ\n")

for i, title in enumerate(proche['Title_ru'].head(20), 1):
    print(f"{i}. {title}")

for title in proche['Title_ru'].head(20):
    title_lower = title.lower()
    found = False
    for cat, keywords in categories.items():
        for kw in keywords:
            if kw in title_lower:
                found = True
                break
        if found:
            break
    if not found:
        print(f"НЕТ КЛЮЧЕЙ: {title[:80]}...")