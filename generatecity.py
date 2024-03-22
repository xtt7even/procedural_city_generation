import subprocess
import matplotlib
import os
import subprocess

matplotlib.use("QT4Agg")

from procedural_city_generation.roadmap import main as roadmap_main
from procedural_city_generation.polygons import main as polygons_main
from procedural_city_generation.building_generation import main as building_generation_main
from procedural_city_generation.additional_stuff.Singleton import Singleton

#Generate everything in the city
roadmap_main.main()
Singleton("roadmap").kill()

polygons_main.main(None)
Singleton("polygons").kill()

building_generation_main.main()
Singleton("building_generation").kill()

# To make it work you need to have a blender 3.x.x outide of the procedural_city_generation folder
# Enter your correct path below
blender_executable_path = '../blender_335/blender.exe'

# Define the path to your script
script_path = os.getcwd() + '/procedural_city_generation/visualization/blenderize.py'

# Construct the command to be executed
command = [blender_executable_path, '--background', '--python', script_path]

# Execute the command
try:
    subprocess.run(command, check=True)
    print("Blender script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to execute Blender script: {e}")