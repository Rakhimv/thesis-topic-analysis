from categories import apply_categories
import pandas as pd 
import plotly.express as px

data = pd.read_excel("thesis_data.xlsx")
data = apply_categories(data)
pivot = pd.crosstab(data["Advisor"], data["category"])

fig = px.imshow(pivot, title="Связь научных руководителей и тематик", aspect="auto", color_continuous_scale="Blues")
fig.show()
