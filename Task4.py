from categories import apply_categories, teacher_eng_mapping
import pandas as pd 
import plotly.express as px


data = pd.read_excel("thesis_data.xlsx")
data = apply_categories(data)

data["Advisor"] = data["Advisor"].astype(str).str.strip()
data["Advisor_mapped"] = data["Advisor"].map(teacher_eng_mapping).fillna(data["Advisor"])

pivot = pd.crosstab(data["Advisor_mapped"], data["category"])

fig = px.imshow(pivot, title="Связь научных руководителей и тематик", aspect="auto", color_continuous_scale="Blues")
fig.show()