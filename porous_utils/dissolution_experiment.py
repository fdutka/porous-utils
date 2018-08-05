
# experimental constants

D = 1e-3 # [mm^2/s]
k = 4.67e-3 # [mm/s]
phi = 0.55
csat = 15 # [mol/m^3]
csol = 2.308/172.173*1e6 # [mol/m^3]

def PeDa(Q,W,h0):
    """
    returns Peclet and Damkohler numbers
    Q in ml/h, W in mm, h0 in mm
    """
    Q = Q*1e3/3600 # transforms into mm^3/s

    Pe = Q/(W*D)
    Da = k*h0*W/Q
    return Pe, Da

def U0(Q,W,h0, hmax):
    """
    returns velocity of flat front in experiment [mm/h]
    Q in ml/h, W in mm, h0 in mm
    """


    Q = Q*1e3 # transforms into mm^3/h
    
    U = Q*csat/(W*(hmax-h0)*(1-phi)*csol)
    return U 