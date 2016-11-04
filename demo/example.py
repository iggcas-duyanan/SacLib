"""
SACLib - A Simple library for I/O of SAC files
----------------------------------------------
"""

import SacLib

FileIn = 'data/x.sac'
FileOut = 'data/x_out.sac'

# Initialise main object
S = SacLib.Sac()

# Read SAC file
S.Read(FileIn, ByteOrder='be')

# Write SAC file
S.Write(FileOut, ByteOrder='le', OverWrite=True)

# Create a copy
S2 = S.Copy()

# Print header
S2.Print()


