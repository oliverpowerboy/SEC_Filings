# imports
from matplotlib import pyplot as plt
import pandas as pd

# read in data
data = pd.read_csv("AccountsReceivableNetCurrent APPL.csv", index_col="index")

# convert to long int and scale down by $100,000,000
data["value"] = data["value"].astype("int64")
data["value"] = data["value"] / 100_000_000

# Convert to datetime and sort by date time
data['ddate'] = pd.to_datetime(data['ddate'], format="%Y%m%d")
data.sort_values("ddate", inplace=True)

# plot data
plot_data = data[["ddate", "value"]]

# matplot stuff
plt.style.use('fast')
plt.plot(plot_data["ddate"], plot_data["value"])
plt.ylabel("Accounts Receivable Net Current $")
plt.xlabel("date")
plt.title("Apple Inc\nNet accounts recievables ($100,000,000)")

plt.show()
