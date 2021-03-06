# FLOWSS: Calculates the FLOW rate for a sample needed to achieve a certain delivered dose with Solution SAXS 

Author: Tim Stachowski | email tstachowski@hwi.buffalo.edu

## About FLOWSS

FLOWSS is a program for calculating the flow rate of a sample that is needed to deliver a specific dose in a SAXS experiment. In the age of third, and now fourth, generation synchrotron sources with high-flux beamlines, radiation damage is one of the most common impedements to collecting useful scattering data from samples in solution. Often to limit radiation damage, a sample volume, much larger than the volume that is actually illuminated at a given time, is oscillated back-and-forth across the beam path so the total dose is distributed across a larger volume. A second approach is to move the sample uni-directionally using an FPLC/HPLC, in this case the flow rate is known and constant. FLOWSS is centered on the relationship that the amount of dose that a sample recieves is proportional to the amount of time it is illuminated by the X-ray beam - or for a flowing sample, how long it takes to traverse the beam path. Once a dose rate is calculated, FLOWSS calculates how fast the sample must flow to achieve a specific delivered dose. Since FPLC/HPLC systems can achieve a wide range of flow rates, FLOWSS is a useful tool for comparing X-ray damage to biomolecules in solution versus crystalline (high doses) or solution samples to typical conditions seen in X-ray radiation therapy (low doses). 


## Requirements
FLOWSS requires that Python 3.2, and NumPy and tabulate libraries are installed. Python 3.2 is typically installed by default on Mac OS X. The NumPy and tabulate libraries can be installed through a command line interpreter using a package manager such as PIP:
```
pip install tabulate
```
and 
```
pip install numpy
```


## Usage 

From the directory where flowss.py is saved, it is run with defaults in a terminal shell:
```
python3 flowss.py
``` 
or 
```
flowss.py
```

In this case, FLOWSS uses a dose rate for the G1 beam line at the Cornell High Energy Synchrotron Source. A custom dose rate can be used (calculated perhaps from RADDOSE-3D (Bury et al., 2018) in Grays/second (Gy/s)) by specifying the -b parameter:

```
flowss.py -b 300
```

Additionally, by default FLOWSS returns experimental parameters for three different sample doses (100, 10, and 1 Gy). A space spearated list can be used by specifying the -a parameter: 

```
flowss.py -a 100 25 10 1
```

A third option specifies the minimum dose needed to achieve enough 'signal to noise' (SND) to sufficiently evaluate whatever characteristic you are interested in with SAXS. This is something that should be determined experimentally. If for instance, with a dose rate of 300 Gy/s and a 0.1 second exposure you determine the resultant scattering intensity is sufficient for your experiment, then your SND is 30 Gy. Since in a flowing experiment many redundant exposures are collected, (all things being equal) the scattering intensity from each exposure can be summed together to reach this SND value. The SND option can be specified using the -c parameter: 

```
flowss.py -c 30
```

Currently, FLOWSS only sets an upper limit for volume, which is advantageous for monitoring sample consumption. For example, faster flowing samples that receive lower doses will naturally require more sample volume to reach the required SND value. However, if an attenuator can be used to lower the sample dose instead of adjusting the flow rate, then the sample consumption can minimized - however, this relationship requires that the dose rate is also changed and is done so by FLOWSS. In general, a lower limit for sample volume will be restricted based on the sample delivery system at the beamline including the size of the FLPC loop (if) used and broadening or adhesion effects during sample delivery. An upper volume limit (in microliters) is specified with the -d parameter:

```
flowss.py -d 100
```

The illuminated volume is approximated by a retangular prism with dimensions x and y from the beam profile and z from the internal diameter of the sample cell. Illuminated volume dimensions are specified in a space separated list in units of millimeters with the -e parameter:

```
flowss.py -e .3 .2 1
```

In addition to flow rate, attenuators offer another dimension used to change the sample dose, and is most advantageous to save sample volume. However, this changes the dose rate and therefore might cause a difference in the sample response. Atteunation values (up to two) can be defined in fraction of flux attenuated (e.g. 10% transmission should be input as 0.1) and is specified with the -f parameter: 

```
flows.py -f .1 .1
```

Since most likely the user will want to define all of these parameters so that the dose is most accurately approximated, a final parameter `-i` can be used *alone* to input all the definitions in a plain text file. Each parameter, in alphabetical order according to the parameter key, should be placed on its own line with space seperated values so that the final file should look like (without comments):

```
100 99 88 77 55 42 31 22 31 16 5 1  # -a, list of doses for sample
2300                                # -b, dose rate
100                                 # -c, SND
200                                 # -d, volume limit
0.2 0.4 1.0                         # -e, illuminated volume dimensions
0.1 .01                             # -f, attenuator values
```

and the input:

```
flowss.py -i input.txt
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
flowss.py -a 100 25 10 1 -b 300 -c 30 -d 100 >> dosetable.txt
```


