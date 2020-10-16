# Antarctic ozone loss saturation

This repository contains the analysis codes for the paper [Emergence of ozone recovery evidenced by reduction in the occurrence of Antarctic ozone loss saturation](https://www.nature.com/articles/s41612-018-0052-6).

## Data

1. Stratospheric Ozone profiles from ozonesonde ([NDACC](ndaccdemo.org) and [WOUDC](https://www.woudc.org/data/explore.php?lang=en)).

2. [Stratospheric Aerosol and Gas Experiment II  (SAGE II)](https://data.giss.nasa.gov/sageii/)

3. [Aura Microwave Limb Sounder (MLS) ](https://mls.jpl.nasa.gov/)

4. [ERA Interim Meteorological Reanalyses ]()

## Workflow

1. Reading and conversion of ozonesonde measurements to isentropic coordinates.

2. Reading, conversion and correction of satellite data using [reported correction factors](https://mls.jpl.nasa.gov/data/v4-2_data_quality_document.pdf).

3. Determination of [equivalent latitude](https://en.wikipedia.org/wiki/Equivalent_latitude) and [polar vortex edge using Nash Criteria](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/96JD00066). 

4. Determination of all data points lying inside the vortex edge.

5. Calculate the daily fraction of data points for which ozone concentration is less than the loss saturation criteria (0.1 ppmv). 

## Notebooks should be run in the following order:

1. [Polar vortex edge estimation using Nash Criteria]()
2. [Ozonesonde data processing]()


