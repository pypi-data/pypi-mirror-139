from tabulate import tabulate
from .bd import dbConductorCu, dbConductorAl, dbConductorCuStd
import numpy as np
import matplotlib.pyplot as plt
import math
import time


'''
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
| PYEWS, ElectricalWireSizes, 19/02/2022                                 |
| Version : 0.1.27rc2                                                    |
| Autor : Marco Polo Jacome Toss                                         |
| License: GNU Affero General Public License v3 (GPL-3.0)                |
| Requires: Python >=3.5                                                 |
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Las correcciones de este archivo se muestran en el control de cambios.

'''


def version():
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("                                                                          ")
    print("                         ─▄▀─▄▀")
    print("                         ──▀──▀")
    print("                         █▀▀▀▀▀█▄")
    print("                         █░░░░░█─█")
    print("                         ▀▄▄▄▄▄▀▀")
    print("                                                                          ")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("| Python ElectricalWireSizes, 19/12/2022                                 |")
    print("| Version : 0.1.27rc2                                                    |")
    print("| Autor : Marco Polo Jacome Toss                                         |")
    print("| License: GNU Affero General Public License v3 (GPL-3.0)                |")
    print("| Requires: Python >=3.5                                                 |")
    print("| PyPi : https://pypi.org/project/ElectricalWireSizes/                   |")
    print("| Donativos : https://ko-fi.com/jacometoss                               |")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")  

