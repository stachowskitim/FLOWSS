# FLOWSS: Calculates the FLOW rate for a sample needed to achieve a certain delivered dose with Solution SAXS 

Author: Tim Stachowski | email tstachowski@hwi.buffalo.edu

## Requirements
FLOWSS requires that Python 3.2, and NumPy and tabulate libraries are installed. Python 3.2 is typically insalled by default on MAC OS X. The NumPy and tabulate libraries can be installed through a command line interpreter using a package manager such as PIP:
```
pip install tabulate
```
and 
```
pip install numpy
```


## Usage 

From the directory where FLOWSS.py is saved, it can be run with defaults in a terminal shell:
```
python3 flowss.py
``` 
or 
```
flowss.py
```

In this case, FLOWSS uses a dose rate for the G1 beam line at the Cornell High Energy Synchrotron Source. A custom dose rate can be used (calculated perhaps from RADDOSE-3D (Bury 2018) in Grays/second (Gy/s)) by specifying the -b parameter:

```
flowss.py -b 300
```

Additionally, by default FLOWSS returns experimental parameters for three different sample doses (100, 10, and 1 Gy). A space spearated list can be used by specifying the -a parameter: 

```
flowss.py -a 100 25 10 1
```

A third option specifies the minimum dose needed to achieve enough 'signal to noise' (SND) to sufficiently evaluate whatever characteristic you are interested in with SAXS. This is something that should be determined experimentally. If for instance, with a dose rate of 300 Gy/s and a 0.1 second exposure you determine that is sufficient for your experiment, then your SNR is 30 Gy. Since in a flowing experiment many redundant exposures are collected, (all things being equal) the scattering intensity from each exposure can be summed together to reach this SND value. The SND option can be specified using the -c parameter: 

```
flowss.py -c 30
```

The last option regards specifying the volume limit. Currently, FLOWSS only sets an upper limit for volume, which is advantageous for monitoring sample consumption. For example, faster flowing samples that receive lower doses will naturally require more sample volume to reach the required SND value. However, if an attenuator can be used to lower the sample dose instead of adjusting the flow rate, then the sample consumption can minimized - however, this relationship requires that the dose rate is also changed. This relationship is apparent in the output of FLOWSS. In general, a lower limit for sample volume will be restricted based on the sample delivery system at the beamline including the size of the FLPC loop (if) used and broadening or adhesion effects during sample delivery. A (upper) volume limit (in microliters) is specified with the -d parameter:

```
flowss.py -d 100
```

## Results
With an input of:
```
flowss.py -a 100 25 10 1 -b 300 -c 30 -d 100 
```
The output will be printed to the screen:
```
+--------------------+--------------------+------------------------+------------------+--------------+
|   Sample Dose (Gy) |   Flow Rate (uL/s) |   Equiv. Signal Volume |   Total Time (s) |   Attenuator |
+====================+====================+========================+==================+==============+
|                100 |              0.375 |                 0.1125 |              0.3 |            0 |
+--------------------+--------------------+------------------------+------------------+--------------+
|                 25 |              1.5   |                 1.8    |              1.2 |            0 |
+--------------------+--------------------+------------------------+------------------+--------------+
|                 10 |              3.75  |                11.25   |              3   |            0 |
+--------------------+--------------------+------------------------+------------------+--------------+
|                  1 |              0.375 |                11.25   |             30   |            2 |
+--------------------+--------------------+------------------------+------------------+--------------+
Equivalent Dose for Desired SNR: 30 Gy
Volume Limit Per Injection: 100 uL
Total Sample Volume Required: 24 uL
Total Experiment Time: 34 seconds
```
In addition to the parameters calculated for each individual experiment, the program also calculates the total combined exposure time and the total volume needed to conduct all experiments in the table. For convienence, the five columns of values are also saved as space separated values to a text file 'dose.txt' in the current working directory, but the formatted table can easily be saved with:

```
flowss.py -a 1000 100 50 1 -b 100 -c 1000 -d 100 >> dosetable.txt
```


