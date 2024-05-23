# COVID-19 Plotting

This project contains a script for analyzing COVID-19 death data specifically for California, with a focus on comparing a county (hardcoded to Los Angeles) with the overall state data. The script retrieves data from a GitHub repository, processes it, and generates visualizations to display the distribution and trends of COVID-19 deaths in California.

## Files

- `covid19_california_county_plots.py`: The main script to analyze and visualize COVID-19 death data for California.
- `california.png`: An image of the map of California used in the visualization.
- `Sample_Results.docx`: A document containing sample results from the analysis.

## Description

The `covid19_california_county_plots.py` script retrieves COVID-19 death data for California from a GitHub repository, processes it to calculate total deaths per county, and generates a scatter plot showing the distribution of deaths across the state. It also generates a chart comparing daily deaths in Los Angeles County with the overall state data.

## Usage

### Prerequisites

Make sure you have the following Python libraries installed on your system:

- `pandas`
- `matplotlib`
- `numpy`
- `urllib`

You can install them using `pip`:

```sh
pip install pandas matplotlib numpy urllib
