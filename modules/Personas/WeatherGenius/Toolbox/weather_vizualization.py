import matplotlib.pyplot as plt

dates = ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']
temperatures = [85.96, 87.28, 92.98, 96.69, 98.29]
rainfall = [0, 3.98, 1.94, 0, 0.31]

fig, ax1 = plt.subplots()

ax1.plot(dates, temperatures, color='tab:red', marker='o')
ax1.set_ylabel('Temperature (°F)', color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

ax2 = ax1.twinx()
ax2.bar(dates, rainfall, color='tab:blue', alpha=0.5)
ax2.set_ylabel('Rainfall (inches)', color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

plt.title('Weather Forecast for Shreveport, LA')
plt.xlabel('Date')

ax1.legend(['Temperature'], loc='upper left')
ax2.legend(['Rainfall'], loc='upper right')

plt.xticks(rotation=45)

plt.show()