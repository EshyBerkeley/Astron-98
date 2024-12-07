# Eshwary Mishra

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

# Part 1

# 1a) Load and filter data
df = pd.read_csv('GlobalLandTemperaturesByState.csv')
df_filtered = df[['dt', 'AverageTemperature', 'State']]
df_filtered['dt'] = pd.to_datetime(df_filtered['dt'], format='%Y-%m-%d')
df_filtered = df_filtered[df_filtered['dt'].dt.year >= 2000]
df_filtered = df_filtered[df_filtered['State'].isin(['Wyoming', 'Nebraska', 'South Dakota'])]

# Check the resulting DataFrame
print(df_filtered.shape)

df_grouped = df_filtered.groupby('dt')['AverageTemperature'].mean().reset_index()

# 1c) Plot grouped data
# I have commented this out because I plot the curve and the fitted curve together later
# I left this here to show I did 1c
# plt.plot(df_grouped['dt'], df_grouped['AverageTemperature'], label='Average Temperature')
# plt.xlabel('Date')
# plt.ylabel('Average Temperature (°C)')
# plt.title('Average Temperature for Wyoming, Nebraska, and South Dakota (After 2000)')
# plt.xticks(rotation=45)
# plt.show()

# 1d) I am using unix time as a numeric representation of the date
df_grouped['date_numeric'] = (df_grouped['dt'] - pd.Timestamp('1970-01-01')) // pd.Timedelta('1D')

# 1e) I am guessing a cosine function based on the earlier plot (now commented out)
def model(t, A, period, phi, B):
    return A * np.cos((2 * np.pi / period) * t + phi) + B

initial_guess = [10, 365, 0, df_grouped['AverageTemperature'].mean()]
t_values = df_grouped['date_numeric']
y_values = df_grouped['AverageTemperature']

# 1f) Perform the optimization (curve fitting)
params_opt, params_cov = opt.curve_fit(model, t_values, y_values, p0=initial_guess)
A_opt, period_opt, phi_opt, B_opt = params_opt

# Plot the original data and the fitted curve
plt.plot(df_grouped['dt'], y_values, label="Original Data", color='blue')
plt.plot(df_grouped['dt'], model(t_values, *params_opt), label="Fitted Curve", color='red')
plt.xlabel('Date')
plt.ylabel('Average Temperature (°C)')
plt.title('Curve Fitting to Temperature Data')
plt.legend()
# plt.show()

# 1h) Calculate and print the errors
param_errors = np.sqrt(np.diag(params_cov))
print(f"Parameter errors:")
print(f"A (Amplitude) = {A_opt} +- {param_errors[0]}")
print(f"Period = {period_opt} +- {param_errors[1]}")
print(f"Phi (Phase shift) = {phi_opt} +- {param_errors[2]}")
print(f"B (Vertical offset) = {B_opt} +- {param_errors[3]}")

print("\nFinal fitted equation:")
print(f"y(t) = {A_opt:.2f} * cos((2 * pi / {period_opt:.2f}) * t + {phi_opt:.2f}) + {B_opt:.2f}")

# Putting this here means it prints all information and then shows the plot so we can view both simultaneously
plt.show()