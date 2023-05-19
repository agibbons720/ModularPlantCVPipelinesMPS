import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
from typing import cast
from StageConfig import StageConfig, WhiteBalanceConfig, ViewportAdjustConfig, BinaryMaskConfig, RigidSegmentationConfig, RigidSegmentationGridConfig, RigidSegmentationCustomConfig, DBSCANSegmentationConfig, PlantAnalysisConfig, ConsolidationConfig
from StageChannel import StageChannel, SingleImageChannel, DoubleImageChannel, SegmentationChannel, SnapshotChannel

"""
Represents an encapsulated processing unit that involves wrapped PlantCV function calls.

Each Stage instance can be fitted with a corresponding StageConfig object, which preps the
the desired PlantCV calls with the specified parameters. To run the Stage, simply call [Invoke].
Compatibility between stages is determined by looking pairwise at the values returned from [GetInterfaceIDs].
"""
class Stage(object):
    """
    Construct a new Stage instance.
    
    Parameters:
        cfg - The parameters for the PlantCV calls used
              in this stage.
    """
    def __init__(self, cfg):
        self.cfg = cfg

    """
    Retrives the string identifier for the Stage.

    Returns:
        The literal equivalent of the Stage name without quotes.
    """
    def GetName() -> str:
        pass

    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.

    Returns:
        A pair (a, b) where both are of type int and represent the input and output interface IDs for
        this Stage, respectively.
    """
    def GetInterfaceIDs(self) -> tuple:
        pass

    """
    Runs this Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A StageChannel that contains data to process during this stage.

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage and [b] is the
        outputted data from the calls performed in this stage. Specifically, [b] is
        the np.ndarray of interest that was produced from the processing.
    """
    def Invoke(inData: StageChannel) -> tuple:
        pass

"""
Represents a configurable processing unit that invokes PlantCV calls to produce a white-balanced image.

This Stage will white-balance the supplied image relative to the pixel values in the ROI provided in the configuration.
"""
class WhiteBalance(Stage):
    """
    Constructs a new WhiteBalance Stage instance.

    Parameters:
        cfg - The configuration for the PlantCV calls used
              in this stage.
    """
    def __init__(self, cfg: WhiteBalanceConfig):
        super().__init__(cfg)
    
    """
    Retrives the string identifier for the WhiteBalance Stage.

    Returns:
        The literal (without quotes): "WhiteBalance"
    """
    def GetName(self) -> str:
        return "WhiteBalance"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair of identical SingleImageChannel IDs.
    """
    def GetInterfaceIDs(self) -> tuple:
        return (SingleImageChannel.CHANNEL_ID, SingleImageChannel.CHANNEL_ID)
    
    """
    Runs the WhiteBalance Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A SingleImageChannel that contains the np.ndarray of the image data to process
                 during this stage.

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "WhiteBalance") and [b] is the
        outputted np.ndarray from the final PlantCV call performed in this stage. Specifically, [b] is
        the white-balanced adjusted version of the passed in RGB image within a SingleImageChannel.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        wbInput = cast(SingleImageChannel, inData)
        oImg = pcv.white_balance(wbInput.img, roi=self.cfg.roi)
        oChannel = SingleImageChannel(oImg) # Package for next stage
        return (self.GetName(), oChannel)

"""
Represents a configurable processing unit that invokes PlantCV calls to produce an image where the origin is in the bottom-left (0,0).

This Stage will rotate the input image the desired amount, then translate the result as much as is specified.
"""
class ViewportAdjust(Stage):
    """
    Constructs a new ViewportAdjust Stage instance.

    Parameters:
        cfg - The configuration for the PlantCV calls used
              in this stage.
    """    
    def __init__(self, cfg: ViewportAdjustConfig):
        super().__init__(cfg)

    """
    Retrives the string identifier for the ViewportAdjust Stage.

    Returns:
        The literal (without quotes): "ViewportAdjust"
    """    
    def GetName(self) -> str:
        return "ViewportAdjust"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair of identical SingleImageChannel IDs.
    """
    def GetInterfaceIDs(self) -> int:
        return (SingleImageChannel.CHANNEL_ID, SingleImageChannel.CHANNEL_ID)
    
    """
    Runs the ViewportAdjust Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A SingleImageChannel that contains the np.ndarray of the image data to process
                 during this stage.

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "ViewportAdjust") and [b] is the
        outputted np.ndarray from the final PlantCV call performed in this stage. Specifically, [b] is
        the viewport adjusted version of the passed in RGB image within a SingleImageChannel.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        vaInput = cast(SingleImageChannel, inData)
        pcv.params.verbose = False
        turned = pcv.rotate(vaInput.img, rotation_deg=self.cfg.rotate, crop=False)
        oImg = pcv.shift_img(turned, number=self.cfg.shift, side=self.cfg.side)
        oChannel = SingleImageChannel(oImg) # Package for next stage
        return (self.GetName(), oChannel)

"""
Represents a configurable processing unit that invokes PlantCV calls to produce an equivalent and filled binary mask.

