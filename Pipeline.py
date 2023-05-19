from sys import stderr
from typing import NamedTuple, cast
from plantcv import plantcv as pcv
from DataTypes import DataUnit, FormattedData
from Options import Options
from Stage import Consolidation
from StageChannel import SingleImageChannel, SnapshotChannel, DoubleImageChannel, SegmentationChannel

"""
A struct that represents a single Pipeline.

Used to indicate in what fashion the application should react
while running the pipeline itself, such as debug mode or previewing
intermiediate graphs, as well as what processing stages make up
this particular pipeline.
"""
class PipelineConfig(NamedTuple):
     """General application operating procedures while running the Pipeline."""
     options: Options

     """Ordered list of procesing stages that the data will get linearly passed throughly."""
     stages: list # Stage

"""
Functional equivalent to a [PipelineConfig] that carries out the processing of 
collection event data (in the form of DataUnit objects).
"""
class Pipeline(object):
     """
     Construct a new Piepline according the configuration in [cfg], so long as
     there is compatibility.
     
     Parameters:
        cfg - The configuration for this Pipeline to follow when run with [Format].

     Note:
        This constructor self-aborts the application in the event that the given
        configuration is determined to be incompatible. See [IsCompatible] for
        what constitutes a valid configuration.
     """
     def __init__(self, cfg: PipelineConfig):
        if not self.IsCompatible(cfg.stages):
            print("This pipeline configuration is incompatible!", file=stderr)
            exit(2)
        self.cfg = cfg # PipelineConfig

     """
     
     """
     def IsCompatible(self, stages: list) -> bool:
         curr = stages[0]
         cIds = curr.GetInterfaceIDs()
         for i in range(1, len(stages)):
             nxt = stages[i]
             nIds = nxt.GetInterfaceIDs()
             if (nIds[0] != SnapshotChannel.CHANNEL_ID and cIds[1] != nIds[0]):
                return False
             curr = nxt
             cIds = curr.GetInterfaceIDs()
         return True
       
     """
     Passes the DataUnit through the Pipeline and returns the processed data.

     Parameters:
        data - The DataUnit to process with the current pipeline
               configuration.

     Returns:
        The FormattedData equivalent for the [data] DataUnit after
        being passed through this Pipeline with the current configuration.
     """
     def Format(self, data: DataUnit) -> FormattedData:
        print("Processing ", data.meta.rgbFile)
        if not data.raw.valid:
            return 0
        inData = SingleImageChannel(data.raw.rgb)
        intmed = [("Disk", data)] # Used to keep track of Output channels throughout
        for stage in self.cfg.stages:
            if stage.GetInterfaceIDs()[0] == SnapshotChannel.CHANNEL_ID:
                inData = SnapshotChannel(intmed)
            out = stage.Invoke(inData)
            intmed.append(out)
            inData = out[1] # Output channel this iteration is input channel for the next
        return FormattedData(base=data.raw, proc=intmed)
        
     """
     List equivalent of [Format].
     
     Parameters:
        data - A list of DataUnit instances to process with
        the configuration assigned to this pipeline in the 
        constructor.
        
     Returns:
        A list of FormattedData objects that represent the
        evolution of the initial DataUnit's RawData entry over
        the course of the pipeline. Note that each FormattedData
        instance contains multiple StageEntry instances, so there
        is a 1-to-1 correlation between a DataUnit and an entry
        in the returned list.
     """
     def FormatSet(self, data: list) -> list:
        done = []
        i = 0
        for unit in data:
            print("Loading image", i, "of", len(data) - 1, "...")
            i = i + 1
            # TODO Error condition invalid data
            done.append(self.Format(unit))
        return done
