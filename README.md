# Plots health data

I have started collecting personal health related statistics.

This repo contains scripts to visualize collected data from csv files.

Usage:

```
usage: plotter.py [-h] [--ldl LDL] [--hdl HDL] [--chol CHOL] [--trig TRIG] [--weight WEIGHT] [--bpm BPM] [--bp SYS,DIA] [--verbose] csv_file

Health plotter

positional arguments:
  csv_file         CSV file with data

options:
  -h, --help       show this help message and exit
  --ldl LDL        Column in a csv file with LDL cholesterol
  --hdl HDL        Column in a csv file with HDL cholesterol
  --chol CHOL      Column in a csv file with Total cholesterol
  --trig TRIG      Column in a csv file with Triglycerides
  --weight WEIGHT  Column in a csv file with Weight
  --bpm BPM        Column in a csv file with BPM (heart rate)
  --bp SYS,DIA     Columns in a csv file with systolic and diastolic blood pressures
  --verbose        Print head of read file
```

## Supported plots

### Lipid panel

```
./plotter.py cholesterol.csv --hdl 1 --trig 2 --chol 3 --ldl 4  --verbose
```

The tool supports plotting of total cholesterol, low-density lipoproteins, high-density lipoproteins and triglycerides.
For example:

<img src="misc/trig.png" width="256">

There are also 2 derrived ratios that you will see: LDL/HDL and Trig/HDL:

<img src="misc/trig_to_hdl.png" width="256">
