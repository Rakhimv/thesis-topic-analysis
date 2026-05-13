import pandas as pd

data = pd.read_excel("thesis_data.xlsx")
print(sorted(data["Graduation"]))

