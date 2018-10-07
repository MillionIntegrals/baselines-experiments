import pandas as pd

# data = pd.read_csv("../benchmarks/atari.csv", index_col=0)
data = pd.read_csv("../benchmarks/mujoco.csv", index_col=0)

# print("STOP")

print(data.to_html(float_format=lambda x: '{:,.2f}'.format(x)))
