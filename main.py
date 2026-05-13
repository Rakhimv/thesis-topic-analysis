import pandas as pd
import plotly.express as px


data = pd.read_excel("thesis_data.xlsx")
yrs = sorted(data["Graduation"])

yrs_count = data["Graduation"].value_counts().sort_index().reset_index()
yrs_count.columns = ["year", "count"]

print(yrs_count)

fig = px.bar(yrs_count, x="year", y="count", title="Col-vo rabot")
fig.show()