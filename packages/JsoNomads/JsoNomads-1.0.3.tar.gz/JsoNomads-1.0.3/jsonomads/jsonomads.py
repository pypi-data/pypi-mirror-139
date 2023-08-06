#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
#                                                        #
#   ██████╗ ██████╗  █████╗ ██╗  ██╗███████╗███╗   ██╗   #
#   ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝████╗  ██║   #
#   ██║  ██║██████╔╝███████║█████╔╝ █████╗  ██╔██╗ ██║   #
#   ██║  ██║██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██║╚██╗██║   #
#   ██████╔╝██║  ██║██║  ██║██║  ██╗███████╗██║ ╚████║   #
#   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   #
#                                                        #
#                Copyright © 2022 Draken TT              #
#                   https://draken.ee                    #
#                                                        #
##########################################################

import os
import json
import numpy as np
import datetime
import xarray as xr
import argparse

class Wind():
    def __init__(self, *args, ds=None, **kwargs):
        self.grib_info = ds.attrs
        self.create_header(ds)
        
    def to_dict(self):
        return {"header": self.header, "data": self.data}

    def create_header(self, ds=None):
        lon1 = float(ds.variables['longitude'][0])
        lon2 = float(ds.variables['longitude'][-1])
        lat1 = float(ds.variables['latitude'][0])
        lat2 = float(ds.variables['latitude'][-1])
        nx = ds.dims['longitude']
        ny = ds.dims['latitude']
        dx = (lon2 - lon1 + 1) / nx
        dy = abs(round((lat2 - lat1 + 1) / ny, 1))
        refTime = str(ds.coords["time"].data).split('.')[0]+'.000Z'

        self.header = {
            "discipline":0,
            "disciplineName":"Meteorological products",
            "gribEdition": self.grib_info['GRIB_edition'],
            "center": self.grib_info['GRIB_centre'],
            "centerName": self.grib_info['GRIB_centreDescription'],
            "subcenter":self.grib_info['GRIB_subCentre'],
            "refTime":refTime,
            "significanceOfRT":1,
            "significanceOfRTName":"Start of forecast",
            "productStatus":0,
            "productStatusName":"Operational products",
            "productType":1,
            "productTypeName":"Forecast products",
            "productDefinitionTemplate":0,
            "productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time",
            "parameterCategory": 2,
            "parameterCategoryName":"Momentum",
            "parameterUnit": self.grib_info['Conventions'],
            "genProcessType":2,
            "genProcessTypeName":"Forecast",
            "forecastTime": 0,
            "surface1Type":103,
            "surface1TypeName":"Specified height level above ground",
            "surface1Value":10.0,
            "surface2Type":255,
            "surface2TypeName":"Missing",
            "surface2Value":0.0,
            "gridDefinitionTemplate":0,
            "gridDefinitionTemplateName":"Latitude_Longitude",
            "shape":6,
            "shapeName":"Earth spherical with radius of 6,371,229.0 m",
            "gridUnits":"degrees",
            "resolution":48,
            "winds":"true",
            "scanMode":0,
            "nx": nx,
            "ny": ny,
            "basicAngle": 0,
            "la1": lat1,
            "lo1": lon1,
            "lo2": lon2,
            "la2": lat2,
            "dx": dx,
            "dy": dy,
          }
        


class UWind(Wind):
    def __init__(self, *args, ds=None, **kwargs):
        super().__init__(self, *args, ds=ds, **kwargs)
        self.header["parameterNumberName"] = "U-component_of_wind"
        self.header["parameterNumber"] = 2
        self.data = np.flipud(ds.variables['u10'])[::-1].flatten().tolist()
        self.header["numberOfPoints"] = len(self.data)

class VWind(Wind):
    def __init__(self, *args, ds=None, **kwargs):
        super().__init__(*args, ds=ds, **kwargs)
        self.header["parameterNumberName"] = "V-component_of_wind"
        self.header["parameterNumber"] = 3
        self.data = np.flipud(ds.variables['v10'])[::-1].flatten().tolist()
        self.header["numberOfPoints"] = len(self.data)


