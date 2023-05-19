"""
Superclass for configuring a given Pipeline stage.

Allows for swapping the order of PlantCV calls in the pipeline at runtime.
"""
class StageConfig(object):
     pass

"""
Used to setup a WhiteBalance Pipeline Stage.
"""
class WhiteBalanceConfig(StageConfig):
     """
     Constructs a new configuration for a WhiteBalance Pipeline Stage.

     Wraps parameters for pcv.white_balance.

     Parameters:
        roi - A four-valued tuple (a, b, c, d) where the pixels in the rectangle 
              formed by points (a, b) and (c, d) are used relatively to white-balance
              the rest of the image.
     """
     def __init__(self, roi: tuple):
          self.roi = roi

"""
Used to setup a ViewportAdjust Pipeline Stage.
"""
class ViewportAdjustConfig(StageConfig):
     """
     Constructs a new configuration for a ViewportAdjust Pipeline Stage.
     
     Wraps parameters for pcv.rotate, pcv.shift_img
     
     Parameters:
        side - One of 'top', 'bottom', 'left', 'right'. The side from which to initate the translation.
        rotate - The amount in degrees to rotate the image clockwise.
        shift - Amount in pixels to translate the rotated image.
     """
     def __init__(self, side: str, rotate: int, shift: int):
          self.side = side
          self.rotate = rotate
          self.shift = shift

"""
Used to setup a BinaryMask Pipeline Stage.

Controls various parameters for PlantCV's binary mask functions.
"""
class BinaryMaskConfig(StageConfig):
    """
    Constructs a new configuration for a BinaryMask Pipeline Stage.

    Wraps parameters for pcv.rgb2gray_lab, pcv.threshold.binary, pcv.fill

    Parameters:
        threshold - Values in [0, 255]. Represents the cutoff for "hot" pixel intensity in the mask.
        mx - Value should be greater than [threshold]. Represents the value of pixels that make the cutoff for the mask.
        obj - One of 'light' or 'dark'. Represents nature of environment.
        fill - The amount by which to reduce noise in the mask.
        channel - The color channel upon which to enforce the threshold.
    """
    def __init__(self, threshold: int, mx: int, obj: str, fill: int, channel: str):
        self.threshold = threshold
        self.mx = mx
        self.obj = obj
        self.fill = fill
        self.channel = channel

"""
Used to setup a Consolidation Pipeline Stage.
"""
class ConsolidationConfig(StageConfig):
    """
    Constructs a new configuration for a RigidSegmentation Pipeline Stage.
     
    Parameters:
        stageNames - The string names for all of the stages whose output
                     should be grouped into the specified channel
        outChannelId - The type of channel interface to consolidate the previous 
                       specified stages' outputs into.    
    """
    def __init__(self, stageNames: list, outChannelId: int):
        self.stageNames = stageNames
        self.outChannelId = outChannelId

class RigidSegmentationConfig(StageConfig):
    def GetRigidType(self):
        pass

"""
Used to setup a RigidSegmentationGrid Pipeline Stage.
"""
class RigidSegmentationGridConfig(RigidSegmentationConfig):
    RIGID_TYPE: int = 0

    """
     Constructs a new configuration for a RigidSegmentationGrid Pipeline Stage.
     
     Wraps parameters for pcv.find_objects, pcv.multi.roi
     
     Parameters:
        start - The (x, y) pixel coordinates of the first ROI to create; all others relative to this.
        radius - The radius of the ROI circles to create.
        spacing - A pair of deltas (dx, dy) such that the other plants can be found by creating linear combinations with [start].
        rows - Number of rows in the grid of ROIs to create.
        cols - Numbers of columns in the grid of ROIs to create.
     """
    def __init__(self, start: tuple, radius: int, spacing: tuple, rows: int, cols: int, roiType: str):
        self.start = start
        self.radius = radius
        self.spacing = spacing
        self.rows = rows
        self.cols = cols
        self.roiType = roiType

    def GetRigidType(self):
        return RigidSegmentationGridConfig.RIGID_TYPE

"""
Used to setup a RigidSegmentationCustom Pipeline Stage.
"""
class RigidSegmentationCustomConfig(RigidSegmentationConfig):
    RIGID_TYPE: int = 1

    """
     Constructs a new configuration for a RigidSegmentationCustom Pipeline Stage.
     
     Wraps parameters for pcv.find_objects, pcv.multi.roi
     
     Parameters:
        centers - A list of a pairs of points (x, y) indicating where the plants are in the image.
        radius - The radius of the circle about the centers in [centers].
     """
    def __init__(self, centers: list, radius: int):
        self.centers = centers
        self.radius = radius
    
    def GetRigidType(self):
        return RigidSegmentationCustomConfig.RIGID_TYPE

"""
Used to setup a DBSCANSegmentation Pipeline Stage.
"""
class DBSCANSegmentationConfig(StageConfig):
    """
    Constructs a new configuration for a DBSCANSegmentation Pipeline Stage.
     
    Wraps parameters for pcv.spatial_clustering
     
    Parameters:
       minClusterSize - The lower bound for how many pixels to have in each cluster.
       epsilon - Hyperparamter that relates how close another pixel must be to the centroid for inclusion.
    """
    def __init__(self, minClusterSize: int, epsilon: float):
        self.minClusterSize = minClusterSize
        self.epsilon = epsilon

"""
Used to setup a PlantAnalysis Pipeline Stage.
"""
class PlantAnalysisConfig(StageConfig):
    """
    Constructs a new configuration for a PlantAnalysis Pipeline Stage.
     
    Wraps parameter for pcv.output.save_results
    
    Parameters:
       filetype - One of 'csv', 'json'. Format to use when writing the extracted plant feature data to disk.
       outfile - The destination on disk to write the extracted feature data CSV to.
    """
    def __init__(self, filetype, outfile):
        self.filetype = filetype
        self.outfile = outfile
