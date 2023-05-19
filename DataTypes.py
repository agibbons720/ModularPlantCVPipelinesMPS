import numpy as np
from typing import NamedTuple, List, Dict

"""
Custom type-definition
"""
StageEntry = Dict[str, np.ndarray]

"""
Houses all of the strings needed for representing
a collective event's data.
"""
class MetaData(NamedTuple):
     """Images' timestamp string in the form of YYYY-MM-DD HH_MM_SS"""
     timestamp: str

     """Path to the JPG image that contains the RGB data"""
     rgbFile: str

     """Path to the image file that contains the Depth map data"""
     #depthFile: str

"""
Represents the loaded data for a given collection event.
Is associated with a MetaData entry in a DataUnit instance.
"""
class RawData(NamedTuple):
     """Whether or not the loaded arrays are valid (i.e., images were loaded succesfully)"""
     valid: bool

     """PlantCV-compatible RGB data"""
     rgb: np.ndarray

     """PlantCV-compatible Depth Map data"""
     #depth: np.ndarray

"""
Represents all of the information related to a single collection event.
"""
class DataUnit(NamedTuple):
     """Loaded, unprocessed RGB and Depth data"""
     raw: RawData

     """Information needed to access the unloaded raw data from the disk"""
     meta: MetaData

"""
Represents the evolution of an initial collection event's data over
the course of the pipeline's execution.
"""
class FormattedData(NamedTuple):
     """The initial collection event data loaded from disk."""
     base: RawData # Ideally a read-only pointer (const Rawdata *const); no ownership

     """
     All of the outputs associated with the RawData in [base] from all of the processing 
     units across all Stages in the pipeline.
     """
     proc: List[StageEntry]