This Stage will extract a desired channel from the image and create a mask based on given threshold values.
From there, the mask is filled to prevent noise and the result is returned.
"""
class BinaryMask(Stage):
    """
    Constructs a new BinaryMask Stage instance.

    Parameters:
        cfg - The configuration for the PlantCV calls used
              in this stage.
    """
    def __init__(self, cfg: BinaryMaskConfig):
        super().__init__(cfg)

    """
    Retrives the string identifier for the BinaryMask Stage.

    Returns:
        The literal (without quotes): "BinaryMask"
    """
    def GetName(self) -> str:
        return "BinaryMask"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair of identical SingleImageChannel IDs.
    """
    def GetInterfaceIDs(self) -> tuple:
        return (SingleImageChannel.CHANNEL_ID, SingleImageChannel.CHANNEL_ID)
    
    """
    Runs the BinaryMask Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A SingleImageChannel that contains the np.ndarray of the image data to process
                 during this stage.

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "BinaryMask") and [b] is the
        outputted np.ndarray from the final PlantCV call performed in this stage. Specifically, [b] is
        the filled binary mask produced from the input image based on the configuration parameters housed
        within a SingleImageChannel.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        bmIn = cast(SingleImageChannel, inData)
        chan = pcv.rgb2gray_lab(bmIn.img, channel=self.cfg.channel)
        thre = pcv.threshold.binary(chan, threshold=self.cfg.threshold, max_value=self.cfg.mx, object_type=self.cfg.obj)
        oImg = pcv.fill(thre, size=self.cfg.fill)
        oChannel = SingleImageChannel(oImg) # Package for next stage
        return (self.GetName(), oChannel)

"""
Represents a stage whose sole purpose is to combine the outputs of multiple previous stages' outputs and package 
into a StageChannel for processing in the next step.
"""
class Consolidation(Stage):
    """
    Constructs a new Consolidation Stage instance.
    
    Parameters:
        cfg - A configuration detailng what Stage outputs to group.
    """
    def __init__(self, cfg: ConsolidationConfig):
        super().__init__(cfg)

    """
    Retrives the string identifier for the Consolidation Stage.

    Returns:
        The literal (without quotes): "Consolidation"
    """
    def GetName(self) -> str:
        return "Consolidation"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair (a, b) where [a] is a DoubleImageChannel ID and [b] is the specified output channel ID.
    """
    def GetInterfaceIDs(self) -> tuple:
        return (SnapshotChannel.CHANNEL_ID, self.cfg.outChannelId)
    
    """
    Extracts the output from the stage with name [stageName] from the list of StageEntry instances [formatted].

    Parameters:
        stageName - The string name of the Stage whose output should be collected.
        formatted - A list of StageEntry instances outputted so far by the pipeline; used for sourcing images.
    """
    def FindOutput(self, stageName, formatted):
        for entry in formatted:
            if entry[0] == stageName:
                if stageName == "Disk":
                    return entry[1].raw.rgb
                else:    
                    return entry[1].img
        return 0

    """
    Runs the RigidSegmentation Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A DoubleImageChannel containing the RGB data and corresponding binary mask to segment. 

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "BinaryMask") and [b] is a 
        SegmentationChannel containing all of the found contours and masks for the individually labeled plants.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        csInput = cast(SnapshotChannel, inData)
        if self.cfg.outChannelId == SingleImageChannel.CHANNEL_ID:
            return (self.GetName(), SingleImageChannel(img=self.FindOutput(self.cfg.stageNames[0], csInput.formatted)))
        elif self.cfg.outChannelId == DoubleImageChannel.CHANNEL_ID:
            return (self.GetName(), DoubleImageChannel(imgPrimary=self.FindOutput(self.cfg.stageNames[0], csInput.formatted),
                                                       imgSecondary=self.FindOutput(self.cfg.stageNames[1], csInput.formatted),
                                                       tag=csInput.formatted[0][1].meta.rgbFile))

"""
Represents a configurable processing unit that invokes PlantCV calls to produce individual masks for each plant.

