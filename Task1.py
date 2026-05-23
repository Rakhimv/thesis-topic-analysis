import pandas as pd
from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from categories import expand_department_name, department_mapping, speciality_mapping, categories, get_category, apply_categories


data = pd.read_excel("thesis_data.xlsx")
data = apply_categories(data)
total = data["category"].value_counts().reset_index()
total.columns = ["category", "count"]
total = total.sort_values("count", ascending=True)





stop_words = {"для", "на", "по", "в", "с", "и", "к", "о", "из",
              "при", "за", "от", "не", "до", "об"}

bigrams, words = [], []
for title in data["Title_ru"].dropna():
    tokens = [w for w in title.lower().split() if len(w) > 3 and w not in stop_words]
    words.extend(tokens)
    bigrams.extend(f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1))

top_bigrams = Counter(bigrams).most_common(20)[::-1]
top_words   = Counter(words).most_common(20)[::-1]



print("\n****** топ словосочетаний ******")
print(top_bigrams[::-1])
print("\n****** топ слов ******")
print(top_words[::-1])

fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=("Распределение по категориям",
                    "Топ-20 биграмм в категории",
                    "Топ-20 слов в категории"),
    vertical_spacing=0.08,
    row_heights=[0.3, 0.35, 0.35],
)

fig.add_trace(go.Bar(
    x=total["count"], y=total["category"], orientation="h",
    marker_color="#4C78A8", text=total["count"], textposition="outside",
), row=1, col=1)

fig.add_trace(go.Bar(
    x=[c for _, c in top_bigrams], y=[b for b, _ in top_bigrams],
    orientation="h", marker_color="#F58518",
    text=[c for _, c in top_bigrams], textposition="outside",
), row=2, col=1)

fig.add_trace(go.Bar(
    x=[c for _, c in top_words], y=[w for w, _ in top_words],
    orientation="h", marker_color="#54A24B",
    text=[c for _, c in top_words], textposition="outside",
), row=3, col=1)

fig.update_layout(
    height=1500, showlegend=False,
    title_text="Анализ тем дипломных работ",
    margin=dict(l=220, r=80, t=80, b=40),
)
fig.update_xaxes(title_text="Количество")
fig.update_yaxes(
    tickmode='array',
    tickvals=total["category"],
    automargin=True,
    row=1, col=1
)
fig.update_layout(
    height=2200,  
    width=1400,
    autosize=False,
)
fig.write_html("thesis_plots.html", auto_open=False)
fig.show()
print("thesis_plots.html")