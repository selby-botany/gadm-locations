# gadm-locations

Extract location names from GADM GeoJSON files (gadm-locations)

A tool for extracting the names of political divisions from the
[Database of Global Administrative Boundaries (GADM)](https://gadm.org)
available from [UC Davis](https://www.ucdavis.edu).
A good overview of the dataset is found [here](https://www.dante-project.org/datasets/gadm).
The data used is in GeoJSON format ([RFC7946](https://www.rfc-editor.org/rfc/rfc7946)) and
downloaded from <https://geodata.ucdavis.edu/gadm/gadm4.1/json/>. This utility only 
uses _feature properties_ and ignores all the boundary descriptions. The GADM properties 
are documented [here](https://gadm.org/metadata.html).

The GADM locality data varies in its precision from country to country. Most have
two or three administrative levels corresponding to "country", "state" and "county" in the US.
Some, such as France, have five administrative levels represented.

The GADM data is merged with the United Nations Statistics Division (UNSD) publication
*[Standard Country or Area Codes for Statistical Use](https://unstats.un.org/unsd/methodology/m49/)* (M49).
The data used is downloaded from  <https://unstats.un.org/unsd/methodology/m49/overview>.


## Usage

```
Usage: gadm-locations [OPTION]...

Extract location names from GADM GeoJSON files (gadm-locations).

The input file is in GeoJSON format as described above. Input is read from /dev/stdin
unless the --input option is given.

The output file is in CSV format as described below. Output is written to /dev/stdout
unless the --output option is given.


	      --copyright              Display the copyright and exit
	  -f, --first-line-is-header   The first row of the output are column headings -- the
	                               second line of the output file is the first record
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
```

## Data Formats

### Input File Format

The input file is in GeoJSON format ([RFC7946](https://www.rfc-editor.org/rfc/rfc7946)).

### Output File Format

The output file is in comma separated value (CSV) format with one record per location.
A row in output file contains these columns:

<dl>
  <dt><code>iso_3</code></dt>
  <dd>The three character country code as defined by <a href="https://www.iso.org/obp/ui/#search">ISO 3666</a>.
      The code is used to join the <a href="https://unstats.un.org/unsd/methodology/m49">USCD M4</a> data with
      the <a href="https://gadm.org">GADM</a> data.
  <dt><code>region</code></dt>
  <dd>The country's region as defined by <a href="https://unstats.un.org/unsd/methodology/m49">USCD M4</a>.</dd>
  <dt><code>subregion</code></dt>
  <dd>The continental subregion  as defined by <a href="https://unstats.un.org/unsd/methodology/m49">USCD M4</a>.</dd>
  <dt><code>region</code></dt>
  <dd>The country's intermediate region as defined by <a href="https://unstats.un.org/unsd/methodology/m49">USCD M4</a>.</dd>
  <dt><code>country</code></dt>
  <dd>The location's country as given by <a href="https://gadm.org">GADM</a> feature property <code>COUNTRY</code>.</dd>
  <dt><code>pd1</code></dt>
  <dd>The location's 'political division level 1' as given by <a href="https://gadm.org">GADM</a> feature property <code>NAME_1</code>.
      This is typically the state, province or territory level political division.</dd>
  <dt><code>pd2</code></dt>
  <dd>The location's 'political division level 2' as given by <a href="https://gadm.org">GADM</a> feature property <code>NAME_2</code>.
      This is typically the county or parish level.</dd>
  <dt><code>pd3</code></dt>
  <dd>The location's 'political division level 3' as given by <a href="https://gadm.org">GADM</a> feature property <code>NAME_3</code>.
      This is the city level.</dd>
  <dt><code>pd4</code></dt>
  <dd>The location's 'political division level 4' as given by <a href="https://gadm.org">GADM</a> feature property <code>NAME_4</code>.
      This is the suburb level.</dd>
  <dt><code>pd5</code></dt>
  <dd>The location's 'political division level 5' as given by <a href="https://gadm.org">GADM</a> feature property <code>NAME_5</code>. This is the neighborhood level.</dd>
</dl>

## Release History

* 1.0.0
    * Initial release

## Meta

Copyright © 2021  Marie Selby Botanical Gardens «[botany@selby.org](mailto:botany@selby.org)»

[GitHub: selby-botany/gadm-locations](https://github.com/selby-botany/gadm-locations)

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
