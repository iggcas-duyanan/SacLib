# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2016 GEM Foundation
#
# The SacLib is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# SacLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# Author: Poggi Valerio

"""
An simple Python library for SAC file I/O
"""

from struct import pack, unpack
from copy import deepcopy
from os.path import isfile

#-----------------------------------------------------------------------------------------

class Sac():

  def __init__(self, File=[], ByteOrder=[]):
    """
    Main class
    -----------------------
    Usage:
      S = SacLib.Sac
      S = SacLib.Sac('MyFile.sac')

    Optional parameters:
      ByteOrder='le' (Little Endian, default)
               ='be' (Big Endian)

    Attributes:
      S.Head = SAC header information
      S.Data[0] = SAC trace
      S.Data[1] = SAC trace (optional block)
      S.Byte = Byte-Order

    Methods:
      S.Read = Read SAC file from disk
      S.Write = Write SAC file to disk
      S.Copy = Create copy of SAC object
      S.Print = Print header information
    """

    # Variable initialisation
    self.Head = {}
    self.Data = [[],[]]
    self.Byte = 'le'

    if ByteOrder:
      # Set byte order
      self.Byte = ByteOrder

    if File:
      # Import SAC file
      self.Read(File)

    else:
      # Set header defaults
      for H in _HdrStruc:
        self.Head[H[0]] = H[3]

  #---------------------------------------------------------------------------------------

  def Read(self, FileName, ByteOrder=[]):
    """
    Read SAC file from disk
    -----------------------
    Usage:
      S.Read('MyFile.sac')
      S.Read('MyFile.sac',ByteOrder='be')
    """

    if ByteOrder:
      # Set byte order
      self.Byte = ByteOrder

    # Open input SAC file
    with open(FileName, 'rb') as fid:

      # Import header
      for H in _HdrStruc:
        self.Head[H[0]] = _fread(fid, H[1], H[2], self.Byte)

      # Import first block of data
      for N in range(0,self.Head['NPTS']):
        self.Data[0].append(_fread(fid, 4, 'f', self.Byte));

      # Import second block of data
      if self.Head['LEVEN'] != 1 or self.Head['IFTYPE'] in (2, 3):
        for N in range(0,self.Head['NPTS']):
          self.Data[1].append(_fread(fid, 4, 'f', self.Byte));

      fid.close()
      return

    # Warn user if model file does not exist
    print 'Error: File not found'

  #---------------------------------------------------------------------------------------

  def Write(self, FileName, ByteOrder='le', OverWrite=False):
    """
    Write SAC file to disk
    -----------------------
    Usage:
      S.Write('MyFile.sac')
      S.Write('MyFile.sac',ByteOrder='be')
      S.Write('MyFile.sac',OverWrite=True)
    """

    if isfile(FileName) and not OverWrite:
      print 'Error: Not overwriting file'
      return

    if ByteOrder:
      # Set byte order (le/be)
      self.Byte = ByteOrder

    # Open output SAC file
    with open(FileName, 'wb') as fid:

      # Export header
      for H in _HdrStruc:
        _fwrite(fid, self.Head[H[0]], H[1], H[2], self.Byte)

      # Export first block of data
      for D in self.Data[0]:
        _fwrite(fid, D, 4, 'f', self.Byte)

      # Export second block of data
      if self.Data[1]:
        for D in self.Data[1]:
          _fwrite(fid, D, 4, 'f', self.Byte)

      fid.close()
      return

    # Warn user if model file does not exist
    print 'Error: File not found'

  #---------------------------------------------------------------------------------------

  def Copy(self):
    """
    Create a hard-copy of an
    existing SAC object
    -----------------------
    Usage:
      SacNew = Sac.Copy()
    """

    SacNew = deepcopy(self)

    return SacNew

  #---------------------------------------------------------------------------------------

  def Print(self):
    """
    Print header details
    -----------------------
    Usage:
      Sac.Print()
    """

    print '------------'
    for H in _HdrStruc:
      Data = self.Head[H[0]]

      if Data != H[3]:
        print '{0:>12} = {1}'.format(H[0],Data)

#-----------------------------------------------------------------------------------------
# INTERNAL: bytewise read

def _fread(fid, bnum, bkey, bord):

    hex = fid.read(bnum)

    if bkey == 's': bkey = str(bnum) + bkey
    if bord == 'be': bkey = '>' + bkey
    if bord == 'le': bkey = '<' + bkey

    data = unpack(bkey, hex)[0]

    return data

#-----------------------------------------------------------------------------------------
# INTERNAL: bytewise write

def _fwrite(fid, data, bnum, bkey, bord):

    if bkey == 's': bkey = str(bnum) + bkey
    if bord == 'be': bkey = '>' + bkey
    if bord == 'le': bkey = '<' + bkey

    hex = pack(bkey, data)

    fid.write(hex)

#-----------------------------------------------------------------------------------------
# Header Structure (sorted):
#   [0] - Field Name
#   [1] - Length in Bytes
#   [2] - Variable Type
#   [3] - Default Vaule

