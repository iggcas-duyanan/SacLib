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
"""
An simple Python library for SAC file manipulation
"""

import numpy as np
import scipy.signal as sig
import scipy.interpolate as itp
import copy
import pyproj
import sys
import sacio


# =============================================================================

class Sac(sacio.Sac):

    #--------------------------------------------------------------------------

    def copy(self):
        """
        Create a hard-copy of an existing SAC object
        """

        return copy.deepcopy(self)

    #--------------------------------------------------------------------------

    def filter(self, low_corner=None, high_corner=None, order=None):
        """
        Butterworth filter
        """

        DT = self.head['DELTA']

        # Corner frequencies
        corners = []

        if low_corner:
            corners.append(2.*low_corner*DT)
            filter_type = 'high'

        if high_corner:
            corners.append(2.*high_corner*DT)
            filter_type = 'low'

        if low_corner and high_corner:
            filter_type = 'band'

        if len(corners) > 0:
            # Butterworth filter
            b, a = sig.butter(order, corners, btype=filter_type)

            # Filtering seismic record
            zi = sig.lfilter_zi(b, a);
            self.data[0],_ = sig.lfilter(b, a, self.data[0],
                                         zi=zi*self.data[0][0])

    #--------------------------------------------------------------------------

    def cut(self, date_start, date_stop, dt=None):
        """
        Cut (and resample) seismic record within given time
        bounds (in seconds from 1.1.1.0.0.0)
        """

        DT = self.head['DELTA']
        TN = self.head['NPTS']

        if not dt:
            # Keep original sampling time
            dt = DT

        # Convert to ordinal date, if needed
        if len(date_start) == 6:
            date_start = _dateconvert(date_start)

        if len(date_stop) == 6:
            date_stop = _dateconvert(date_stop)

        # Reference time (in seconds)
        sec_ref = _date2sec(self.head['NZYEAR'],
                            self.head['NZJDAY'],
                            self.head['NZHOUR'],
                            self.head['NZMIN'],
                            self.head['NZSEC'],
                            self.head['NZMSEC'])

        sec_start = _date2sec(date_start[0],
                              date_start[1],
                              date_start[2],
                              date_start[3],
                              date_start[4])

        sec_stop = _date2sec(date_stop[0],
                             date_stop[1],
                             date_stop[2],
                             date_stop[3],
                             date_stop[4])

        tax0 = np.linspace(sec_ref, sec_ref+(TN-1)*DT, TN)
        tax1 = np.arange(sec_start, sec_stop+dt, dt)

        data = itp.interp1d(tax0, self.data[0],
                            bounds_error=False,
                            fill_value=0.)

        self.data[0] = data(tax1)

        self.head['DELTA'] = dt
        self.head['NPTS'] = len(self.data[0])
        self.head['NZYEAR'] = date_start[0]
        self.head['NZJDAY'] = date_start[1]
        self.head['NZHOUR'] = date_start[2]
        self.head['NZMIN'] = date_start[3]
        self.head['NZSEC'] = divmod(date_start[4], 1)[0]
        self.head['NZMSEC'] = divmod(date_start[4], 1)[1]

    #--------------------------------------------------------------------------

    def wgs2xy(self, utm_zone=32):
        """
        Converting from WGS coordinates to cartesian using UTM
        projection and store them into USER7 and USER8 fields
        """

        lon = self.head['STLO']
        lat = self.head['STLA']

        P = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84')
        x,y = P(lon, lat)

        self.head['USER7'] = x
        self.head['USER8'] = y


# =============================================================================
# Utility functions

def _ordinalday(year, month, day):

    if _leapcheck(year):
        MDAYS = [0.,31.,60.,91.,121.,152.,182.,213.,244.,274.,305.,335.]
    else:
        MDAYS = [0.,31.,59.,90.,120.,151.,181.,212.,243.,273.,304.,334.]

    oday = MDAYS[month-1] + day

    return oday


def _dateconvert(date):
    """
    Convert a standard date into ordinal date:
    (year,month,day,hour,min,sec > year,oday,hour,min,sec)
    """

    oday = _ordinalday(date[0], date[1], date[2])

    return [date[0], oday, date[3], date[4], date[5]]


def _date2sec(year, oday, hour, min, sec, msec=0.):
    """
    Transform full date to total seconds, computed
    from 1st January, 1AD
    """

    DSEC = 24.*3600.
    YDAYS = 365.

    ysec = (year-1)*YDAYS*DSEC
    ysec += _leapnum(year)*DSEC
    dsec = (oday-1)*DSEC
    tsec = ysec + dsec + hour*3600.+ min*60. + sec*1. + msec/1e3

    return tsec


def _leapnum(year):
    """
    Return the number of leap years occurring before that date
    """

    N0 = (year-1)//4
    N1 = (year-1)//100
    N2 = (year-1)//400

    return N0 - N1 + N2


def _leapcheck(year):
    """
    Check if year is a leap year (boolean)
    """

    C0 = (year % 4 == 0)
    C1 = (year % 100 != 0)
    C2 = (year % 400 == 0)

    return (C0 and C1) or C2
