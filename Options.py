from typing import NamedTuple

"""
Represnts a configuration for the application.
"""
class Options(NamedTuple):
    image: str = "/Users/alex/Desktop/pipeline/images/image_2023-02-13 16_52_27.jpg"
    segname: str = "image_pid_"
    debug: str = "plot"
    visualize: bool = True
    writeimg: bool = True
    result: str = "multi_plant_tutorial_results_ffp.csv"
    outdir: str = "./"