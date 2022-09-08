#!/usr/bin/env python3

import csv
from datetime import datetime
import errno
import getopt
import hashlib
import json
import logging
import os
import pathlib
import socket
import subprocess
import sys
import tempfile
from validate import Validate

class GadmNames:
    '''GADM Location Names Extractor (gadm_names)'''
    __instance = None

    def __init__(self, argv):
        ''' Virtually private constructor. '''
        if GadmNames.__instance != None:
            raise Exception('This class is a singleton!')

        logging.captureWarnings(True)
        self.config = self.options(argv)
        try:
            pathlib.Path(os.path.dirname(self.config['log-file'])).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        logging.basicConfig(filename=self.config['log-file'],
                            encoding=self.config['logging']['encoding'],
                            style=self.config['logging']['style'],
                            format=self.config['logging']['format'],
                            datefmt=self.config['logging']['datefmt'],
                            filemode=self.config['logging']['filemode'],
                            level=getattr(logging, self.config['log-level'].upper(), getattr(logging, 'DEBUG')))
        self.execute()


    def copyright(self):
        return '''
GADM Location Names Extractor (gadm_names)

Copyright (C) 2022 Marie Selby Botanical Gardens

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


    def country_config(self):
        with open(self.config['system']['taskdir'] + '/countries.csv') as country_config:
            reader = csv.reader(country_config)
            result = { r[0]:{ 'iso_3': r[0], 'country': r[1], 'subregion': r[2], 'continent': r[3] } for r in reader}
            return result


    def default_configuration(self):
        task = 'gadm_names'
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
        idtext = task + socket.gethostname() + str(os.getpid()) + timestamp
        hasher = hashlib.sha1();
        hasher.update(idtext.encode('utf-8'))
        request_id = hasher.hexdigest()
        taskdir = os.path.dirname(os.path.realpath(sys.argv[0]))
        taskdotdir = os.path.expanduser(f'{pathlib.Path.home()}/.gqc')
        result = {
                    'input-file': '/dev/stdin',
                    'first-line-is-header': True,
                    'log-file': f'{taskdotdir}/log/{timestamp}.log',
                    'log-level': 'DEBUG',
                    'logging' : {
                        'encoding': 'utf-8',
                        'datefmt': '%Y%m%dT%H%M%S',
                        'style': '%',
                        'format': '%(asctime)s.%(msecs)d gqc:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s',
                        'filemode': 'a'
                    },
                    'output-file': '/dev/stdout',
                    'system': {
                        'argv': sys.argv,
                        'command': subprocess.list2cmdline([sys.executable] + sys.argv),
                        'prg': os.path.realpath(sys.argv[0]),
                        'request_id': request_id,
                        'task': task,
                        'taskdir': taskdir,
                        'taskdotdir': taskdotdir,
                        'tmpdir': tempfile.mkdtemp(prefix='org.selby.botany.gqc.'),
                        'working-directory': os.getcwd(),
                    }
                }
        return result


    def execute(self):
        countries = self.country_config()
        output_columns = ['iso_3', 'continent', 'subregion', 'country', 'pd1', 'pd2', 'pd3', 'pd4', 'pd5']
        selected_properties = {
                                'GID_0': 'iso_3',
                                'COUNTRY': 'country',
                                'NAME_1': 'pd1',
                                'NAME_2': 'pd2',
                                'NAME_3': 'pd3',
                                'NAME_4': 'pd4',
                                'NAME_5': 'pd5',
                              }
        with open(self.config['output-file'], 'w', newline='') as csv_output:
            writer = csv.writer(csv_output)
            with open(self.config['input-file'], 'r') as json_input:
                try:
                    gadm = json.load(json_input)
                    row_number = 0
                    for feature in gadm['features']:
                        if ((row_number == 0) and self.config['first-line-is-header']):
                            # header row
                            writer.writerow(output_columns)
                        row_number += 1
                        properties = feature['properties']
                        '''
                        Examples:
                        json = {
                            'GID_0': 'AFG',
                            'COUNTRY': 'Afghanistan',
                            'GID_1': 'AFG.34_1',
                            'NAME_1': 'Zabul',
                            'NL_NAME_1': 'NA',
                            'GID_2': 'AFG.34.8_1',
                            'NAME_2': 'Shinkay',
                            'VARNAME_2': 'NA',
                            'NL_NAME_2': 'NA',
                            'TYPE_2': 'Wuleswali',
                            'ENGTYPE_2': 'District',
                            'CC_2': 'NA',
                            'HASC_2': 'AF.ZB.SK'
                        }

                        {
                            'GID_0': 'FRA',
                            'COUNTRY': 'France',
                            'GID_1': 'FRA.13_1',
                            'NAME_1': "Provence-Alpes-Côted'Azur",
                            'GID_2': 'FRA.13.6_1',
                            'NAME_2': 'Vaucluse',
                            'GID_3': 'FRA.13.6.3_1',
                            'NAME_3': 'Carpentras',
                            'GID_4': 'FRA.13.6.3.9_1',
                            'NAME_4': 'Vaison-la-Romaine',
                            'GID_5': 'FRA.13.6.3.9.4_1',
                            'NAME_5': 'Faucon',
                            'TYPE_5': 'Communesimple',
                            'ENGTYPE_5': 'Commune',
                            'CC_5': ''
                        }

                        '''
                        if properties['GID_0'] in countries:
                            names = { k:'' for k in output_columns }
                            names |= countries[properties['GID_0']] 
                            names |= { v:properties[k] for (k,v) in selected_properties.items() if k in properties }
                            result = [ names[k] for k in output_columns ]
                            logging.debug(f'selected[{row_number}]: {json.dumps(result)}')
                            writer.writerow(result)
                except json.decoder.JSONDecodeError:
                    pass


    @classmethod
    def instance(cls, argv):
        if not cls.__instance:
            cls.__instance = GadmNames(argv)
        return cls.__instance


    def options(self, argv):
        assert type(argv) == list, f'Need argv to be list: found [{type(argv)}]{argv}'
        result = self.default_configuration()
        try:
            opts, _args = getopt.getopt(argv, 'fhi:L:l:no:', [
                                             'copyright',
                                             'first-line-is-header',
                                             'header',
                                             'help',
                                             'input=',
                                             'log-file=',
                                             'log-level=',
                                             'noheader',
                                             'no-header'
                                             'output='])
            for opt, arg in opts:
                if opt in ['--copyright']:
                    print(self.copyright())
                    sys.exit()
                elif opt in ['-f', '--header', '--first-line-is-header']:
                    result[Config.SECTION_GQC]['first-line-is-header'] = True
                elif opt in ['-h', '--help']:
                    print(self.usage())
                    sys.exit()
                elif opt in ['-i', '--input', '--input-file']:
                    path = os.path.realpath(arg)
                    if not Validate.file_readable(path): raise ValueError(f'Can not read input file: {path}')
                    result['input-file'] = path
                elif opt in ['-L', '--log-file']:
                    path = os.path.realpath(arg)
                    if not Validate.file_writable(path): raise ValueError(f'Can not write to log file: {path}')
                    result['log-file'] = path
                elif opt in ['-l', '--log-level']:
                    l = getattr(logging, arg.upper(), None)
                    if not isinstance(l, int): raise ValueError(f'Invalid log level: {arg}')
                    result['log-level'] = arg
                elif opt in ['-n', '--noheader', '--no-header']:
                    result[Config.SECTION_GQC]['first-line-is-header'] = False
                elif opt in ['-o', '--output', '--output-file']:
                    path = os.path.realpath(arg)
                    if not Validate.file_writable(path): raise ValueError(f'Can not write to output file: {path}')
                    result['output-file'] = path
                else:
                    assert False, f'unhandled option: {opt}'
        except getopt.GetoptError as exception:
            logging.error(exception)
            print(self.usage())
            sys.exit(2)
        logging.debug(f'options: {result}')
        return result


    def usage(self):
        defaults = self.default_configuration()
        return f'''
Usage: gadm_names [OPTION]...

A tool for extracting location tuples from a GADM GeoJson file..

The input file is in GeoJson. Input is read from {defaults['input-file']}
unless the --input option is given.

The output file is CSV file with level 1 (Country), 2 (state), and 3 (county) (actual political
divisions vary be country. Output is written to  {defaults['output-file']}
unless the --output option is given.


      --copyright              Display the copyright and exit
  -f, --first-line-is-header   Treat the first row of the input file as a header -- the
                               second line of the input file is the first record
                               processed.
      --header
  -h, --help                   Display this help and exit
  -i, --input file             Input file; defaults to {defaults['input-file']}
  -L, --log-file file          The log file; defaults to "{defaults['log-file']}"
  -l, --log-level              Sets the lowest severity level of log messages to
                               show; one of DEBUG, INFO, WARN, ERROR, FATAL or QUIET;
                               defaults to {defaults['log-level']}
  -n, --noheader, --no-header  Treat the first row of the input file as data -- not as a header
  -o, --output file            Output file; defaults to {defaults['output-file']}
      --                       Terminates the list of options
'''


if __name__ == '__main__':
    try:
        sys.exit(GadmNames.instance(sys.argv[1:]).execute())
    except KeyboardInterrupt as _:
        pass
