import numpy as np
import os

class export():
    def __init__(self, name, path): # add volute according to data type and shape
        #self.A = volute.A
        #self.B = volute.B
        #self.C = volute.C
        self.name = name
        self.path = path

    def Export2DXF(self):
        self.Create_DXF_File()
        self.Write_Header()
        self.Write_Sections()

    def Create_DXF_File(self):
        self.f=open(self.path+"/"+self.name, "x")
        self.f.write("0\n")

    def Write_Header(self):
        self.f.write("SECTION\n")
        self.f.write("2\n")
        self.f.write("HEADER\n")
        self.f.write("9\n")
        self.f.write("$DIMAUNIT\n")
        self.f.write("70\n")
        self.f.write("$DIMLUNIT\n")
        self.f.write("70\n")
        self.f.write("$INSUNITS\n")
        self.f.write("70\n")
        self.f.write("4\n")
        self.f.write("0\n")

    def Write_Sections(self):
        self.f.write("SECTION\n")
        self.f.write("2\n")
        self.f.write("ENTITIES\n")
        #... ajouter boucle de line et arc
        # for i in range (Nb_points):
            #Write_Line(volute.b[i], volute.c[i])
            #Write_Arc(volute.a[i], volute.b[i])
        self.f.write("ENDSEC\n")
        self.f.write("0\n")

    def Write_Line(self, Start_point, End_point):
        self.f.write("LINE\n")
        self.f.write("10\n")
        self.f.write(str(Start_point.x)+"\n")
        self.f.write("20\n")
        self.f.write(str(Start_point.y)+"\n")
        self.f.write("30\n")
        self.f.write(str(Start_point.z)+"\n")
        self.f.write("11\n")
        self.f.write(str(End_point.x)+"\n")
        self.f.write("21\n")
        self.f.write(str(End_point.y)+"\n")
        self.f.write("31\n")
        self.f.write(str(End_point.z)+"\n")
        self.f.write("0\n")
    
    def Write_Arc(self, Start_point, End_point):
        CenterPoint=1
        Radius=2
        Start_Angle=0
        End_Angle=180
        D_extr=[0,0,1]
        ###### Calculer l'arc (position centre, rayon, angle de début et de fin aisni que la direction d'extrusion) \n
        ###### sachant qu'il est tangent à deux droites et connaissant ses deux points d'accroches.
        ###### Faire les calculs ci-dessus######
        self.f.write("LINE\n")
        self.f.write("10\n")
        self.f.write(str(CenterPoint.x)+"\n")
        self.f.write("20\n")
        self.f.write(str(CenterPoint.y)+"\n")
        self.f.write("30\n")
        self.f.write(str(CenterPoint.z)+"\n")
        self.f.write("40\n")
        self.f.write(str(Radius)+"\n")
        self.f.write("50\n")
        self.f.write(str(Start_Angle)+"/n")
        self.f.write("51\n")
        self.f.write(str(End_Angle)+"/n")
        self.f.write("210\n")
        self.f.write(str(D_extr[0])+"\n")
        self.f.write("220\n")
        self.f.write(str(D_extr[1])+"/n")
        self.f.write("230\n")
        self.f.write(str(D_extr[2])+"/n")
        self.f.write("0\n")



os.remove(r"/Users/yvan/Desktop/Venture Orbital System/Export_2_DXF/Test.dxf")
E=export("Test.dxf", r"/Users/yvan/Desktop/Venture Orbital System/Export_2_DXF")
E.Export2DXF()