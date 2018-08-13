# waze-predict
Predictive modeling for City of LA's waze data

###

`road_squares.py`: uses `la_streets.csv` to generate a grid covering all streets in LA County in  `data/`. This can then be used to bucket the jams in a trainable way.

Usage: `python road_squares.py`

###

`pull_data.py`: pulls data from the database into usable csvs (into `data/jams.csv`, specifically).

Usage: `python pull_data.py user password database -H host -p port`
