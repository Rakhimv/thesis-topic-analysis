import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("thesis_data.xlsx")
print(sorted(data["Graduation"]))

