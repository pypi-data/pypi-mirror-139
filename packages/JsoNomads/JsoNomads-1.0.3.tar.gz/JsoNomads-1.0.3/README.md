# JsoNomads

It is a module to download and convert NOMADS data from NOAA to JSON. 
Also provides a command line tool.

# Installation

pip3 install jsonomads

or if you install it from source:

pip3 install .

# Usage

usage: jsonomads [-h] [-i [GRIBFILE]] [-o [JSONFILE]] [-k] [-t [DATATYPE]]
                 [-p] [-r [N]] [-I [N]] [--leftlon [N]] [--rightlon [N]]
                 [--toplat [N]] [--bottomlat [N]] [--res [RESOLUTION]]
                 [--tol [LEVELTYPE]] [--level [N]] [--nou] [--nov]

Download NOMADS data from NOAA and convert the grib file to JSON

optional arguments:
  -h, --help            show this help message and exit
  -i [GRIBFILE], --input [GRIBFILE]
                        Input GRIB file. Download fresh file from NOAA if not
                        specified.
  -o [JSONFILE], --output [JSONFILE]
                        Output JSON file
  -k, --keep            Keep grib file
  -t [DATATYPE], --type [DATATYPE]
                        Data type. (Default: wind)

JSON parameters:
  -p, --print           Just print json data to stdout
  -r [N], --round [N]   Round to N decimals
  -I [N], --indent [N]  Indentation

Wind parameters:
  Optional wind parameters

  --leftlon [N]         Left longitude. (Default: 0)
  --rightlon [N]        Right longitude. (Default: 360)
  --toplat [N]          Top latitude. (Default: 90)
  --bottomlat [N]       Bottom latitude. (Default: -90)
  --res [RESOLUTION]    Resolution. (Default: 1p00)
  --tol [LEVELTYPE]     Type of level. (Default: heightAboveGround)
  --level [N]           Level. (Default: 10)
  --nou                 No U-component
  --nov                 No V-component
