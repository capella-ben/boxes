#from IPython.display import SVG, display

import sys
#sys.path.append('..') # uncomments and adjust if your Boxes.py copy in not in the Python path
from boxes import *


class BENBOX(Boxes):
    """My Box Style"""

    ui_group = "Box"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(edges.GroovedSettings)
        self.buildArgParser("x", "y", "outside", bottom_edge="F")
        self.argparser.add_argument(
            "--heightBase", action="store", type=float, default=50,
            help="height base portion")
        self.argparser.add_argument(
            "--heightLid", action="store", type=float, default=50,
            help="height of the lid")
        self.argparser.add_argument(
            "--edge_types", action="store", type=str, default="eeee",
            help="which edges are flat (e) or grooved (z,Z), counter-clockwise from the front")
        self.argparser.add_argument(
            "--hingeHoleSize", action="store", type=float, default=2,
            help="Hole diameter for the hinge screws/rivets")
        self.argparser.add_argument(
            "--hingeEdgeOffset", action="store", type=float, default=3.9,
            help="The distance from the edge the hinge holes need to be")
        self.argparser.add_argument(
            "--hingeHoleSpacing", action="store", type=float, default=11,
            help="distance between the holes in the hinge")
        self.argparser.add_argument(
            "--hinge", action="store", type=bool, default=True,
            help="distance between the holes in the hinge")
        


    def render(self):

        x, y= self.x, self.y
        hb = self.heightBase
        hl = self.heightLid
        hgh = self.hingeHoleSize
        hgo = self.hingeEdgeOffset
        hgs = self.hingeHoleSpacing
        
        edge_types = self.edge_types
        if len(edge_types) != 4 or any(et not in "ezZ" for et in edge_types):
            raise ValueError("Wrong edge_types style: %s)" % edge_types)

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            hb = self.adjustSize(hb, self.bottom_edge, False)
            hl = self.adjustSize(hl, self.bottom_edge, False)
            extra = 0       # an extra distance that you sometimes need...
        else:
            extra = self.thickness

        #print(extra)


        t = self.thickness
        b = self.bottom_edge

        # base sides
        self.rectangularWall(x, hb, [b, "F", edge_types[0], "F"], move="right", label="Front Base")
        self.rectangularWall(y, hb, [b, "f", edge_types[1], "f"], move="right", label="Right Base")
        
        if self.hinge:
            #self.hole(x = 0, y=0, d=hgh)
            self.hole(x = self.x/4 + (hgh/2) + extra,         y=(hb + self.thickness) - hgo + (hgh/2), d=hgh)
            self.hole(x = self.x/4 - hgs + (hgh/2) + extra,   y=(hb + self.thickness) - hgo + (hgh/2), d=hgh)
            self.hole(x = self.x/4*3 + (hgh/2) + extra,       y=(hb + self.thickness) - hgo + (hgh/2), d=hgh)
            self.hole(x = self.x/4*3 + hgs + (hgh/2) + extra, y=(hb + self.thickness) - hgo + (hgh/2), d=hgh)
        self.rectangularWall(x, hb, [b, "F", edge_types[2], "F"], move="right", label="Back Base")
        self.rectangularWall(y, hb, [b, "f", edge_types[3], "f"], move="right", label="Left Base")

        with self.saved_context():
            if b != "e":
                self.rectangularWall(x, y, "ffff", move="up", label="Base")

            self.rectangularWall(x, y, "ffff", move="up", label='Lid')
            maxh = max([hb, hl])

        self.moveTo(0, maxh+self.heightLid+self.edges["F"].spacing()+self.edges[b].spacing()+1*self.spacing + extra, 180)
        edge_inverse = {"e": "e", "z": "Z", "Z": "z"}
        edge_types = [edge_inverse[et] for et in edge_types]

        self.rectangularWall(y, hl, "Ff" + edge_types[3] + "f", move="right", label="Left Lid")
        
        if self.hinge:
            #self.hole(x = 0, y=0, d=hgh)
            self.hole(x = self.x/4 + (hgh/2) + extra,         y=(hl + self.thickness) - hgo + (hgh/2), d=hgh)
            self.hole(x = self.x/4 - hgs + (hgh/2) + extra,   y=(hl + self.thickness) - hgo + (hgh/2), d=hgh)
            self.hole(x = self.x/4*3 + (hgh/2) + extra,       y=(hl + self.thickness) - hgo + (hgh/2), d=hgh)
            self.hole(x = self.x/4*3 + hgs + (hgh/2) + extra, y=(hl + self.thickness) - hgo + (hgh/2), d=hgh)
        self.rectangularWall(x, hl, "FF" + edge_types[2] + "F", move="right", label="Back Lid")
        
        self.rectangularWall(y, hl, "Ff" + edge_types[1] + "f", move="right", label="Right Lid")
        self.rectangularWall(x, hl, "FF" + edge_types[0] + "F", move="right", label="Front Lid")
        


if __name__ == "__main__":

    b = BENBOX()


    #fd, fn = tempfile.mkstemp()
    fn = 'benBox.svg'
    b.parseArgs(['--reference=0', '--debug=0', '--output=' + fn])
    b.thickness = 2.8
    b.tabs = 0
    b.burn = 0.1
    b.labels = False

    b.outside = True
    b.heightBase = 30
    b.heightLid = 15
    b.x = 190               # should be longest as it will have the hinge
    b.y = 70

    b.hinge=True
    b.hingeHoleSize = 1.8
    b.hingeEdgeOffset = 3.3
    b.hingeHoleSpacing = 11
    #b.lid = True
    b.edge_types = 'zeee'

    b.open()
    b.render()
    b.close()