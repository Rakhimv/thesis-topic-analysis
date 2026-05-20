from categories import apply_categories
import pandas as pd
import plotly.graph_objects as go

data = pd.read_excel("thesis_data.xlsx")
data = apply_categories(data)
pivot = pd.crosstab(data["Advisor"], data["category"])
main_topic = pivot.idxmax(axis=1)
main_topic_pct = (pivot.max(axis=1) / pivot.sum(axis=1) * 100).round(1)
result = pd.DataFrame({
    "Преподаватель": main_topic.index,
    "Основная тематика": main_topic.values,
    "Доля работ (%)": main_topic_pct.values,
    "Всего работ": pivot.sum(axis=1).values
}).sort_values("Всего работ", ascending=False)
fig_table = go.Figure(data=[go.Table(
    header=dict(values=list(result.columns),
                fill_color='steelblue',
                align='left',
                font=dict(color='white', size=12)),
    cells=dict(values=[result[col] for col in result.columns],
               fill_color='lavender',
               align='left',
               font_size=11))
])
fig_table.update_layout(title="Специализация преподавателей по тематикам", height=600)
fig_table.show()
