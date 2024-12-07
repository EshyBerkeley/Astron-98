# Functions for analysis; abstracted away since they are used twice and I did not want to copy and paste
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import os
import fpdata

script_dir = os.path.dirname(__file__)
plt.switch_backend('Qt5Agg')

# Basically distance formula but accounts for curvature of the Earth
# I doubt it'll make a huge difference, but might as well
def haversine(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km

# Apply this function to calculate distances from a high-impact location (lat, lon)
def calculate_distances(data, high_impact_zones, impact_zone_idx):
    calc_lat = high_impact_zones[impact_zone_idx][0]
    calc_long = high_impact_zones[impact_zone_idx][1]
    data['distance_from_zone_' + str(impact_zone_idx)] = data.apply(
        lambda row: haversine(row['latitude'], row['longitude'], calc_lat, calc_long), axis=1
    )
    return data

def bin_data(data, impact_zone_idx):
    bins = np.arange(0, fpdata.cluster_radius, fpdata.bin_size)
    binned_data = pd.cut(data['distance_from_zone_' + str(impact_zone_idx)], bins=bins)
    return binned_data.value_counts().sort_index()

# Binned data is an array containing arrays that represent the histograms
def populate_binned_data(data, high_impact_zones):
    binned_data = []
    # Find distances and curve fit for c
    for idx in range(len(high_impact_zones)):
        data = calculate_distances(data, high_impact_zones, idx)
        binned_counts = bin_data(data, idx)
        
        # distance_bins is a array of the range for each bin
        # counts is the amount of data per bin (this is what we are interested in)
        distance_bins = binned_counts.index.astype(str)
        counts = binned_counts.values
        
        binned_data.append(counts)
        
        # Enable this to see the histogram of distances from high-impact location
        if fpdata.plot_input_data_histograms:
            plt.figure(figsize=(10, 6))
            bars = plt.bar(distance_bins, counts, color='skyblue', edgecolor='black')

            for bar, count in zip(bars, counts):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, str(count), 
                        ha='center', va='bottom', fontsize=10)

            plt.xlabel('Distance Bins (km)')
            plt.ylabel('Count')
            plt.title(f'Histogram of Distances from High-Impact Location {idx}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
    
    return binned_data

def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

def fit_binned_data_exponential(binned_data):
    fit_results = []
    bin_edges = np.arange(0, fpdata.cluster_radius, fpdata.bin_size)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    popt = None
    
    for idx, counts in enumerate(binned_data):
        try:
            # Initial guess: a = max(counts), b = 1/mean(bin_centers), c = min(counts)
            p0 = [max(counts), 1 / (bin_centers.mean() + 1e-6), min(counts)]
            popt, pcov = curve_fit(exponential_decay, bin_centers[:len(counts)], counts, p0=p0)
            fit_results.append((popt, pcov))
        except RuntimeError:
            print(f"Fit failed for zone {idx}")
            fit_results.append(None)
            
        # Enable to plot the histogram and fit
        if fpdata.plot_fitted_data:
            plt.figure(figsize=(8, 4))
            # Plot histogram
            plt.bar(bin_centers[:len(counts)], counts, width=fpdata.bin_size, color='skyblue', edgecolor='black', alpha=0.7, label='Data')
            
            if popt is not None:
                # Generate the fitted curve
                fitted_curve = exponential_decay(bin_centers[:len(counts)], *popt)
                
                # Calculate confidence intervals
                perr = np.sqrt(np.diag(pcov))  # Standard errors from covariance matrix
                lower_bound = exponential_decay(bin_centers[:len(counts)], *(popt - perr))
                upper_bound = exponential_decay(bin_centers[:len(counts)], *(popt + perr))
                
                # Plot the fit and confidence intervals
                plt.plot(bin_centers[:len(counts)], fitted_curve, color='red', label='Fit')
                plt.fill_between(bin_centers[:len(counts)], lower_bound, upper_bound, color='red', alpha=0.2, label='Confidence Interval')
                
                plt.title(f'Zone {idx}: Exponential Decay Fit')
            
            plt.xlabel('Distance (km)')
            plt.ylabel('Count')
            plt.legend()
            plt.tight_layout()
            plt.show()
    
    return fit_results

def average_fitted_parameters_with_errors(fit_results):
    a_values, b_values, c_values = [], [], []
    a_errors, b_errors, c_errors = [], [], []
    
    for result in fit_results:
        if result is not None:
            popt, pcov = result
            a_values.append(popt[0])
            b_values.append(popt[1])
            c_values.append(popt[2])
            
            perr = np.sqrt(np.diag(pcov))
            a_errors.append(perr[0])
            b_errors.append(perr[1])
            c_errors.append(perr[2])
    
    avg_a = np.mean(a_values) if a_values else None
    avg_b = np.mean(b_values) if b_values else None
    avg_c = np.mean(c_values) if c_values else None
    
    avg_a_error = np.mean(a_errors) if a_errors else None
    avg_b_error = np.mean(b_errors) if b_errors else None
    avg_c_error = np.mean(c_errors) if c_errors else None
    
    return avg_a, avg_b, avg_c, avg_a_error, avg_b_error, avg_c_error