# simtel_reader

Experiments on reading simtel files and printing trigger information

##Usage:

```
$ python simtel_reader.py -h
usage: simtel_reader.py [-h] -f FILENAME [-l LIMIT] --tel TEL [TEL ...]

optional arguments:
  -h, --help           show this help message and exit
  -f FILENAME          simtelarray data file name
  -l LIMIT             Max number of events to read
  --tel TEL [TEL ...]  telescope ids

```

##Example

```
$ python simtel_reader.py -f proton/run 10001.simtel.gz --tel 37 38 -l 4

Reading file proton/run 10001.simtel.gz
Number of simulated telescopes: 38
Run ID: 10001, Event ID: 805
  Telescopes ( 2) for which we have data: [18 26]
  teltrg_time (ns):                       [4.48 0.00]
Run ID: 10001, Event ID: 807
  Telescopes ( 8) for which we have data: [ 9 13 17 25 33 36 37 38]
  teltrg_time (ns):                       [86.84 0.00 98.94 114.32 141.07 17.18 46.14 34.08]
Run ID: 10001, Event ID: 815
  Telescopes ( 6) for which we have data: [ 9 17 25 33 37 38]
  teltrg_time (ns):                       [54.07 61.09 72.27 81.55 16.14 0.00]
Run ID: 10001, Event ID: 1414
  Telescopes ( 2) for which we have data: [20 28]
  teltrg_time (ns):                       [8.80 0.00]

Read 4 events, of which triggered by tel 37: 2
Read 4 events, of which triggered by tel 38: 2


```