This stage will attempt to find objects within the image and create an ROI as well as an object hierarchy and contour per plant.
This is carried out through specifying the nature of the grid-like layout to adhere to in the configuration.
"""
class RigidSegmentation(Stage):
    """
    Constructs a new RigidSegmentation Stage instance.

    Parameters:
        cfg - The configuration for the PlantCV calls used
              in this stage.
    """
    def __init__(self, cfg: StageConfig):
        super().__init__(cfg)

    """
    Retrives the string identifier for the RigidSegmentation Stage.

    Returns:
        The literal (without quotes): "RigidSegmentation"
    """
    def GetName(self) -> str:
        return "RigidSegmentation"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair (a, b) where [a] is a DoubleImageChannel ID and [b] is a SegmentationChannel ID.
    """
    def GetInterfaceIDs(self) -> tuple:
        return (DoubleImageChannel.CHANNEL_ID, SegmentationChannel.CHANNEL_ID)
    
    """
    Runs the RigidSegmentation Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A DoubleImageChannel containing the RGB data and corresponding binary mask to segment. 

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "BinaryMask") and [b] is a 
        SegmentationChannel containing all of the found contours and masks for the individually labeled plants.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        rsInput = cast(DoubleImageChannel, inData)
        objs, objH = pcv.find_objects(rsInput.imgPrimary, rsInput.imgSecondary)
        rCfg = cast(RigidSegmentationConfig, self.cfg)
        if rCfg.GetRigidType() == RigidSegmentationGridConfig.RIGID_TYPE:
            gCfg = cast(RigidSegmentationGridConfig, rCfg)
            rois, roiH = pcv.roi.multi(rsInput.imgPrimary, coord=gCfg.start, 
                                                       radius=gCfg.radius, 
                                                       spacing=gCfg.spacing, 
                                                       nrows=gCfg.rows, 
                                                       ncols=gCfg.cols)
        elif rCfg.GetRigidType() == RigidSegmentationCustomConfig.RIGID_TYPE:
            cCfg = cast(RigidSegmentationCustomConfig, self.cfg)
            rois, roiH = pcv.roi.multi(rsInput.imgPrimary, coord=cCfg.centers, radius=cCfg.radius)
        oContours = []
        oMasks = []
        for i in range(0, len(rois)):
            xCont, xHier, _, pArea = pcv.roi_objects(rsInput.imgPrimary, 
                                                     roi_contour=rois[i],
                                                     roi_hierarchy=roiH[i],
                                                     object_contour=objs,
                                                     obj_hierarchy=objH)
            if pArea <= 0:
                oContours.append([])
                oMasks.append([])
                continue # Go to next plant but recognize that there was no reading
            pCont, pMask = pcv.object_composition(rsInput.imgPrimary, contours=xCont, hierarchy=xHier)
            oContours.append(pCont)
            oMasks.append(pMask)
        return (self.GetName(), SegmentationChannel(contours=oContours, masks=oMasks, rgb=rsInput.imgPrimary, tag=rsInput.tag))

"""
Represents a configurable processing unit that invokes PlantCV calls to produce individual masks for each plant.

