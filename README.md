# Facebook-Movement-Map-Analysis


Dependencies:
matplotlib, seaborn, pandas, networkx

Required files:
RKI case number files, Facebook population/mobility data sets

Overview:
construction.py: functions for building data structures from data files (Facebook, RKI .csvs)

analytics.py:    functions to perform analysis on data structures (e.g. node, edge, graph filters)

model.py:        functions for SIR-simulation (ignore, paused because of problems with mobility data set, messy)

plot.py:         methods for data visualization(KML, graphs)

utility.py:      helper methods (file and path handling)

settings.py:     required: path to RKI files, all other paths optional

auto.py:         semi-automated keyboard for downloading Facebook data sets (~5-10~ min for main data sets)
