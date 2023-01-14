import numpy as np
import os

class export():
    def __init__(self, name, path): # add volute according to data type and shape
        """Create DXF file from point cloud

        Args:
            name (str): name of the DXF file
            path (str): path of the folder to save the DXF file
        """
        #self.A = volute.A
        #self.B = volute.B
        #self.C = volute.C
        #self.ProjectA = volute.A-[0, 0, volute.A.z] #Projection de la ligne A sur le plan xy
        #self.ProjectC = volute.C-[0, 0, volute.C.z] #Projection de la ligne C sur le plan xy
        self.name = name
        self.path = path
        #self.PAA = volute.A-self.ProjectA
        #self.BC = volute.C-volute.B

    def Export2DXF(self):
        """Export to DXF file
        """
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
            #Write_Arc(volute.a[i], volute.b[i], self.PAA[i], self.BC[i])
        self.f.write("ENDSEC\n")
        self.f.write("0\n")

    def Write_Line(self, Start_point, End_point):
        x=Start_point.x
        y=Start_point.y
        z=Start_point.z
        xprim=End_point.x
        yprim=End_point.y
        zprim=End_point.z
        self.f.write("LINE\n")
        self.f.write("10\n")
        self.f.write(str(x)+"\n")
        self.f.write("20\n")
        self.f.write(str(y)+"\n")
        self.f.write("30\n")
        self.f.write(str(z)+"\n")
        self.f.write("11\n")
        self.f.write(str(xprim)+"\n")
        self.f.write("21\n")
        self.f.write(str(yprim)+"\n")
        self.f.write("31\n")
        self.f.write(str(zprim)+"\n")
        self.f.write("0\n")
    
    def Write_Arc(self, Start_point, End_point, V, Vprim):
        x = Start_point.x
        y = Start_point.y
        z = Start_point.z
        xprim = End_point.x
        yprim = End_point.y
        zprim = End_point.z
        A = np.matrix([[2*(x-xprim), 2*(y-yprim), 2*(z-zprim)],
                       [V[0], V[1], V[2]],
                       [Vprim[0], Vprim[1], Vprim[2]]])
        C = np.matrix([[x**2-xprim**2+y**2-yprim**2+z**2-zprim**2], [V[0]*x + V[1]*y + V[2]*z], [Vprim[0]*xprim + Vprim[1]*yprim + zprim*Vprim[2]]])
        CenterPoint = np.linalg.inv(A)*C # Position dans le WCS du centre de l'arc tangent aux deux droites
        Radius = np.linalg.norm(CenterPoint-np.array([x, y, z]))
        Ez = np.linalg.cross(CenterPoint-np.array([x, y, z]), CenterPoint-np.array([xprim, yprim, zprim]))/np.linalg.norm(np.linalg.cross(CenterPoint-np.array([x, y, z]), CenterPoint-np.array([xprim, yprim, zprim])))
        if (abs(Ez[0]) < 1/64.) and (abs(Ez[1]) < 1/64.):
            v = np.cross(np.array([0, 1, 0]), Ez)
            Ex = v/np.linalg.norm(v)  # the cross-product operator
        else:
            v=np.cross(np.array([0, 0, 1]), Ez)
            Ex = v/np.linalg.norm(v)  # the cross-product operator
        Ey = np.cross(Ez,Ex)/np.linalg.norm(np.cross(Ez,Ex))
        self.Wx = self.wcs_to_ocs((1, 0, 0), Ex, Ey, Ez)
        self.Wy = self.wcs_to_ocs((0, 1, 0), Ex, Ey, Ez)
        self.Wz = self.wcs_to_ocs((0, 0, 1), Ex, Ey, Ez)
        CenterPointOCS=self.wcs_to_ocs(CenterPoint, Ex, Ey, Ez)

        Start_Angle = np.arccos(np.dot(CenterPointOCS+Ex, np.array([x, y, z])+CenterPointOCS))*180/np.pi
        End_Angle=180
        ###### Calculer l'arc (position centre, rayon, angle de début et de fin aisni que la direction d'extrusion) \n
        ###### sachant qu'il est tangent à deux droites et connaissant ses deux points d'accroches.
        ###### Faire les calculs ci-dessus######
        self.f.write("LINE\n")
        self.f.write("10\n")
        self.f.write(str(CenterPointOCS[0])+"\n")
        self.f.write("20\n")
        self.f.write(str(CenterPointOCS[1])+"\n")
        self.f.write("30\n")
        self.f.write(str(CenterPointOCS[2])+"\n")
        self.f.write("40\n")
        self.f.write(str(Radius)+"\n")
        self.f.write("50\n")
        self.f.write(str(Start_Angle)+"/n")
        self.f.write("51\n")
        self.f.write(str(End_Angle)+"/n")
        self.f.write("210\n")
        self.f.write(str(Ez[0])+"\n")
        self.f.write("220\n")
        self.f.write(str(Ez[1])+"/n")
        self.f.write("230\n")
        self.f.write(str(Ez[2])+"/n")
        self.f.write("0\n")

    def wcs_to_ocs(self, P, Ex, Ey, Ez):
        """
        Convert WCS to OCS coordinates of a point
        
        Attributes
        ----------
        P: 
            (X,Y,Z) in WCS coordinates of the point
        
        Returns
        -------
        Point:
            (X,Y,Z) coordinates (OCS) of the point
        """
        px, py, pz = P[0], P[1], P[2]
        x = px * Ex[0] + py * Ex[1] + pz * Ex[2]
        y = px * Ey[0] + py * Ey[1] + pz * Ey[2]
        z = px * Ez[0] + py * Ez[1] + pz * Ez[2]
        return np.array([x, y, z])

    def ocs_to_wcs(self, P):
        """
        Convert OCS to WCS coordinates of a point
        
        Attributes
        ----------
        P: 
            (X,Y,Z) in OCS coordinates of the point
        
        Returns
        -------
        Point:
            (X,Y,Z) coordinates (WCS) of the point
        """
        px, py, pz = P[0], P[1], P[2]
        x = px * self.Wx[0] + py * self.Wx[1] + pz * self.Wx[2]
        y = px * self.Wy[0] + py * self.Wy[1] + pz * self.Wy[2]
        z = px * self.Wz[0] + py * self.Wz[1] + pz * self.Wz[2]
        return np.array([x, y, z])

try :
    os.remove(r"/Users/yvan/Desktop/Venture Orbital System/Export_2_DXF/Test.dxf")
except:
    None
E=export("Test.dxf", r"/Users/yvan/Desktop/Venture Orbital System/Export_2_DXF")
E.Export2DXF()