This stage will attempt to find objects within the image and create an ROI as well as an object hierarchy and contour per plant.
This is carried out through repeated use of DBSCAN.
"""
class DBSCANSegmentation(Stage):
    """
    Constructs a new DBSCANSegmentation Stage instance.

    Parameters:
        cfg - The configuration for the PlantCV calls used
              in this stage.
    """
    def __init__(self, cfg: DBSCANSegmentationConfig):
        super().__init__(cfg)

    """
    Retrives the string identifier for the DBSCANSegmentation Stage.

    Returns:
        The literal (without quotes): "DBSCANSegmentation"
    """
    def GetName(self) -> str:
        return "DBSCANSegmentation"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair (a, b) where [a] is a DoubleImageChannel ID and [b] is a SegmentationChannel ID.
    """
    def GetInterfaceIDs(self) -> tuple:
        return (DoubleImageChannel.CHANNEL_ID, SegmentationChannel.CHANNEL_ID)
    
    """
    Runs the DBSCANSegmentation Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A DoubleImageChannel containing the RGB data and corresponding binary mask to segment. 

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "BinaryMask") and [b] is a 
        SegmentationChannel containing all of the found contours and masks for the individually labeled plants.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        dbInput = cast(DoubleImageChannel, inData)
        _, cMsks = pcv.spatial_clustering(mask=dbInput.imgSecondary, algorithm="DBSCAN", 
                                            min_cluster_size=self.cfg.minClusterSize, max_distance=self.cfg.epsilon)
        def extractSubMasks(topLvlMask, masks) -> list:
            for mask in topLvlMask:
                _, sbMsks = pcv.spatial_clustering(mask=mask, algorithm="DBSCAN", min_cluster_size=self.cfg.minClusterSize, max_distance=self.cfg.epsilon)
                if len(sbMsks) == 1:
                    masks.append(mask) # Best one can get with these hyperparameters
                else:
                    for sbMsk in extractSubMasks(topLevelMsk=sbMsks, masks=[]):
                        masks.append(sbMsk)
            return masks
        retMsks = []
        retCnts = []
        for mask in cMsks:
            retMsks.append(mask)
            cnt = pcv.roi.from_binary_image(img=dbInput.imgPrimary, bin_img=mask)
            retCnts.append(cnt)
        return (self.GetName(), SegmentationChannel(contours=retCnts, masks=retMsks, rgb=dbInput.imgPrimary, tag=dbInput.tag))

"""
Represents a configurable processing unit that invokes PlantCV calls to analyze and save the features of individual plants.

This stage will attempt to analyze each individual plant in the image; in the end, all data is written to a csv file.
"""
class PlantAnalysis(Stage):
    """
    Constructs a new PlantAnalysis Stage instance.

    Parameters:
        cfg - The configuration for the PlantCV calls used
              in this stage.
    """
    def __init__(self, cfg: PlantAnalysisConfig):
        super().__init__(cfg)

    """
    Retrives the string identifier for the PlantAnalysis Stage.

    Returns:
        The literal (without quotes): "PlantAnalysis"
    """
    def GetName(self) -> str:
        return "PlantAnalysis"
    
    """
    Retrieves the pair of interface channel types that correspond to the I/O nature of this stage.
    
    Returns:
        A pair (a, b) where [a] is a DoubleImageChannel ID and [b] is a SnapshotChannel ID.
    """
    def GetInterfaceIDs(self) -> tuple:
        return (SegmentationChannel.CHANNEL_ID, SnapshotChannel.CHANNEL_ID)
    
    """
    Runs the PlantAnalysis Stage's processing unit on the given input channel from a previous stage.

    Parameters:
        inData - A SegmentationChannel containing the contours and masks to analyze.

    Returns:
        A pair (a, b) where [a] is the name of the Pipeline Stage (i.e., "PlantAnalysis") and [b] is an 
        empty SnapshotChannel, since all results are saved to disk.
    """
    def Invoke(self, inData: StageChannel) -> tuple:
        paInput = cast(SegmentationChannel, inData)
        print(len(paInput.masks))
        for i in range(0, len(paInput.masks)):
            pImg = pcv.analyze_object(paInput.rgb, obj=paInput.contours[i], mask=paInput.masks[i], label=i)
        outputFile = (self.cfg.outfile + "_" + paInput.tag.split("image_")[1].split("/")[-1].split(".")[0] + ".csv").replace(" ", "_").replace("-", "_")
        print("Saving results to", outputFile)
        pcv.outputs.save_results(filename=(outputFile), outformat=self.cfg.filetype)
        csv = pd.read_csv(outputFile)
        time = [paInput.tag.split("image_")[1].split("/")[-1].split(".")[0]]
        time = np.repeat(time, len(paInput.masks) * 18)
        csv['timestamp'] = time
        try:
            csv['timestamp'] = pd.to_datetime(csv['timestamp'], format="%Y-%m-%d %H_%M_%S")
        except ValueError:
            csv['timestamp'] = pd.to_datetime(csv['timestamp'], format="%Y-%m-%d %H-%M-%S")
        csv.to_csv(outputFile)
        return (self.GetName(), SnapshotChannel([]))