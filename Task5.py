from categories import apply_categories, expand_department_name
import pandas as pd 
import plotly.express as px

data = pd.read_excel("thesis_data.xlsx")
data = apply_categories(data)
data["Department"] = data["Department"].apply(expand_department_name)
pivot = pd.crosstab(data["Department"], data["category"])

fig = px.imshow(pivot, title="Связь кафедр и тематик", aspect="auto", color_continuous_scale="Blues")
fig.show()