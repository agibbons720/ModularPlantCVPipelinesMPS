import glob, sys
import numpy as np
from plantcv import plantcv as pcv
from DataTypes import MetaData, RawData, DataUnit

"""
Responsible for reading in collection event data.
"""
class DataLoader:
     """
     Converts the metadata in [meta] to a DataUnit object.
     
     The metadata entry is used to attempt to load the corresponding images
     on the disk, and the success of that process determines the validity 
     flag within a given DataUnit. In any case, the loaded arrays are placed
     into the returned DataUnit instance.

     Parameters:
          meta - The MetaData representing the collection event raw data to load into a DataUnit.
     """
     def GenRaw(meta: MetaData) -> RawData:
          img, _, _ = pcv.readimage(meta.rgbFile) # Read from disk
          if np.average(img) < 50: # Check validity
               print("{} is a night image!".format(meta.rgbFile), file=sys.stderr)
               return RawData(False, 0)
          return RawData(True, img) # Valid, non-night entry

     """
     Scans the directory at [path] for collection event data and processes the findings into
     corresponding pairs of MetaData and DataUnits.
     
     Paramaters:
          path - Path to the directory of collection event data. Must have a trailing forward-slash.

     Returns:
          A list of pairs (a, b) where [a] is the MetaData for a collection event
          found in the directory [path] and [b] is the corresponding DataUnit that
          houses the associated, loaded raw data for the metadata in [a].
     """
     def LoadDir(path: str) -> list:
          jpgs = glob.glob(path + "*.jpg") # Scan directory
          data = []
          # TODO Hook up depth image pairs
          for name in jpgs: # Per collection event raw data entry
               meta = MetaData(DataLoader.GetTimestamp(name), name) # Make metadata
               raw = DataLoader.GenRaw(meta)
               if raw.valid:
                    data.append(DataUnit(raw, meta)) # Add converted DataUnit
          return data
               
     """
     Extracts the timestamp from the tail-end of a filename.
     
     Parameters:
          filename - The string containing a timestamp in the form of YYYY-MM-DD HH-MM-SS.

     Returns:
          A string representing the embedded timestamp in [filename] in the
          form of YYYY-MM-DD-HH-MM-SS.
     """
     def GetTimestamp(filename: str) -> str:
          return ""