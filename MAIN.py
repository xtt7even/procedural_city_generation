from procedural_city_generation.additional_stuff.Singleton import Singleton

from procedural_city_generation.roadmap.main import main as roadmap_main
from procedural_city_generation.polygons.main import main as polygons_main
from procedural_city_generation.building_generation.main import main as building_generation_main



singleton = Singleton('roadmap')
roadmap_main()
singleton.kill()

singleton = Singleton('polygons')
polygons_main(None)
singleton.kill()

singleton = Singleton('building_generation')
building_generation_main()
singleton.kill()