_HdrStruc = [('DELTA',4,'f',-12345),
             ('DEPMIN',4,'f',-12345),
             ('DEPMAX',4,'f',-12345),
             ('SCALE',4,'f',-12345),
             ('ODELTA',4,'f',-12345),
             ('B',4,'f',-12345),
             ('E',4,'f',-12345),
             ('O',4,'f',-12345),
             ('A',4,'f',-12345),
             ('INTERNAL1',4,'f',-12345),
             ('T0',4,'f',-12345),
             ('T1',4,'f',-12345),
             ('T2',4,'f',-12345),
             ('T3',4,'f',-12345),
             ('T4',4,'f',-12345),
             ('T5',4,'f',-12345),
             ('T6',4,'f',-12345),
             ('T7',4,'f',-12345),
             ('T8',4,'f',-12345),
             ('T9',4,'f',-12345),
             ('F',4,'f',-12345),
             ('RESP0',4,'f',-12345),
             ('RESP1',4,'f',-12345),
             ('RESP2',4,'f',-12345),
             ('RESP3',4,'f',-12345),
             ('RESP4',4,'f',-12345),
             ('RESP5',4,'f',-12345),
             ('RESP6',4,'f',-12345),
             ('RESP7',4,'f',-12345),
             ('RESP8',4,'f',-12345),
             ('RESP9',4,'f',-12345),
             ('STLA',4,'f',-12345),
             ('STLO',4,'f',-12345),
             ('STEL',4,'f',-12345),
             ('STDP',4,'f',-12345),
             ('EVLA',4,'f',-12345),
             ('EVLO',4,'f',-12345),
             ('EVEL',4,'f',-12345),
             ('EVDP',4,'f',-12345),
             ('MAG',4,'f',-12345),
             ('USER0',4,'f',-12345),
             ('USER1',4,'f',-12345),
             ('USER2',4,'f',-12345),
             ('USER3',4,'f',-12345),
             ('USER4',4,'f',-12345),
             ('USER5',4,'f',-12345),
             ('USER6',4,'f',-12345),
             ('USER7',4,'f',-12345),
             ('USER8',4,'f',-12345),
             ('USER9',4,'f',-12345),
             ('DIST',4,'f',-12345),
             ('AZ',4,'f',-12345),
             ('BAZ',4,'f',-12345),
             ('GCARC',4,'f',-12345),
             ('INTERNAL2',4,'f',-12345),
             ('INTERNAL3',4,'f',-12345),
             ('DEPMEN',4,'f',-12345),
             ('CMPAZ',4,'f',-12345),
             ('CMPINC',4,'f',-12345),
             ('XMINIMUM',4,'f',-12345),
             ('XMAXIMUM',4,'f',-12345),
             ('YMINIMUM',4,'f',-12345),
             ('YMAXIMUM',4,'f',-12345),
             ('UNUSED1',4,'f',-12345),
             ('UNUSED2',4,'f',-12345),
             ('UNUSED3',4,'f',-12345),
             ('UNUSED4',4,'f',-12345),
             ('UNUSED5',4,'f',-12345),
             ('UNUSED6',4,'f',-12345),
             ('UNUSED7',4,'f',-12345),
             ('NZYEAR',4,'i',-12345),
             ('NZJDAY',4,'i',-12345),
             ('NZHOUR',4,'i',-12345),
             ('NZMIN',4,'i',-12345),
             ('NZSEC',4,'i',-12345),
             ('NZMSEC',4,'i',-12345),
             ('NVHDR',4,'i',6),
             ('NORID',4,'i',-12345),
             ('NEVID',4,'i',-12345),
             ('NPTS',4,'i',-12345),
             ('INTERNAL4',4,'i',-12345),
             ('NWFID',4,'i',-12345),
             ('NXSIZE',4,'i',-12345),
             ('NYSIZE',4,'i',-12345),
             ('UNUSED8',4,'i',-12345),
             ('IFTYPE',4,'i',1),
             ('IDEP',4,'i',-12345),
             ('IZTYPE',4,'i',-12345),
             ('UNUSED9',4,'i',-12345),
             ('IINST',4,'i',-12345),
             ('ISTREG',4,'i',-12345),
             ('IEVREG',4,'i',-12345),
             ('IEVTYP',4,'i',-12345),
             ('IQUAL',4,'i',-12345),
             ('ISYNTH',4,'i',-12345),
             ('IMAGTYP',4,'i',-12345),
             ('IMAGSRC',4,'i',-12345),
             ('UNUSED10',4,'i',-12345),
             ('UNUSED11',4,'i',-12345),
             ('UNUSED12',4,'i',-12345),
             ('UNUSED13',4,'i',-12345),
             ('UNUSED14',4,'i',-12345),
             ('UNUSED15',4,'i',-12345),
             ('UNUSED16',4,'i',-12345),
             ('UNUSED17',4,'i',-12345),
             ('LEVEN',4,'i',1),
             ('LPSPOL',4,'i',0),
             ('LOVROK',4,'i',1),
             ('LCALDA',4,'i',1),
             ('UNUSED18',4,'i',0),
             ('KSTNM',8,'s','-12345  '),
             ('KEVNM',16,'s','-12345  -12345  '),
             ('KHOLE',8,'s','-12345  '),
             ('KO',8,'s','-12345  '),
             ('KA',8,'s','-12345  '),
             ('KT0',8,'s','-12345  '),
             ('KT1',8,'s','-12345  '),
             ('KT2',8,'s','-12345  '),
             ('KT3',8,'s','-12345  '),
             ('KT4',8,'s','-12345  '),
             ('KT5',8,'s','-12345  '),
             ('KT6',8,'s','-12345  '),
             ('KT7',8,'s','-12345  '),
             ('KT8',8,'s','-12345  '),
             ('KT9',8,'s','-12345  '),
             ('KF',8,'s','-12345  '),
             ('KUSER0',8,'s','-12345  '),
             ('KUSER1',8,'s','-12345  '),
             ('KUSER2',8,'s','-12345  '),
             ('KCMPNM',8,'s','-12345  '),
             ('KNETWK',8,'s','-12345  '),
             ('KDATRD',8,'s','-12345  '),
             ('KINST',8,'s','-12345  ')]