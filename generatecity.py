import subprocess
import matplotlib
matplotlib.use("QT4Agg")

from procedural_city_generation.roadmap import main as roadmap_main
from procedural_city_generation.polygons import main as polygons_main
from procedural_city_generation.building_generation import main as building_generation_main
from procedural_city_generation.additional_stuff.Singleton import Singleton

roadmap_main.main()
Singleton("roadmap").kill()

polygons_main.main(None)
Singleton("polygons").kill()

building_generation_main.main()
Singleton("building_generation").kill()
# os.chdir("/citygenlib/procedural_city_generation/procedural_city_generation/visualization/")


# Run the script using subprocess
import subprocess

# Define the path to the Blender executable
blender_executable_path = '../blender_335/blender.exe'

# Define the path to your script
script_path = 'E:/SelfEducation/programming/Websites/CityGeneration/citygenlib/procedural_city_generation/procedural_city_generation/visualization/blenderize.py'

# Construct the command to be executed
command = [blender_executable_path, '--background', '--python', script_path]

# Execute the command
try:
    subprocess.run(command, check=True)
    print("Blender script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to execute Blender script: {e}")