# Global City Population Visualization

A geospatial data analysis and visualization project that maps the global distribution of cities and their recorded populations using Python and the `geoplotlib` library.

## Research Question
How are the world's cities distributed geographically, and what does the distribution of large cities (population > 100,000) reveal about regional urbanization patterns?

## Dataset
- **Source:** `world_cities_pop.csv` — a world cities database (derived from the GeoNames dataset), bundled with the `geoplotlib` Python package.
- **Content:** ~3.17 million city records with columns: `Country`, `City`, `AccentCity`, `Region`, `Population`, `Latitude`, `Longitude`.
- **License / terms:** Distributed as part of the geoplotlib sample datasets; GeoNames data is publicly available for free use. See the [geoplotlib repository](https://github.com/andrea-cuttone/geoplotlib) for details.

## Methods and Tools
- **Tools:** Python, Jupyter Notebook, pandas, numpy, geoplotlib
- **Steps:**
  1. Load `world_cities_pop.csv` and inspect its structure.
  2. Clean the data: coerce coordinates and population to numeric, drop invalid latitude/longitude rows.
  3. Aggregate the number of city records per country.
  4. Render a dot-density map of all cities (OSM HOT provider).
  5. Render a dot map for cities with a recorded population above 0.
  6. Build a Voronoi diagram for cities with population > 100,000.
  7. Build a Delaunay triangulation for Germany and Great Britain (cities > 100,000).

## Key Findings
1. The dataset holds ~3.17M city records across 234 countries — a sample, not a complete census (mean of ~13,564 records per represented country).
2. Only 3,527 records have a population above 100,000; these large cities concentrate in Europe and Asia.
3. China, Russia, Indonesia, the United States, and Iran have the most city records in this sample.
4. Germany and Great Britain form dense Delaunay networks of large cities, reflecting high urbanization.

## Limitations
- The dataset is a record-based sample rather than a complete real-world city census, so population statistics reflect the sample only.
- Map tiles (OSM HOT / CARTO) require an internet connection when rendered.

## How to Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Place `world_cities_pop.csv` beside this notebook (or in a `Datasets` folder). The file is bundled with `geoplotlib` — after installation you can copy it from the package's `datasets` directory.
3. Open `mc652817_Activity8.01.ipynb` in Jupyter Notebook and run all cells.
