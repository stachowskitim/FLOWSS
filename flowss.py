#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#    flowss.py

#    A program to calculate the flow rate of a solution SAXS sample necessary
#    to achieve a certain delivered dose.
#
#
#    Tested using Python 3.6.5
#
#    Author: Timothy Stachowski
#    Email: <tstachowski@hwi.buffalo.edu>
#    Copyright 2018 The Research Foundation for SUNY
#
#    Additional authors:
#    Thomas Grant
#    Edward Snell
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import argparse
import numpy as np
from tabulate import tabulate


        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        #                            USER INPUT                           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

"""
    Calculates flow rate, sample volume, and time, needed to conduct experiments
    for each dose supplied in sampledoses


    Prameters
    ---------
    sampledoses : float
        List of values separated by spaces
    doserate : float
        Single value of beam dose rate in Grays / second (Gy/s)
    snr : float
        Single value of the Grays (Gy) required for accetable signal to noise.
        Many redundant frames are collected at low dose to match this value.
    voluemlimit: float
        Single value for the maximum volume allowed for the experiment

"""

CLI = argparse.ArgumentParser(prog='FLOWSS', usage='%(prog)s [options]',
                              description='Calculate sample flow rate to '
                              'deliver specific dose in solution scattering experiments.'
                              ' More information available at github.com/stachowskitim')

CLI.add_argument(
    '-a',
    '--sampledoses',
    nargs="+",
    type=float,
    default=[100, 10, 1],
    help='input space separated list of doses for sample'
)

CLI.add_argument(
    '-b',
    '--doserate',
    nargs="+",
    type=float,
    # Most defaults are from CHESS G1: Acerbo, et al. JSR 2015
    default=[2300],
    help='define dose rate in Gy/s'
)

CLI.add_argument(
    '-c',
    '--snr',
    nargs="+",
    type=float,
    default=[100],
    help='define SNR value in Gy'
)

CLI.add_argument(
    '-d',
    '--volumelimit',
    nargs="+",
    type=float,
    default=[200],
    help='define volume limit in microliters'
)

CLI.add_argument(
    '-e',
    '--beamdimensions',
    nargs="+",
    type=float,
    default=[.321, .303, 1],
    help='define beamdimensions x y followed by sample cell internal diameter z '
    ', all in millimeters'
)

CLI.add_argument(
    '-f',
    '--attenuators',
    nargs="+",
    type=float,
    default=[.1, .01],
    help='define up to two attenuator values in fraction flux attenuation (e.g. 10%% = .1)'
)

CLI.add_argument(
    '-i',
    '--filename',
    nargs='?',
    required=False,
    default=None,
    help='input text file with parameter values in alphabetical order of parameter'
)

ARGS = CLI.parse_args()

A = np.array(ARGS.sampledoses)
B = np.array(ARGS.doserate)
C = np.array(ARGS.snr)
D = np.array(ARGS.volumelimit)
E = np.array(ARGS.beamdimensions)
F = np.array(ARGS.attenuators)

if ARGS.filename is not None:
    content = []
    with open(ARGS.filename) as file:
        for line in file:
            split = [float(x) for x in line.split(' ')]
            content.append(split)

    A = np.array(content[0])
    B = np.array(content[1])
    C = np.array(content[2])
    D = np.array(content[3])
    E = np.array(content[4])
    F = np.array(content[5])

def dosetable(doselist, doserate, snr, volumelimit, beamdimensions, attenuators):



        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        #               EXPERIMENT PARAMETER DETERMINATION                #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    """

        Returns
        -------
        flowratevalues: 1D numpy array
        Array of flow rates
        timevalues: 1D numpy array
        Array of times needed to collect data
        volumevalues: 1D numpy array
        Array of sample volume needed to collect data that is equivalent to desired SNR

    """

    volumevalues = []
    timevalues = []
    flowratevalues = []
    attenuation = []
    illuminatedvolume = (beamdimensions[0]*beamdimensions[1]*beamdimensions[2])

    for sampledose in doselist:
        flowrate = doserate * illuminatedvolume / sampledose
        time = (snr * flowrate) / (doserate * illuminatedvolume)
        volume = time * flowrate
        # CHESS G1 has three attenuators, the first two are each one order of magnitude
        attenuator = 0

        if volume > volumelimit:

            attenuator = 1
            flowrate = (doserate*attenuators[0]) * illuminatedvolume / sampledose
            time = (snr * flowrate) / ((doserate * attenuators[0]) * illuminatedvolume)
            volume = time * flowrate

            if volume > volumelimit:
                attenuator = 2
                flowrate = (doserate*attenuators[1]) * illuminatedvolume / sampledose
                time = (snr * flowrate) / ((doserate* attenuators[1]) * illuminatedvolume)
                volume = time * flowrate
                flowratevalues.append(flowrate)
                timevalues.append(time)
                volumevalues.append(volume)
                attenuation.append(attenuator)

            else:
                flowratevalues.append(flowrate)
                timevalues.append(time)
                volumevalues.append(volume)
                attenuation.append(attenuator)

        else:
            flowratevalues.append(flowrate)
            timevalues.append(time)
            volumevalues.append(volume)
            attenuation.append(attenuator)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        #                    FORMATTING & TABLE OUTPUT                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    data = []
    cats = ["Sample Dose (Gy)", "Flow Rate (uL/s)",
            "Equiv. Signal Volume", "Total Time (s)", "Attenuator"]

    for i in range(len(doselist)):
        data.append((doselist[i], flowratevalues[i], volumevalues[i], timevalues[i],
                     attenuation[i]))

    dataarray = np.array(data)
    np.savetxt("dose.txt", dataarray, delimiter=" ", fmt="%.3f")

    print(tabulate(data, cats, tablefmt="grid"))

    print("Equivalent Dose for Desired SND: " + str(int(snr)) + " Gy")
    print("Volume Limit Per Injection: " + str(int(volumelimit)) + " uL")
    print("Total Sample Volume Required: "+ str(int(sum(volumevalues))) + " uL")
    print("Total Experiment Time: " + str(int(sum(timevalues))) + " seconds")


dosetable(A, B, C, D, E, F)