class JsoNomads():
    def __init__(self, gribfile=None, jsonfile=None, round_n=5, indent=4, to_stdout=False):
        self.gribfile = gribfile
        self.jsonfile = jsonfile
        self.round_n = round_n
        self.indent = indent
        self.to_stdout = to_stdout
    
    def round_floats(self, o):
        if isinstance(o, float): return round(o, self.round_n)
        if isinstance(o, dict): return {k: self.round_floats(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [self.round_floats(x) for x in o]
        return o

    def data_to_json(self, data, file_name):
        if self.to_stdout:
            print(json.dumps(self.round_floats(data), indent=self.indent))
        else:
            with open(file_name, 'w') as f:
                return json.dump(self.round_floats(data), f, indent=self.indent)

    def get_winds(self, ds=None, u=True, v=True):
        data = []
        if u:
            data.append(UWind(ds=ds).to_dict()) 
        if v:
            data.append(VWind(ds=ds).to_dict())
        return data
        
    def winds_to_json(self, all_lev='on', all_var='on', leftlon=0, rightlon=360, toplat=90, bottomlat=-90, res='1p00', 
                      type_of_level='heightAboveGround', level=10, keep_grib=False, u=True, v=True):
        if self.gribfile:
            ds = xr.open_dataset(self.gribfile, engine='cfgrib', backend_kwargs={'indexpath': '', 'filter_by_keys': {'typeOfLevel':type_of_level, 'level': level}})
            data = self.get_winds(ds=ds, u=u, v=v)
        else:
            current_time = datetime.datetime.utcnow()-datetime.timedelta(hours=5)
            YYYYMMDD = current_time.strftime("%Y%m%d")
            HH = '{0:02}'.format((current_time.hour//6)*6)
            url = f'''https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_{res}.pl?file=gfs.t{HH}z.pgrb2.{res}.f000&all_lev={all_lev}&all_var={all_var}&\
leftlon={leftlon}&rightlon={rightlon}&toplat={toplat}&bottomlat={bottomlat}&dir=%2Fgfs.{YYYYMMDD}%2F{HH}%2Fatmos'''
            tempfile = f'/tmp/{YYYYMMDD}{HH}.grib'
            os.system(f'wget --show-progress -O{tempfile} "{url}"')
            ds = xr.open_dataset(tempfile, engine='cfgrib', backend_kwargs={'indexpath': '', 'filter_by_keys': {'typeOfLevel':type_of_level, 'level': level}})
            data = self.get_winds(ds=ds, u=u, v=v)
            if not keep_grib:
                os.system(f'rm {tempfile}')
        if not self.jsonfile:
            self.jsonfile = f'{str(ds.coords["time"].data).split(".")[0]}.json'
        self.data_to_json(data, self.jsonfile)

def main(*a, **kw):
    parser = argparse.ArgumentParser(prog="jsonomads", description='Download nomads data from NOAA and convert the grib file to JSON')
    parser.add_argument('-i', '--input', nargs='?', type=str, metavar="GRIBFILE", help='Input GRIB file. Download fresh file from NOAA if not specified.')
    parser.add_argument('-o', '--output', nargs='?', type=str,  metavar="JSONFILE", help='Output JSON file')
    parser.add_argument('-k', '--keep', action='store_true', help='Keep grib file')
    parser.add_argument('-t', '--type', nargs='?', metavar="DATATYPE", default="wind", help='Data type. (Default: wind)')
    json_group = parser.add_argument_group('JSON parameters')
    json_group.add_argument('-p', '--print', action='store_true', help='Just print json data to stdout')
    json_group.add_argument('-r', '--round', nargs='?', type=int, default=5, metavar="N", help='Round to N decimals')
    json_group.add_argument('-I', '--indent', nargs='?', type=int, default=4, metavar="N", help='Indentation')
    wind_group = parser.add_argument_group('Wind parameters', 'Optional wind parameters')
    wind_group.add_argument('--leftlon', nargs='?', type=int, default=0, metavar="N", help='Left longitude. (Default: 0)')
    wind_group.add_argument('--rightlon', nargs='?', type=int, default=360, metavar="N", help='Right longitude. (Default: 360)')
    wind_group.add_argument('--toplat', nargs='?', type=int, default=90, metavar="N", help='Top latitude. (Default: 90)')
    wind_group.add_argument('--bottomlat', nargs='?', type=int, default=-90, metavar="N", help='Bottom latitude. (Default: -90)')
    wind_group.add_argument('--res', nargs='?', type=str, default="1p00", metavar="RESOLUTION", help='Resolution. (Default: 1p00)')
    wind_group.add_argument('--tol', nargs='?', type=str, default='heightAboveGround', metavar="LEVELTYPE", help='Type of level. (Default: heightAboveGround)')
    wind_group.add_argument('--level', nargs='?', type=int, default=10, metavar="N", help='Level. (Default: 10)')
    wind_group.add_argument('--nou', action='store_true', help='No U-component')
    wind_group.add_argument('--nov', action='store_true', help='No V-component')
    args = parser.parse_args()

    jn = JsoNomads(gribfile=args.input, jsonfile=args.output, to_stdout=args.print, indent=args.indent, round_n=args.round)
    if args.type.lower() == "wind":
        jn.winds_to_json(keep_grib=args.keep, u=not args.nou, v=not args.nov, leftlon=args.leftlon, rightlon=args.rightlon, toplat=args.toplat, bottomlat=args.bottomlat,
                         res=args.res, type_of_level=args.tol, level=args.level)

if __name__ == "__main__":
    main()
