from random import getrandbits
import numpy as np

"""
Superclass for all interfaces between Pipeline Stages.

Remarks:
    This class exists solely to enable polymorphism in the nature
    of these interfaces. For example, if Stage X outputs only a single
    image and Stage Y only accepts one, then just a single image field is required;
    increase this requirement to two, and now another field would be needed.

    The justification for not having a single class where a variable-length
    list of images to be passed is housed is because there could be potential
    for mismatching which index of that list corresponds to which image type.

    By forcing the hierarchical approach, there is a gurantee that when a given
    Stage requests the white-balanced image in the first slot, it will find it since
    it is housed in a SingleImageChannel, for example. Finally, this ultimately allows
    for increased 
"""
class StageChannel(object):
    pass

"""
Represents an interface for a Pipeline Stage that either outputs or takes in a single image.
"""
class SingleImageChannel(StageChannel):
    """Read-only field to identify this type of stage interface when checking Stage compatibility."""
    CHANNEL_ID: int = getrandbits(256) # Read-only

    """
    Constructs a new interface instance filled with an image.

    Parameters:
        img - The current NumPy equivalent of the image data to associate.
    """
    def __init__(self, img: np.ndarray):
        self.img = img

"""
Represents an interface for a Pipeline Stage that either outputs or takes in two images.
"""
class DoubleImageChannel(StageChannel):
    """Read-only field to identify this type of stage interface when checking Stage compatibility."""
    CHANNEL_ID: int = getrandbits(256) # Read-only

    """
    Constructs a new interface instance filled with two images.

    Parameters:
        imgPrimary - The first of the current NumPy equivalents of the image data to associate.
        imgSecondary - The first of the current NumPy equivalents of the image data to associate.
        tag - 
    """
    def __init__(self, imgPrimary: np.ndarray, imgSecondary: np.ndarray, tag: str):
        self.imgPrimary = imgPrimary
        self.imgSecondary = imgSecondary
        self.tag = tag

"""
Represents an interface specifically for a Consildation Pipeline Stage.
"""
class SnapshotChannel(StageChannel):
    """Read-only field to identify this type of stage interface when checking Stage compatibility."""
    CHANNEL_ID: int = getrandbits(256) # Read-only

    """
    Constructs a new interface instance filled with all the given FormattedData entries.

    Parameters:
        formatted - The FormattedData instances to associate.
    """
    def __init__(self, formatted: list):
        self.formatted = formatted

"""
Represents an interface for a Pipeline Stage that either inputs or outputs a list of countours and masks.
"""
class SegmentationChannel(StageChannel):
    """Read-only field to identify this type of stage interface when checking Stage compatibility."""
    CHANNEL_ID: int = getrandbits(256) # Read-only

    """
    Constructs a new interface instance filled with two lists of contours and masks.

    Parameters:
        contours - The list of contours to associate.
        masks - The list of masks to associate.
        rgb - The most recent version of the RGB data.
        tag - 
    """
    def __init__(self, contours: list, masks: list, rgb: np.ndarray, tag: str):
        self.contours = contours
        self.masks = masks
        self.rgb = rgb
        self.tag = tag
