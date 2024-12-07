# Pretty much just configuration variables

# Kepler does point-plot by default, this config needs to be specified for heatmaps
keplerHeatmapConfig = {
        "version": "v1",
        "config": {
            "visState": {
                "filters": [],
                "layers": [
                    {
                        "id": "heatmap-layer",
                        "type": "heatmap",
                        "config": {
                            "dataId": "Meteorite Impacts",
                            "label": "Meteorite Impact Heatmap",
                            "color": [255, 0, 0],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.8,
                                "radius": 50,
                                "intensity": 1
                            }
                        }
                    }
                ],
                "interactionConfig": {
                    "tooltip": {
                        "fieldsToShow": {
                            "Meteorite Impacts": [
                                "id", "nametype", "mass", "year"
                            ]
                        }
                    }
                }
            }
        }
    }

# Config variables for convenience
plot_input_data = True
plot_input_data_histograms = False
plot_fitted_data = True
cluster_radius = 500
bin_size = 1

# Following my visual inspection, I have found the following geolocations to be in the middle of high-impact zones
high_impact_zones = [
    [40.28, -118.94],
    [35, -116.7],
    [34, -103.5],
    [-24.68, -69.76],
    [30.3, -5.83],
    [27.47, 3.7],
    [25.33, 0.46],
    [27.19, 16.28],
    [0, 35.66],
    [19, 55],
    [-30, 128]
]