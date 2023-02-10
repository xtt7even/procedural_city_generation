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


from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, GeomNode, LPoint3d, GeomTristrips, CSZupRight, LVector3f
from panda3d.egg import EggCoordinateSystem, EggData, EggVertexPool, EggVertex, EggPolygon


def updateWindingOrder(tri,points):
    """for i in range(len(tri) - 1):
        v1 = points[tri[i]]
        v2 = points[tri[i+1]]

        if (v1[0] - v2[0] < 0 or
            v1[1] - v2[1] < 0 or
            v1[2] - v[2] < 0):
            tmp = tri[i]
            tri[i] = tri[i+1]
            tri[i+1] = tmp
    return tri
    """
    v = LVector3f(0,0,1)

    for i in range(len(tri) - 2):
        a = LVector3f(points[tri[i]][0],points[tri[i]][1],points[tri[i]][2])
        b = LVector3f(points[tri[i+1]][0],points[tri[i+1]][1],points[tri[i+1]][2])
        c = LVector3f(points[tri[i+2]][0],points[tri[i+2]][1],points[tri[i+2]][2])
        n = (b-a).cross(c-a)
        w = n.dot(a-v)
    if w < 0:
        return tri
    else:
        return reversed(tri)

def fromPyDataEgg(points,triangles):

    z_up = EggCoordinateSystem()
    z_up.setValue(CSZupRight)

    data = EggData()
    data.addChild(z_up)

    vp = EggVertexPool('fan')
    data.addChild(vp)

    vertices = {}

    i = 0
    for p in points:
        v = EggVertex()
        v.setPos(LPoint3d(p[0], p[1], p[2]))
        v.setNormal((0,0,1))
        vp.addVertex(v)
        vertices[i] = v
        i+=1

    for t in triangles:
        poly = EggPolygon()
        t = updateWindingOrder(t,points)
        for v in t:
            poly.addVertex(vertices[v])

        data.addChild(poly)

    data.writeEgg('test.egg')
    loader.loadModel('test.egg').reparentTo(render)


def fromPyData(points,triangles):
    vdata = GeomVertexData('vertices',GeomVertexFormat.getV3n3t2(),Geom.UHStatic)
    vdata.setNumRows(len(points))
    vertexWriter = GeomVertexWriter(vdata,'vertex')
    normalWriter = GeomVertexWriter(vdata,'normal')
    texcoordWriter = GeomVertexWriter(vdata,'texcoord')
    #TODO color?
    for p in points:
        vertexWriter.addData3(p[0],p[1],p[2])
        normalWriter.addData3(0,0,1)
        #TODO texcoord

    gnode = GeomNode('gnode')
    geom = Geom(vdata)

    i = 1
    n = 0

    for t in triangles:
        prim = GeomTristrips(Geom.UHStatic)
        #prim.addVertex(t[0])
        #prim.addVertex(t[1])
        #prim.addVertex(t[2])
        t = updateWindingOrder(t,points)
        for v in t:
            prim.addVertex(v)
        prim.closePrimitive()
        geom.addPrimitive(prim)

        if geom.getNumPrimitives() > 2000:
            gnode.addGeom(geom)
            i+=1
            geom = Geom(vdata)

    render.attachNewNode(gnode)
    #TODO Texturing
    #TODO GeoMip ???


def createGround(points, triangles):
    fromPyDataEgg(points,triangles)
    

def createBuilding(verts,faces,texname,texscale,shrinkwrap):
    #MESH
    fromPyDataEgg(verts,faces)



def createBuildings(polygons):
    for polygon in polygons:
        verts = polygon[0]
        faces = polygon[1]
        texname = polygon[2]
        texscale = polygon[3]
        shrinkwrap = polygon[4]
        createBuilding(verts,faces,texname,texscale,shrinkwrap)


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

    """points = []
    triangles = []
    for i in range(0,10):
        for j in range(0,10):
            points.append([10 * i,10*j,0])


    for i in range(0,9):
        for j in range(0,9):
            tri1 = [i * 10 + j, i*10 + j + 1 , (i+1)*10 + j + 1]
            tri2 = [i * 10 + j, (i+1) * 10 + j, (i+1) * 10 + j + 1]
            triangles.append(tri1)
            triangles.append(tri2)"""

    createGround(points,triangles)
    #createBuildings(polygons)
