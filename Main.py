from plantcv import plantcv as pcv
from Options import Options
from Loader import DataLoader
from Pipeline import Pipeline, PipelineConfig
from Stage import WhiteBalance, ViewportAdjust, BinaryMask, Consolidation, RigidSegmentation, DBSCANSegmentation, PlantAnalysis
from StageConfig import WhiteBalanceConfig, ViewportAdjustConfig, BinaryMaskConfig, ConsolidationConfig, RigidSegmentationGridConfig, RigidSegmentationCustomConfig, DBSCANSegmentationConfig, PlantAnalysisConfig
from StageChannel import DoubleImageChannel

##########################################################
# Data Loading                                           #
##########################################################

#units_2 = DataLoader.LoadDir("/Users/alex/Desktop/SubII/")
units_3a = DataLoader.LoadDir("/Users/alex/Desktop/test_3/")
#units_3b = DataLoader.LoadDir("/Users/alex/Desktop/Moved_3/")

##########################################################
# Shared PlantCV Stage Constructions                     #
##########################################################

#pcv.params.debug = "plot"

# Stage I
wb = WhiteBalance(WhiteBalanceConfig(roi=(220, 87, 60, 10)))

# Stage II
va = ViewportAdjust(ViewportAdjustConfig(side='top', rotate=1, shift=70))

# Stage III
bm = BinaryMask(BinaryMaskConfig(threshold=135, mx=255, obj='light', fill=200, channel='b'))

# Stage VI
analysis = PlantAnalysis(PlantAnalysisConfig(filetype='csv', outfile='/Users/alex/Desktop/CSV_DATA/DBSCAN/3a/data'))

##########################################################
#  Rigid Stage Constructions                             #
##########################################################

# Stage IV
cs_A = Consolidation(ConsolidationConfig(stageNames=[va.GetName(), bm.GetName()], outChannelId=DoubleImageChannel.CHANNEL_ID))
cs_B = Consolidation(ConsolidationConfig(stageNames=[wb.GetName(), bm.GetName()], outChannelId=DoubleImageChannel.CHANNEL_ID))
cs_C = Consolidation(ConsolidationConfig(stageNames=["Disk", bm.GetName()], outChannelId=DoubleImageChannel.CHANNEL_ID))

# Stage V(a)
rSeg_2 = RigidSegmentation(RigidSegmentationGridConfig(start=(70, 150), radius=30, spacing=(90,90), rows=4, cols=7, roiType='partial'))
rSeg_3a = RigidSegmentation(RigidSegmentationCustomConfig(centers=[(139, 205), (220, 200), (306, 194), (407, 190), 
                                                                   (496, 182), (350, 254), (140, 324), (226, 317), 
                                                                  (310, 311), (415, 307), (503, 306)], radius=15))
rSeg_3b = RigidSegmentation(RigidSegmentationCustomConfig(centers=[(107, 200), (189, 196), (279, 192), (383, 186), 
                                                                  (463, 175), (322, 246), (119, 319), (205, 309), 
                                                                  (288, 313), (392, 307), (481, 297)], radius=15))

# Stage V(b)
segDB = DBSCANSegmentation(DBSCANSegmentationConfig(minClusterSize=5, epsilon=0.059))

##########################################################
#  Pipeline Configurations and Constructions             #
##########################################################

options = Options() # General options the same

# Rigid Configuration (ideally: const PipelineConfig *const)
rCfg_2 = PipelineConfig(options, [wb, va, bm, cs_A, rSeg_2, analysis])
rCfg_3a = PipelineConfig(options, [wb, bm, cs_B, rSeg_3a, analysis])
rCfg_3b = PipelineConfig(options, [wb, bm, cs_B, rSeg_3b, analysis])

# Pipeline objects
r_pipe_2 = Pipeline(rCfg_2)        # For Lettuce Trial 1
r_pipe_3a = Pipeline(rCfg_3a)      # For Lettuce Trial 2 (prior to 4/20)
r_pipe_3b = Pipeline(rCfg_3b)      # For Lettuce Trial 2 (post 4/20)

# DBSCAN
dbscanCfg = PipelineConfig(options, [bm, cs_C, segDB, analysis])
db_pipe = Pipeline(dbscanCfg)      # Suitable for all Trials

##########################################################
#  Pipeline Execution                                    #
##########################################################

#r_pipe_2.FormatSet(units_2)
r_pipe_3a.FormatSet(units_3a)
#r_pipe_3b.FormatSet(units_3b)

#db_pipe.FormatSet(units_2)
#db_pipe.FormatSet(units_3a)
#db_pipe.FormatSet(units_3b)