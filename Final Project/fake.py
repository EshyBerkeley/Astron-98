# This file contains analysis on fake data to test if the model would work

import numpy as np
import pandas as pd
import fpanalysis

# Generates fake data that follows an exponential decay based on distance to a center point
def generate_multi_center_decay_data(num_centers=5, row_range=(500, 1500), radius_km=250):
    centers = []
    latitudes = []
    longitudes = []
    ids = []
    current_id = 0

    for center_idx in range(num_centers):
        # Randomly pick the number of rows for this center
        num_rows = np.random.randint(row_range[0], row_range[1] + 1)

        # Randomly select a center point (latitude and longitude)
        center_lat = np.random.uniform(-90, 90)
        center_lon = np.random.uniform(-90, 90)
        centers.append([center_lat, center_lon])

        # Generate random offsets within a bounding box around the center
        lat_offsets = np.random.uniform(-2.25, 2.25, num_rows)  # ~250km in degrees latitude
        lon_offsets = np.random.uniform(-2.25, 2.25, num_rows)  # ~250km in degrees longitude

        # Calculate approximate distances and apply exponential decay
        distances = np.sqrt(lat_offsets**2 + (lon_offsets * np.cos(np.radians(center_lat)))**2) * 111  # km
        decay_probs = np.exp(-distances / radius_km)
        mask = np.random.uniform(0, 1, num_rows) < decay_probs

        # Apply the mask to filter points
        valid_latitudes = (center_lat + lat_offsets)[mask]
        valid_longitudes = (center_lon + lon_offsets)[mask]

        # Ensure we have exactly `num_rows` points for this center
        if len(valid_latitudes) < num_rows:
            extra_needed = num_rows - len(valid_latitudes)
            extra_lat = np.random.choice(valid_latitudes, extra_needed, replace=True)
            extra_lon = np.random.choice(valid_longitudes, extra_needed, replace=True)
            valid_latitudes = np.concatenate([valid_latitudes, extra_lat])
            valid_longitudes = np.concatenate([valid_longitudes, extra_lon])

        # Append data for this center
        latitudes.extend(valid_latitudes[:num_rows])
        longitudes.extend(valid_longitudes[:num_rows])
        ids.extend(range(current_id, current_id + num_rows))
        current_id += num_rows

    # Combine into a single DataFrame
    data = pd.DataFrame({
        "id": ids,
        "latitude": latitudes,
        "longitude": longitudes
    })

    return data, centers

decay_data, center_list = generate_multi_center_decay_data()
binned_data = fpanalysis.populate_binned_data(decay_data, center_list)
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