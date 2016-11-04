#SacLib
An simple Python library for SAC file I/O

##Usage:
S = SacLib.Sac__
S = SacLib.Sac('MyFile.sac')__

##Attributes:
S.Head = SAC header information
S.Data[0] = SAC trace
S.Data[1] = SAC trace (optional block)
S.Byte = Byte-Order

##Methods:
S.Read = Read SAC file from disk
S.Write = Write SAC file to disk
S.Copy = Create copy of SAC object
S.Print = Print header information
