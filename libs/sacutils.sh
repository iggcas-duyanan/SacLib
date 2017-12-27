#!/usr/bin/env python2.7

# =============================================================================
#
# Copyright (C) 2010-2017 GEM Foundation
#
# This file is part of the OpenQuake's Site Response Toolkit (OQ-SRTK)
#
# SacLib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# SacLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# Author: Valerio Poggi
#
# =============================================================================

import sys
import sacio
import sacutils

# =============================================================================
# Main

def main(argv):
    """
    """
    #--------------------------------------------------------------------------
    # Initialise variables
    input_file = None
    output_file = None
    filter = None
    cut = None
    utm = None
    dt = None

    #--------------------------------------------------------------------------

    for i in range(0, len(argv)):

        # Input file
        if '-r' in argv[i]:
            input_file = argv[i+1]

        # Output file
        if '-w' in argv[i]:
            output_file = argv[i+1]

        # Input/Output file (overwrite)
        if '-rw' in argv[i]:
            input_file = argv[i+1]
            output_file = input_file

        if '-filter' in argv[i]:
            filter = argv[i+1].split(',')

        if '-utm' in argv[i]:
            utm = argv[i+1]

        if '-cut' in argv[i]:
            T0 = argv[i+1].split(',')
            T1 = argv[i+2].split(',')
            cut = [[float(T) for T in T0],
                   [float(T) for T in T1]]

        if '-dt' in argv[i]:
            dt = float(argv[i+1])

    #--------------------------------------------------------------------------

    sac = sacutils.Sac(input_file)

    if filter:
        low_corner = None
        high_corner = None
        order = None

        if filter[0] not in ['None', 'none']:
            low_corner = float(filter[0])

        if filter[1] not in ['None', 'none']:
            high_corner = float(filter[1])

        if filter[2] not in ['None', 'none']:
            order = float(filter[2])

        sac.filter(low_corner, high_corner, order)

    if cut:
        sac.cut(cut[0], cut[1], dt)

    if utm:
        sac.wgs2xy(float(utm))

    if output_file:
        sac.write(output_file, owrite=True)


if __name__ == "__main__":
    main(sys.argv[1:])

