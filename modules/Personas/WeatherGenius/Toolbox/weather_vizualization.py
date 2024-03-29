import matplotlib.pyplot as plt

# Define the data
dates = ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']
temperatures = [85.96, 87.28, 92.98, 96.69, 98.29]
rainfall = [0, 3.98, 1.94, 0, 0.31]

# Create the figure and axes
fig, ax1 = plt.subplots()

# Plot the temperature data
ax1.plot(dates, temperatures, color='tab:red', marker='o')
ax1.set_ylabel('Temperature (°F)', color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

# Create a second y-axis for rainfall data
ax2 = ax1.twinx()
ax2.bar(dates, rainfall, color='tab:blue', alpha=0.5)
ax2.set_ylabel('Rainfall (inches)', color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# Set the title and labels
plt.title('Weather Forecast for Shreveport, LA')
plt.xlabel('Date')

# Add a legend
ax1.legend(['Temperature'], loc='upper left')
ax2.legend(['Rainfall'], loc='upper right')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot
plt.show()