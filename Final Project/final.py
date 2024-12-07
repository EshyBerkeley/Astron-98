# Finding an equation using the real data

import pandas as pd
import os
from keplergl import KeplerGl
import fpdata
import fpanalysis

script_dir = os.path.dirname(__file__)

data = pd.read_csv(os.path.join(script_dir, "data.csv"))

def preprocess_data(data):
    print(f"Initially contained {data.shape[0]} rows.")

    # Name, recclass, and fall are irrelevant; Geolocation is already provided by reclat and reclong
    data = data[['id', 'nametype', 'year', 'reclat', 'reclong']]
    data.columns = ['id', 'nametype', 'year', 'latitude', 'longitude']
    # Ensure nametype is valid (I don't know what this means but I don't trust it)
    data = data[data['nametype'] == 'Valid']
    # 1970 onwards we have collected good impact data, I do not trust prior data
    data = data[data['year'] >= 1970]
    # Ensure rows have valid latitude and longitude
    data = data.dropna(subset=['latitude', 'longitude'])

    print(f"Filtered data contains {data.shape[0]} rows.")
    return data

# Functions to plot input data using Kepler.gl
def input_data_kepler_point_geoplot(data):
    map_ = KeplerGl(height=600)
    map_.add_data(data, name="Meteorite Impacts")
    map_.save_to_html(file_name=os.path.join(script_dir, "output_plots", "input_data_kepler_point_geoplot.html"))

def input_data_kepler_heatmap_geoplot(data):
    map_ = KeplerGl(height=600)
    map_.add_data(data, name="Meteorite Impacts")
    map_.config = fpdata.keplerHeatmapConfig
    map_.save_to_html(file_name=os.path.join(script_dir, "output_plots", "input_data_kepler_heatmap_geoplot.html"))

filtered_data = preprocess_data(data)

# Plot initial data for analysis (guessing initial parameters for curve fitting)
if fpdata.plot_input_data:
    input_data_kepler_point_geoplot(filtered_data)
    input_data_kepler_heatmap_geoplot(filtered_data)
    
binned_data = fpanalysis.populate_binned_data(filtered_data, fpdata.high_impact_zones)
fit_results = fpanalysis.fit_binned_data_exponential(binned_data)
results = fpanalysis.average_fitted_parameters_with_errors(fit_results)

avg_a, avg_b, avg_c, avg_a_error, avg_b_error, avg_c_error = results
print("Average Fitted Parameters with Errors:")
if avg_a is not None:
    print(f"  a: {avg_a:.2f} ± {avg_a_error:.2f}")
if avg_b is not None:
    print(f"  b: {avg_b:.4f} ± {avg_b_error:.4f}")
if avg_c is not None:
    print(f"  c: {avg_c:.2f} ± {avg_c_error:.2f}")