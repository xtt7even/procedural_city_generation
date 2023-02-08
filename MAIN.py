from procedural_city_generation.additional_stuff.Singleton import Singleton

from procedural_city_generation.roadmap.main import main as roadmap_main
from procedural_city_generation.polygons.main import main as polygons_main
from procedural_city_generation.building_generation.main import main as building_generation_main



def generateCity():
    singleton = Singleton('roadmap')
    singleton.plot = False
    roadmap_main()
    singleton.kill()

    singleton = Singleton('polygons')
    singleton.plotbool = False
    polygons_main(None)
    singleton.kill()

    singleton = Singleton('building_generation')
    building_generation_main()
    singleton.kill()


def finalize():
    import pickle
    global path
    import os
    path=os.path.join(os.path.dirname(__file__),"procedural_city_generation")
    ### IF ON WINDOWS, OPEN THIS FILE WITH BLENDER AND OVERWRITE       ###
    ### FOLLOWING LINE WITH YOUR PATH AND UNCOMMENT THE FOLLOWING LINE ###
    # path = "/home/jonathan/procedural_city_generation/procedural_city_generation/"
    import json
    global conf_values

    with open(path+"/inputs/visualization.conf", 'r') as f:
        conf_values=json.loads(f.read())
    with open(path+"/temp/"+conf_values[u'input_name'][u'value']+"_heightmap.txt", 'r') as f:
        filename=f.read()
    with open(path+"/temp/"+filename, 'rb') as f:
        points, triangles = pickle.loads(f.read())

    with open(path+"/outputs/"+conf_values[u'input_name'][u'value']+".txt", 'rb') as f:
        polygons=pickle.loads(f.read())
    print(len(points), len(triangles), len(polygons))


from direct.showbase.ShowBase import ShowBase

class Generator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        generateCity()
        finalize()

generator = Generator()
generator.run()