def Rn(Ra=None,T2=None):
    
    if(Ra==None or T2==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                          ▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Los parámetros no son correctos para el                 |")
        print("| módulo Rn(Ra,T2)                                        |")
        print("-----------------------------------------------------------")
        return
    
    Rb=(Ra/(234.5+75))*(234.5+T2)
    return Rb

def RnCd(Ra=None,T2=None):

    if(Ra==None or T2==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                          ▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Los parámetros no son correctos para el                 |")
        print("| módulo RnCd(Ra,T2)                                      |")
        print("-----------------------------------------------------------")
        return
    
    Rb=(Ra/(234.5+75))*(234.5+T2)
    return Rb

def Z(R,X,FP):
    Z=(R*FP+X*math.sin(math.acos(FP)))
    FN=1/((2*100)*((R*FP+X*math.sin(math.acos(FP)))/1000))
    FFN=1/((math.sqrt(3)*100)*((R*FP+X*math.sin(math.acos(FP)))/1000))
    FFFN=1/((math.sqrt(3)*100)*((R*FP+X*math.sin(math.acos(FP)))/1000))
    FFF=1/((math.sqrt(3)*100)*((R*FP+X*math.sin(math.acos(FP)))/1000))
    return [round(FN,4),round(FFN,4),round(FFFN,4),round(FFF,4),round(Z,4)]

def Rcd(R):
    Rcond=(R)
    PN=1/((2*100)*((Rcond)/1000))
    return [round(PN,4),round(Rcond,4)]

def dbc(conductor=None):

    if(conductor==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                          ▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Los parámetros no son correctos para el                 |")
        print("| módulo dbc(conductor)                                   |")
        print("-----------------------------------------------------------")
        return  

    if conductor ==1:
        print(tabulate(dbConductorCu, headers=["AWG/KCM","R(Ω/km)", "X (Ω/km)","R (Ω/km)","X (Ω/km)", "R (Ω/km)", "X (Ω/km)", "60°C", "75°C", "90°C", "S[mm²]"], tablefmt='psql'))
    elif conductor==2:
        print(tabulate(dbConductorAl, headers=["AWG/KCM","R(Ω/km)", "X (Ω/km)","R (Ω/km)","X (Ω/km)", "R (Ω/km)", "X (Ω/km)", "60°C", "75°C", "90°C","S[mm²]"], tablefmt='psql'))
    elif conductor==3:
        print(tabulate(dbConductorCuStd, headers=["AWG/KCM","R[A](Ω/km)", "R[B](Ω/km)","R[C](Ω/km)", "60°C", "75°C", "90°C","S[mm²]"], tablefmt='psql'))
    elif (conductor>3 or conductor<=0):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Por el momento tenemos únicamente tres opciones         |")
        print("| Cobre 1, Aluminio 2, Cobre CD                           |")
        print("-----------------------------------------------------------")        
    
def FCT(Ta=None):

    if(Ta==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Los parámetros no son correctos para el                 |")
        print("| módulo FCT(Ta)                                          |")
        print("-----------------------------------------------------------")
        return  

    if Ta >= 60:
        FT60=0.0
    else:
        FT60=round(math.sqrt((60-Ta)/(60-30)),3)
        return FT60
    if Ta >= 75:
        FT75=0.0
    else:
        FT75=round(math.sqrt((75-Ta)/(75-30)),3)
        return FT75
    if Ta >= 90:
        FT90=0.0
    else :
        FT90=round(math.sqrt((90-Ta)/(90-30)),3)
        return FT90

    
def zpucu(Type=None,Ta=None,Fp=None,View=None):

    if(Type==None or Ta==None or Fp==None or View==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Los parámetros no son correctos para el                 |")
        print("| módulo zpucu(Type,Ta,Fp,View)                           |")
        print("-----------------------------------------------------------")
        return 

    if Type==1:
    #Conductores en ducto de PVC
        Rj=1
        Xj=2
    elif Type==2:
    #Conductores en ducto de Alumunio
        Rj=3
        Xj=4
    elif Type==3:
    #Conductores en ducto de Acero
        Rj=5
        Xj=6
    #print(tabulate(datos))

    datos=[["14 AWG"],
        ["12 AWG"],
        ["10 AWG"],
        ["8 AWG"],
        ["6 AWG"],
        ["4 AWG"],
        ["2 AWG"],
        ["1/0 AWG"],
        ["2/0 AWG"],
        ["3/0 AWG"],
        ["4/0 AWG"],
        ["250 KCM"],
        ["300 KCM"],
        ["350 KCM"],
        ["400 KCM"],
        ["500 KCM"],
        ["600 KCM"],
        ["750 KCM"],
        ["1000 KCM"]]

    for i in range(len(dbConductorCu)):
        Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
        datos[i].append(Zunitaria[0])

    for i in range(len(dbConductorCu)):
        Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
        datos[i].append(Zunitaria[1])

    for i in range(len(dbConductorCu)):
        Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
        datos[i].append(Zunitaria[2])

    for i in range(len(dbConductorCu)):
        Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
        datos[i].append(Zunitaria[3])
        
    if (View ==1):    
        return print(tabulate(datos, headers=["AWG/KCM","1F/2H", "2F/3H","3F/3H","3F/4H"], tablefmt='psql'))
    elif (View==2):
        return  datos
    

def zpual(Type=None,Ta=None,Fp=None,View=None):

    if(Type==None or Ta==None or Fp==None or View==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                    ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                           ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                           ")
        print("-----------------------------------------------------------")
        print("| Los parámetros no son correctos para                    |")
        print("| el módulo zpual(Type,Ta,Fp,View)                        |")
        print("-----------------------------------------------------------")
        return     
    

    if Type==1:
    #Conductores en ducto de PVC
        Rj=1
        Xj=2
    elif Type==2:
    #Conductores en ducto de Alumunio
        Rj=3
        Xj=4
    elif Type==3:
    #Conductores en ducto de Acero
        Rj=5
        Xj=6
    #print(tabulate(datos))

    datos=[
    ["6 AWG"],
    ["4 AWG"],
    ["2 AWG"],
    ["1/0 AWG"],
    ["2/0 AWG"],
    ["3/0 AWG"],
    ["4/0 AWG"],
    ["250 KCM"],
    ["300 KCM"],
    ["350 KCM"],
    ["400 KCM"],
    ["500 KCM"],
    ["600 KCM"],
    ["750 KCM"],
    ["1000 KCM"]]

    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[0])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[1])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[2])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[3])
        
    if (View ==1):    
        return print(tabulate(datos, headers=["AWG/KCM","1F/2H", "2F/3H","3F/3H","3F/4H"], tablefmt='psql'))
    elif (View==2):
        return  datos 

    
def mbtcu(VF=None,VL=None,In=None,Nc=None,L=None,FA=None,Type=None,Ta=None,Vd=None,S=None,Fp=None,View=None,Fsc=None,To=None,Break=None):

    if(VF==None or VL==None or In==None or Nc==None or L==None or FA==None or Type==None or Ta==None or Vd==None or S==None or Fp==None or View==None or Fsc==None or To==None or Break==None):
        t = time.localtime()
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                             ")
        print("                 ",time.asctime(t))
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                                    ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                             ")
        print("--------------------------------------------------------------------")
        print("| Los parámetros no son correctos para el                          |")
        print("| módulo mbtcu(VF,VL,In,Nc,L,FA,Type,Ta,Vd,S,Fp,View,Fsc,To,Break) |")
        print("--------------------------------------------------------------------")
        return         

    if Ta >= 60:
        FT60=0.0
    else :
        FT60=round(math.sqrt((60-Ta)/(60-30)),3)

    if Ta >= 75:
        FT75=0.0
    else :
        FT75=round(math.sqrt((75-Ta)/(75-30)),3)


    if Ta >= 90:
        FT90=0.0
    else :
        FT90=round(math.sqrt((90-Ta)/(90-30)),3)



    SITM=[0,15,20,25,30,35,40,45,50,60,70,80,90,100,110,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000]


    if Type==1:
    #Conductores en ducto de PVC
        Rj=1
        Xj=2
    elif Type==2:
    #Conductores en ducto de Alumunio
        Rj=3
        Xj=4
    elif Type==3:
    #Conductores en ducto de Acero
        Rj=5
        Xj=6
    #print(tabulate(datos))

    In=(In)/Nc

    LIn=L*In
    
    datos=[["14 AWG"],
    ["12 AWG"],
    ["10 AWG"],
    ["8 AWG"],
    ["6 AWG"],
    ["4 AWG"],
    ["2 AWG"],
    ["1/0 AWG"],
    ["2/0 AWG"],
    ["3/0 AWG"],
    ["4/0 AWG"],
    ["250 KCM"],
    ["300 KCM"],
    ["350 KCM"],
    ["400 KCM"],
    ["500 KCM"],
    ["600 KCM"],
    ["750 KCM"],
    ["1000 KCM"]]

    

    #for i in range(len(dbConductor)):
    #datos[i].append(round(Rn(dbConductor[i][1],75),4))

    #for i in range(len(dbConductor)):
    #    datos[i].append(dbConductor[i][2])

    for i in range(len(dbConductorCu)):
         Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
         datos[i].append(Zunitaria[0])
         
    for i in range(len(dbConductorCu)):
         Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
         datos[i].append(Zunitaria[1])
         
    for i in range(len(dbConductorCu)):
         Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
         datos[i].append(Zunitaria[2])
         
    for i in range(len(dbConductorCu)):
         Zunitaria=Z(round(Rn(dbConductorCu[i][Rj],Ta),4),dbConductorCu[i][Xj],Fp)
         datos[i].append(Zunitaria[3])

    for i in range(len(dbConductorCu)):
         datos[i].append(dbConductorCu[i][7])

    for i in range(len(dbConductorCu)):
         datos[i].append(dbConductorCu[i][8])

    for i in range(len(dbConductorCu)):
         datos[i].append(dbConductorCu[i][9])


    for i in range(len(datos)):

        if S==1:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))
        
            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))
            
            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D1:

                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                    
            else:
                datos[i].append('Not')
                
            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
                    
                    
            
        elif S==2:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)

            if Vd > D2:

                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                

            else:
                datos[i].append('Not')
            
            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
                     
        
        elif S==3:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D3:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
                    
            else:
                datos[i].append('Not')

            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
                                    
        
        elif S==4:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D4:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=(In*Fsc))):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
            else:
                datos[i].append('Not')
                    
            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
    if View == 1:
        #Mostrar información en PSQL
        print(tabulate(datos, headers=["AWG/KCM","1F/2H", "2F/3H","3F/3H","3F/4H", "60", "75", "90","%Vd/1F", "%Vd/2F","%Vd/3F","%Vd/3F","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
    elif View == 2:
        #Mostrar la información en lista
        return datos
    

def mbtal(VF=None,VL=None,In=None,Nc=None,L=None,FA=None,Type=None,Ta=None,Vd=None,S=None,Fp=None,View=None,Fsc=None,To=None, Break=None):

    if(VF==None or VL==None or In==None or Nc==None or L==None or FA==None or Type==None or Ta==None or Vd==None or S==None or Fp==None or View==None or Fsc==None or To==None or Break==None):
        t = time.localtime()
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                             ")
        print("                 ",time.asctime(t))
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                                    ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                                    ")
        print("--------------------------------------------------------------------")
        print("| Los parámetros no son correctos para el                          |")
        print("| módulo mbtal(VF,VL,In,Nc,L,FA,Type,Ta,Vd,S,Fp,View,Fsc,To,Break) |")
        print("--------------------------------------------------------------------")
        return 

    if Ta >= 60:
        FT60=0.0
    else :
        FT60=round(math.sqrt((60-Ta)/(60-30)),3)

    if Ta >= 75:
        FT75=0.0
    else :
        FT75=round(math.sqrt((75-Ta)/(75-30)),3)


    if Ta >= 90:
        FT90=0.0
    else :
        FT90=round(math.sqrt((90-Ta)/(90-30)),3)



    SITM=[0,15,20,25,30,35,40,45,50,60,70,80,90,100,110,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000]


    if Type==1:
    #Conductores en ducto de PVC
        Rj=1
        Xj=2
    elif Type==2:
    #Conductores en ducto de Alumunio
        Rj=3
        Xj=4
    elif Type==3:
    #Conductores en ducto de Acero
        Rj=5
        Xj=6
    #print(tabulate(datos))

    In=In/Nc

    LIn=L*In*Fsc
    
    datos=[
    ["6 AWG"],
    ["4 AWG"],
    ["2 AWG"],
    ["1/0 AWG"],
    ["2/0 AWG"],
    ["3/0 AWG"],
    ["4/0 AWG"],
    ["250 KCM"],
    ["300 KCM"],
    ["350 KCM"],
    ["400 KCM"],
    ["500 KCM"],
    ["600 KCM"],
    ["750 KCM"],
    ["1000 KCM"]]

    

    #for i in range(len(dbConductor)):
    #datos[i].append(round(Rn(dbConductor[i][1],75),4))

    #for i in range(len(dbConductor)):
    #    datos[i].append(dbConductor[i][2])

    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[0])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[1])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[2])
         
    for i in range(len(dbConductorAl)):
         Zunitaria=Z(round(Rn(dbConductorAl[i][Rj],Ta),4),dbConductorAl[i][Xj],Fp)
         datos[i].append(Zunitaria[3])

    for i in range(len(dbConductorAl)):
         datos[i].append(dbConductorAl[i][7])

    for i in range(len(dbConductorAl)):
         datos[i].append(dbConductorAl[i][8])

    for i in range(len(dbConductorAl)):
         datos[i].append(dbConductorAl[i][9])


    for i in range(len(datos)):

        if S==1:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))
        
            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))
            
            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D1:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                    
            else:
                datos[i].append('Not')
                
            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
                    
                    
            
        elif S==2:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)

            if Vd > D2:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
            else:
                datos[i].append('Not')
            
            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
                     

                    
        
        elif S==3:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D3:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
                    
            else:
                datos[i].append('Not')

            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
                                    
        
        elif S==4:
            
            D1=LIn/(datos[i][1]*VF)
            datos[i].append(round(D1,3))

            D2=LIn/(datos[i][2]*VF)
            datos[i].append(round(D2,3))

            D3=LIn/(datos[i][3]*VL)
            datos[i].append(round(D3,3))

            D4=LIn/(datos[i][4]*VL)
            datos[i].append(round(D4,3))

            datos[i].append(Nc)
            datos[i].append(round(In,2))
            
            datos[i].append(round(datos[i][5],3)*FA*FT60)
            datos[i].append(round(datos[i][6],3)*FA*FT75)
            datos[i].append(round(datos[i][7],3)*FA*FT90)
            
            if Vd > D4:
                
                if (To==60):

                    if ((round(datos[i][5],3)*FA*FT60>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')

                elif (To==75):

                    if ((round(datos[i][6],3)*FA*FT75>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')


                elif (To==90):
                    
                    if ((round(datos[i][7],3)*FA*FT90>=In)):
                        datos[i].append('Yes')
                    else:
                        datos[i].append('Not')
                        
            else:
                datos[i].append('Not')
                    
            for j in range(len(SITM)):
                if (SITM[j]>=Nc*In*Break):
                    datos[i].append(SITM[j])
                    break
    if View == 1:
        #Mostrar información en PSQL
        print(tabulate(datos, headers=["AWG/KCM","1F/2H", "2F/3H","3F/3H","3F/4H", "60", "75", "90","%Vd/1F", "%Vd/2F","%Vd/3F","%Vd/3F","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
    elif View == 2:
        #Mostrar la información en lista
        return datos
##-----------------------------------------------------------------------------------------------------------##
def mbtcustd(Vcd=None,In=None,Nc=None,L=None,Class=None,Ta=None,Vd=None,View=None,Fsc=None, To=None, Break=None):

    if(Vcd==None or In==None or Nc==None or L==None or Class==None or Ta==None or Vd==None or View==None or Fsc==None or To==None or Break==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                      ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                             ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                             ")
        print("-------------------------------------------------------------")
        print("| Los parámetros no son correctos                           |")
        print("| para el módulo mbtcustd(Vcd,In,Nc,L,Class,Ta,Vd,View,Fsc) |")
        print("-------------------------------------------------------------")
        return  

    if Ta >= 60:
        FT60=0.0
    else :
        FT60=round(math.sqrt((60-Ta)/(60-30)),3)

    if Ta >= 75:
        FT75=0.0
    else :
        FT75=round(math.sqrt((75-Ta)/(75-30)),3)

    if Ta >= 90:
        FT90=0.0
    else :
        FT90=round(math.sqrt((90-Ta)/(90-30)),3)



    SITM=[0,15,20,25,30,35,40,45,50,60,70,80,90,100,110,125,150,175,200,225,250,300,350,400,450,500,600,700,800,1000,1200,1600,2000,2500,3000,4000,5000,6000]


    if Class==1:
    #Conductores en ducto de PVC
        Rj=1
    elif Class==2:
    #Conductores en ducto de Alumunio
        Rj=2
    elif Class==3:
    #Conductores en ducto de Acero
        Rj=3
    #print(tabulate(datos))

    In=(In)/Nc

    LIn=L*In
    
    datos=[["14 AWG"],
    ["12 AWG"],
    ["10 AWG"],
    ["8 AWG"],
    ["6 AWG"],
    ["4 AWG"],
    ["2 AWG"],
    ["1/0 AWG"],
    ["2/0 AWG"],
    ["3/0 AWG"],
    ["4/0 AWG"],
    ["250 KCM"],
    ["300 KCM"],
    ["350 KCM"],
    ["400 KCM"],
    ["500 KCM"],
    ["600 KCM"],
    ["700 KCM"],
    ["750 KCM"],
    ["800 KCM"],
    ["900 KCM"],
    ["1000 KCM"],
    ["1250 KCM"],
    ["1500 KCM"],
    ["1750 KCM"],
    ["2000 KCM"]]

    

    #for i in range(len(dbConductor)):
    #datos[i].append(round(Rn(dbConductor[i][1],75),4))

    #for i in range(len(dbConductor)):
    #    datos[i].append(dbConductor[i][2])

    for i in range(len(dbConductorCuStd)):
         Runitaria=Rcd(round(RnCd(dbConductorCuStd[i][Rj],Ta),4))
         datos[i].append(Runitaria[0])
        
    for i in range(len(dbConductorCuStd)):
         datos[i].append(dbConductorCuStd[i][4])

    for i in range(len(dbConductorCuStd)):
         datos[i].append(dbConductorCuStd[i][5])

    for i in range(len(dbConductorCuStd)):
         datos[i].append(dbConductorCuStd[i][6])


    for i in range(len(datos)):
        
        D1=LIn/(datos[i][1]*Vcd)
        datos[i].append(round(D1,3))
        

        datos[i].append(Nc)
        datos[i].append(round(In,2))
            
        datos[i].append(round(datos[i][2],3)*FT60)
        datos[i].append(round(datos[i][3],3)*FT75)
        datos[i].append(round(datos[i][4],3)*FT90)
        
        if Vd > D1:
            if (To==60):
                if ((round(datos[i][4],3)*FT60>=(In*Fsc))):
                    datos[i].append('Yes')
                else:
                    datos[i].append('Not')

            elif (To==75):
                if ((round(datos[i][5],3)*FT75>=(In*Fsc))):
                    datos[i].append('Yes')
                else:
                    datos[i].append('Not')
            elif (To==90):
                if ((round(datos[i][6],3)*FT90>=(In*Fsc))):
                    datos[i].append('Yes')
                else:
                    datos[i].append('Not')
        else:
            datos[i].append('Not')                
        
        for j in range(len(SITM)):
            if (SITM[j]>=Nc*In*Break):
                datos[i].append(SITM[j])
                break
                
    if View == 1:
        #Mostrar información en PSQL
        print(tabulate(datos, headers=["AWG/KCM","Kcd [A,B,C]", "60", "75", "90","%Vd","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
    elif View == 2:
        #Mostrar la información en lista
        return datos
    
def dbcircuit(carga=None,view=None,conductor=None):


    if(carga==None or view==None or conductor==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                      ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                             ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                             ")
        print("-------------------------------------------------------------")
        print("| Los parámetros no son correctos                           |")
        print("| para el módulo dbcircuit(carga,view,conductor)            |")
        print("-------------------------------------------------------------")
        return  
    
    dbcircuit = [[str(i + 1)] for i in range(len(carga))]
        
    datos=[]  
    for i in range(len(carga)):
        if conductor ==1:
            datos.append(mbtcu(carga[i][1],carga[i][2],carga[i][3],carga[i][4],carga[i][5],carga[i][6],carga[i][7],carga[i][8],carga[i][9],carga[i][10],carga[i][11],carga[i][12],carga[i][13],carga[i][14],carga[i][15])) 
        elif conductor ==2:
            datos.append(mbtal(carga[i][1],carga[i][2],carga[i][3],carga[i][4],carga[i][5],carga[i][6],carga[i][7],carga[i][8],carga[i][9],carga[i][10],carga[i][11],carga[i][12],carga[i][13],carga[i][14],carga[i][15])) 
        if view==1:
            print("Id [",i+1,"]========================================================================================================================================================================")
            print(tabulate(datos[i], headers=["AWG/KCM","1F/2H", "2F/3H","3F/3H","3F/4H", "60", "75", "90","%Vd/1F", "%Vd/2F","%Vd/3F","%Vd/3F","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
        #elif view==2:
        #    print("Id [",i+1,"] View = 1 PyEWS.DBCUIRCUIT(carga,1)") 
            
    if conductor==1:
        dbConductor=dbConductorCu
    elif conductor==2:
        dbConductor=dbConductorAl
        
    for i in range(len(carga)):
        for j in range(len(dbConductor)):
        
            if datos[i][j][17]=="Yes":
                dbcircuit[i].append(datos[i][j][0])
                #dbcircuit[i].append(datos[i][j][1])
                dbcircuit[i].append(carga[i][5])
                dbcircuit[i].append(carga[i][9])
                dbcircuit[i].append(carga[i][11])
             

                if carga[i][10]==1:
                    dbcircuit[i].append("1F/2H")
                elif carga[i][10]==2:
                    dbcircuit[i].append("2F/3H")
                elif carga[i][10]==3:
                    dbcircuit[i].append("3F/3H")
                elif carga[i][10]==4:
                    dbcircuit[i].append("3F/4H")
                
                
                dbcircuit[i].append(FCT(carga[i][8]))
                dbcircuit[i].append(carga[i][6]) 
                
                
                #dbcircuit[i].append(datos[i][j][2])
                #dbcircuit[i].append(datos[i][j][3])
                #dbcircuit[i].append(datos[i][j][4])
                dbcircuit[i].append(datos[i][j][5])
                dbcircuit[i].append(datos[i][j][6])
                dbcircuit[i].append(datos[i][j][7])
                
                #Error encontrado desde la version 0.1.13 en la selección 
           
                
                if carga[i][10]==1:
                    dbcircuit[i].append(datos[i][j][8])
                elif carga[i][10]==2:
                    dbcircuit[i].append(datos[i][j][9])
                elif carga[i][10]==3:
                    dbcircuit[i].append(datos[i][j][10])
                elif carga[i][10]==4:
                    dbcircuit[i].append(datos[i][j][11])
                
                
                dbcircuit[i].append(datos[i][j][12])
                dbcircuit[i].append(datos[i][j][13])
                dbcircuit[i].append(datos[i][j][14])
                dbcircuit[i].append(datos[i][j][15])
                dbcircuit[i].append(datos[i][j][16])
                #dbcircuit[i].append(datos[i][j][17])
                dbcircuit[i].append(datos[i][j][18])
                break

            

    #return dbcircuit
    print("::::::: [ RESUMEN DE CARGAS ]:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    #print(tabulate(dbcircuit, headers=["Id","AWG/KCM","l", "2F/3H","3F/3H","3F/4H", "60", "75", "90","%Vd/1F", "%Vd/2F","%Vd/3F","%Vd/3F","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
    print(tabulate(dbcircuit, headers=["Id","#CAL","L[m]", "Vd","FP","ALM", "Fct","Fa","60", "75", "90","Vd[%]","Nc", "In", "60", "75", "90", "ITM"], tablefmt='psql'))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#            
def dbcircuitcd(carga,view,conductor):

    if(carga==None or view==None or conductor==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                      ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                             ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                             ")
        print("-------------------------------------------------------------")
        print("| Los parámetros no son correctos                           |")
        print("| para el módulo DBCIRCUITCD(carga,view,conductor)          |")
        print("-------------------------------------------------------------")
        return      
    
    dbcircuit = [[str(i + 1)] for i in range(len(carga))]
    
    datos=[]  
    for i in range(len(carga)):
        if conductor == 1:
            datos.append(mbtcustd(carga[i][1],carga[i][2],carga[i][3],carga[i][4],carga[i][5],carga[i][6],carga[i][7],carga[i][8],carga[i][9],carga[i][10])) 
            if view==1:
                print("Id [",i+1,"]============================================================================================================")
                print(tabulate(datos[i], headers=["AWG/KCMxx","Kcd [A,B,C]", "", "60", "75", "90","%Vd","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))
        elif conductor == 2:
            datos.append(mbtcustd(carga[i][1],carga[i][2],carga[i][3],carga[i][4],carga[i][5],carga[i][6],carga[i][7],carga[i][8],carga[i][9],carga[i][10]))
            if view==1:
                print("Id [",i+1,"]============================================================================================================")
                print(tabulate(datos[i], headers=["AWG/KCM","Kcd [A,B,C]", "", "60", "75", "90","%Vd","Nc", "In", "60", "75", "90", "Op", "ITM"], tablefmt='psql'))


            
    if conductor==1:
        dbConductor=dbConductorCuStd
    elif conductor==2:
        dbConductor=dbConductorCuStd
        
    for i in range(len(carga)):
        for j in range(len(dbConductor)):
            
            if datos[i][j][11]=="Yes":
                
                dbcircuit[i].append(datos[i][j][0])
                dbcircuit[i].append(datos[i][j][1])
                dbcircuit[i].append(carga[i][2])
                dbcircuit[i].append(carga[i][7]) 
                dbcircuit[i].append("CD [+-]")
                dbcircuit[i].append(FCT(carga[i][6]))
                dbcircuit[i].append(datos[i][j][2])
                dbcircuit[i].append(datos[i][j][3])
                dbcircuit[i].append(datos[i][j][4])
                dbcircuit[i].append(datos[i][j][5])
                dbcircuit[i].append(datos[i][j][6])
                dbcircuit[i].append(datos[i][j][7])
                dbcircuit[i].append(datos[i][j][8])
                dbcircuit[i].append(datos[i][j][9])
                dbcircuit[i].append(datos[i][j][10])
                #dbcircuit[i].append(datos[i][j][11])
                dbcircuit[i].append(datos[i][j][12])
                break

            

    #return dbcircuit
    print("::::::: [ RESUMEN DE CARGAS ]::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    #print(tabulate(dbcircuit, headers=["Id","#CAL","L[m]", "Vd","FP","ALM", "Fct","Fa","60", "75", "90","Vd[%]","Nc", "In", "60", "75", "90", "ITM"], tablefmt='psql'))
    
    #print(tabulate(dbcircuit, headers=["Idx","#CAL","L[m]", "Vd","ALM", "Fct","60", "75", "90","Vd[%]","Nc", "In", "60", "75", "90", "ITM"], tablefmt='psql'))
    
    print(tabulate(dbcircuit, headers=["Id","#CAL","Kcd [A,B,C]","L[m]", "Vd", "ALM", "Fct", "60", "75", "90", "Vd[%]", "Nc", "In", "60", "75", "90", "ITM"],  tablefmt='psql'))

def autolabel(rects):
    """Funcion para agregar una etiqueta con el valor en cada barra"""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def graph(mydata=None,condA=None,condB=None,w=None,h=None,material=None,color=None,sistema=None):


    if((mydata==None or not mydata) or condA==None or condB==None or w==None or h==None or material==None or color==None or sistema==None):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                      ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                             ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                             ")
        print("-------------------------------------------------------------")
        print("| Los parámetros no son correctos                           |")
        print("| para el módulo                                            |")
        print("| graph(mydata,Cal,Cal,Ancho,Alto,Material,Color,Sistema)   |") 
        print("----------------------------------------------- -------------")
        return         


    xdata=[]
    ydata=[]
    y1data=[]
    y2data=[]

    for i in range(len(mydata)):
        xdata.append(mydata[i][0])
            
        if(sistema==1):
            slabel="%Vd 1F/2H"
            ydata.append(mydata[i][8])
        elif(sistema==2):
            slabel="%Vd 2F/3H"
            ydata.append(mydata[i][9])
        elif(sistema==3):
            slabel="%Vd 3F/3H"
            ydata.append(mydata[i][10])
        elif(sistema==4):
            slabel="%Vd 3F/4H"
            ydata.append(mydata[i][10])
  
    if material==1:
        xConductor =["14 AWG", "12 AWG", "10 AWG", "8 AWG", "6 AWG", "4 AWG", "2 AWG", "1/0 AWG", "2/0 AWG", "3/0 AWG", "4/0 AWG", "250 KCM", "300 KCM", "350 KCM", "400 KCM", "500 KCM", "600 KCM", "750 KCM", "1000 KCM"]
    elif material==2:
        xConductor =["6 AWG", "4 AWG", "2 AWG", "1/0 AWG", "2/0 AWG", "3/0 AWG", "4/0 AWG", "250 KCM", "300 KCM", "350 KCM", "400 KCM", "500 KCM", "600 KCM", "750 KCM", "1000 KCM"]


    for i in range(len(xConductor)):
        if condA==xConductor[i]:
            a=i
            break

    for i in range(len(xConductor)):
        if condB==xConductor[i]:
            b=i+1
            break


    x=xdata
    #print(x)
    numero_de_grupos = len(ydata[a:b])
    indice_barras = np.arange(numero_de_grupos)
    ancho_barras =0.5
    plt.figure(figsize=(w,h))
    rects1 = plt.bar(indice_barras + ancho_barras/10,ydata[a:b], width=ancho_barras,label=slabel, color=color)
    plt.legend(loc='best')
    autolabel(rects1)
    plt.xticks(indice_barras, (x[a:b]))
  
    plt.ylabel('Caída de tensión porcentual [%Vd]')
    plt.xlabel('Calibre de conductores elécticos')
    plt.title('Caída de tensión en conductores eléctricos')
    plt.grid()
    plt.show()



def icc(conductor=None,T1=None,T2=None,fhz=None,view=None):

    if((conductor==None or T1==None or T2==None or fhz==None or view==None)):
        t = time.localtime()
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                    ElectricalWireSizes                      ")
        print("                 ",time.asctime(t))
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("                                                             ")
        print("                         ─▄▀─▄▀")
        print("                         ──▀──▀")
        print("                         █▀▀▀▀▀█▄")
        print("                         █░░░░░█─█")
        print("                         ▀▄▄▄▄▄▀▀")
        print("                                                             ")
        print("-------------------------------------------------------------")
        print("| Los parámetros no son correctos                           |")
        print("| para el módulo                                            |")
        print("| icc(conductor,T1,T2,fhz,view)                             |") 
        print("----------------------------------------------- -------------")
        return  
    
    if conductor==1:
        datos=[["14 AWG"],
            ["12 AWG"],
            ["10 AWG"],
            ["8 AWG"],
            ["6 AWG"],
            ["4 AWG"],
            ["2 AWG"],
            ["1/0 AWG"],
            ["2/0 AWG"],
            ["3/0 AWG"],
            ["4/0 AWG"],
            ["250 KCM"],
            ["300 KCM"],
            ["350 KCM"],
            ["400 KCM"],
            ["500 KCM"],
            ["600 KCM"],
            ["750 KCM"],
            ["1000 KCM"]]

        k=0.0297

        for i in range(len(dbConductorCu)):
            Seccion=dbConductorCu[i][10]
            datos[i].append(Seccion)

        t=1/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=2/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=4/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))
        t=8/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=16/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=30/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=60/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=100/fhz
        for i in range(len(dbConductorCu)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        if view==1:
            headers = ["Calibre","S[mm²]","1C[kA]","2C[kA]","4C[kA]", "8C[kA]", "16C[kA]", "30C[kA]", "60C[kA]", "100C[kA]"]
            print(tabulate(datos, headers, tablefmt="pretty"))
        elif view==2:
            return datos
    
    elif conductor==2:
        
        datos=[["6 AWG"],
            ["4 AWG"],
            ["2 AWG"],
            ["1/0 AWG"],
            ["2/0 AWG"],
            ["3/0 AWG"],
            ["4/0 AWG"],
            ["250 KCM"],
            ["300 KCM"],
            ["350 KCM"],
            ["400 KCM"],
            ["500 KCM"],
            ["600 KCM"],
            ["750 KCM"],
            ["1000 KCM"]]

        k=0.0125

        for i in range(len(dbConductorAl)):
            Seccion=dbConductorAl[i][10]
            datos[i].append(Seccion)

        t=1/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=2/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=4/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))
        t=8/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=16/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=30/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorCu[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=60/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        t=100/fhz
        for i in range(len(dbConductorAl)):
            CM=round(dbConductorAl[i][10]*1973.525241,2)
            datos[i].append(round(math.sqrt(((pow(CM,2)*(k*math.log10((T2+234)/(T1+234)))))/t)/1000,2))

        if view==1:
            headers = ["Calibre","S[mm²]","1C[kA]","2C[kA]","4C[kA]", "8C[kA]", "16C[kA]", "30C[kA]", "60C[kA]", "100C[kA]"]
            print(tabulate(datos, headers, tablefmt="pretty"))
        elif view==2:
            return datos
