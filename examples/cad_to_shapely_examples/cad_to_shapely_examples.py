#%% setup
import os
# os.chdir(r'C:\dev\structural-analysis')

# import logging
# help(logging)
import matplotlib.pyplot as plt
from pprint import pp

#%%
import pyprojroot

help(pyprojroot)
print(pyprojroot.__all__)
print(pyprojroot.here())
os.chdir(pyprojroot.here())
#%%
# import sdxf
# help(sdxf)

import cad_to_shapely
dir(cad_to_shapely)
help(cad_to_shapely)
import cad_to_shapely.dxf as dxf
dir(dxf)
help(dxf)
#%%

import cad_to_shapely.utils as utils
help(utils)
dir(utils)

def import_dxf_example1(dxf_filepath : str, force_zip = False):
    """
    for debugging. just plots geometry with no polygon-making
    """
    my_dxf = dxf.DxfImporter(dxf_filepath)
    my_dxf.process(spline_delta = 0.1)

    print(f'Units are {my_dxf.units}')

    for g in my_dxf.geometry:
        x,y = g.xy
        plt.plot(x,y)

    file_png= f"img/{os.path.splitext(os.path.basename(dxf_filepath))[0]}.png"
    plt.savefig(file_png)
    plt.show()
    

def import_dxf_example2(dxf_filepath: str,force_zip = False):

    assert os.path.exists(dxf_filepath), f"File not found: {dxf_filepath}"
    my_dxf = dxf.DxfImporter(dxf_filepath)
    my_dxf.process(spline_delta = 0.1)

    print(f'Units are {my_dxf.units}')
    my_dxf.polygonize(
        force_zip = force_zip
    )
    
    polygons = my_dxf.polygons
    print (f"Found {len(polygons)} polygons")


    polygons = utils.filter_polygons(polygons,filter_flag=1)

    for p in polygons:
        x,y = p.exterior.xy

        plt.plot(x,y)
        for hole in p.interiors:
            x,y = hole.xy
            plt.plot(x,y)

        for i in range(100):
            pts=  utils.point_in_polygon(p)
            x,y = pts.xy
            plt.plot(x, y, marker='o', markersize=3, color="red")
 
    file_png= f"img/{os.path.splitext(filename)[0]}.png"
    plt.savefig(file_png)

    plt.show()

def import_dxf_example(dxf_filepath : str, force_zip = False):

    assert os.path.exists(dxf_filepath), f"File not found: {dxf_filepath}"
    help(dxf.DxfImporter)
    my_dxf = dxf.DxfImporter(dxf_filepath)
    my_dxf.process(spline_delta = 0.1)  
    print(f'Units are {my_dxf.units}')
    my_dxf.polygonize(
        force_zip = force_zip
    )

    polygons = my_dxf.polygons
    print (f"Found {len(polygons)} polygons")
    print(polygons)

    for p in polygons:
        x,y = p.exterior.xy
        plt.plot(x,y)
    plt.show()

    help(utils.find_holes)
    help(utils.filter_polygons)
    new = utils.find_holes(polygons)
    print(new)

    x,y = new.exterior.xy
    plt.plot(x,y)
    plt.show()
    print(new.interiors)
    for hole in new.interiors:
        print(hole)
        x,y = hole.xy
        plt.plot(x,y)
        plt.show()
 
    # for i in range(100):
    #     p=  utils.point_in_polygon(new)
    #     x,y = p.xy
    #     plt.plot(x, y, marker='o', markersize=3, color="red")

    plt.show()
    

#%%

if __name__ == "__main__":
    import os

    import cad_to_shapely

    pp(os.listdir(os.path.join(r'C:\repos\cad-to-shapely-master','example_files')))


    #logging.basicConfig(level = logging.DEBUG)
    # filename = "section_holes_complex1.dxf"
    #filename = "simplelines_from_solidworks.dxf"
    filename = "200ub22_R12dxf_linesandarcs.dxf"
    
    #straight from http://www.steelweb.info/200x100x6.htm
    #filename = "200x100x6.dxf"

    #filename = "test1.dxf"
    #filename = "three_different_sections.dxf"
   # filename = "tophat_circles_autocadlite.dxf"
   # filename = "test2.dxf"
    #filename = "test3.dxf"


    dxf_filepath = os.path.join(os.getcwd(),'example_files',filename)
    assert os.path.exists(dxf_filepath), f"File not found: {dxf_filepath}"

    import_dxf_example(dxf_filepath)