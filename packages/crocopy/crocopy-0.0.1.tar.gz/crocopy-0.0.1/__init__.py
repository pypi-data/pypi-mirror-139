import numpy as np
from numpy import nan
from numpy import zeros
import sys
from scipy import interpolate
from scipy.spatial import Delaunay
import netCDF4 as nc
import time as tm
from math import radians, cos, sin, asin, sqrt

# --------------- from u-point to rho-point ---------------
def u2rho_2d(var_u):
        [Mp,L]                  = var_u.shape
        Lp                      = L+1
        Lm                      = L-1
        var_rho                 = zeros((Mp,Lp))
        var_rho[:,1:L]          = 0.5*(var_u[:,0:Lm] + var_u[:,1:L])
        var_rho[:,0]            = var_rho[:,1]
        var_rho[:,Lp-1]         = var_rho[:,L-1]
        return var_rho

def u2rho_3d(var_u):
        [N,Mp,L]                = var_u.shape
        Lp                      = L+1
        Lm                      = L-1
        var_rho                 = zeros((N,Mp,Lp))
        var_rho[:,:,1:L]        = 0.5*(var_u[:,:,0:Lm] + var_u[:,:,1:L])
        var_rho[:,:,0]          = var_rho[:,:,1]
        var_rho[:,:,Lp-1]       = var_rho[:,:,L-1]
        return var_rho

def u2rho_4d(var_u):
        [nt,N,Mp,L]             = var_u.shape
        Lp                      = L+1
        Lm                      = L-1
        var_rho                 = zeros((nt,N,Mp,Lp))
        var_rho[:,:,:,1:L]      = 0.5*(var_u[:,:,:,0:Lm] + var_u[:,:,:,1:L])
        var_rho[:,:,:,0]        = var_rho[:,:,:,1]
        var_rho[:,:,:,Lp-1]     = var_rho[:,:,:,L-1]
        return var_rho

def u2v_2d(var_u):
        [Mp,L]                  = var_u.shape
        M                              = Mp-1
        Mm                      = M-1
        Lp                      = L+1
        Lm                      = L-1
        var_v                          = zeros((M,Lp))
        var_v[0:M,1:L]          = 0.25*(var_u[:-1,:-1]+var_u[:-1,1:]+\
                                        var_u[1: ,:-1]+var_u[1: ,1:])
        var_v[:,0]              = var_v[:,1]
        var_v[:,L]              = var_v[:,Lm]
        return var_v

# --------------- from v-point to rho-point ---------------
def v2rho_2d(var_v):
        [M,Lp]                  = var_v.shape
        Mp                      = M+1
        Mm                      = M-1
        var_rho                 = zeros((Mp,Lp))
        var_rho[1:M,:]          = 0.5*(var_v[0:Mm,:] + var_v[1:M,:])
        var_rho[0,:]            = var_rho[1,:]
        var_rho[Mp-1,:]         = var_rho[M-1,:]
        return var_rho

def v2rho_3d(var_v):
        [N,M,Lp]                = var_v.shape
        Mp                      = M+1
        Mm                      = M-1
        var_rho                 = zeros((N,Mp,Lp))
        var_rho[:,1:M,:]        = 0.5*(var_v[:,0:Mm,:] + var_v[:,1:M,:])
        var_rho[:,0,:]          = var_rho[:,1,:]
        var_rho[:,Mp-1,:]       = var_rho[:,M-1,:]
        return var_rho

def v2rho_4d(var_v):
        [nt,N,M,Lp]             = var_v.shape
        Mp                      = M+1
        Mm                      = M-1
        var_rho                 = zeros((nt,N,Mp,Lp))
        var_rho[:,:,1:M,:]      = 0.5*(var_v[:,:,0:Mm,:] + var_v[:,:,1:M,:])
        var_rho[:,:,0,:]        = var_rho[:,:,1,:]
        var_rho[:,:,Mp-1,:]     = var_rho[:,:,M-1,:]
        return var_rho

def v2u_2d(var_v):
        [M,Lp]                  = var_v.shape
        Mp                      = M+1
        Mm                      = M-1
        L                       = Lp-1
        Lm                      = L-1
        var_u                          = zeros((Mp,L))
        var_u[1:M,0:L]          = 0.25*(var_v[:-1,:-1]+var_v[:-1,1:]+\
                                        var_v[1: ,:-1]+var_v[1: ,1:])
        var_u[0,:]              = var_u[1,:]
        var_u[M,:]              = var_u[Mm,:]
        return var_u

# --------------- from rho-point to u,v,psi-point ---------------

def rho2uvp(rfield):                                 # often used for a mask
        [Mp,Lp]         = rfield.shape
        M               = Mp-1
        L               = Lp-1
        vfield          = 0.5*(rfield[0:M,:] + rfield[1:Mp,:])
        ufield          = 0.5*(rfield[:,0:L] + rfield[:,1:Lp])
        pfield          = 0.5*(ufield[0:M,:] + ufield[1:Mp,:])
        return ufield,vfield,pfield

def rho2u_2d(var_rho):
        [Mp,Lp]         = var_rho.shape
        L               = Lp-1
        var_u           = 0.5*(var_rho[:,0:L]+var_rho[:,1:Lp])
        return var_u

def rho2u_3d(var_rho):
        [N,Mp,Lp]       = var_rho.shape
        L               = Lp-1
        var_u           = 0.5*(var_rho[:,:,0:L]+var_rho[:,:,1:Lp])
        return var_u

def rho2u_4d(var_rho):
        [nt,N,Mp,Lp]    = var_rho.shape
        L               = Lp-1
        var_u           = 0.5*(var_rho[:,:,:,0:L]+var_rho[:,:,:,1:Lp])
        return var_u

def rho2v_2d(var_rho):
        [Mp,Lp]         = var_rho.shape
        M               = Mp-1
        var_v           = 0.5*(var_rho[0:M,:]+var_rho[1:Mp,:])
        return var_v

def rho2v_3d(var_rho):
        [N,Mp,Lp]       = var_rho.shape
        M               = Mp-1
        var_v           = 0.5*(var_rho[:,0:M,:]+var_rho[:,1:Mp,:])
        return var_v

def rho2v_4d(var_rho):
        [nt,N,Mp,Lp]    = var_rho.shape
        M               = Mp-1
        var_v           = 0.5*(var_rho[:,:,0:M,:]+var_rho[:,:,1:Mp,:])
        return var_v


def rho2p_2d(var_rho):
        [Mp,Lp]         = var_rho.shape
        M               = Mp-1
        L               = Lp-1
        var_p           = 0.25*(var_rho[0:M,0:L]+var_rho[0:M,1:Lp]+
                                var_rho[1:Mp,0:L]+var_rho[1:Mp,1:Lp])
        return var_p

def rho2p_3d(var_rho):
        [N,Mp,Lp]         = var_rho.shape
        M               = Mp-1
        L               = Lp-1
        var_p           = 0.25*(var_rho[:,0:M,0:L]+var_rho[:,0:M,1:Lp]+
                                var_rho[:,1:Mp,0:L]+var_rho[:,1:Mp,1:Lp])
        return var_p

# --------------- from psi-point to rho-point ---------------
def psi2rho_2d(var_psi):                                # this is for a 2D variable only
        [M,L]           = var_psi.shape
        Mp              = M+1
        Lp              = L+1
        Mm              = M-1
        Lm              = L-1
        var_rho         = zeros((Mp,Lp))
        var_rho[1:M,1:L]=0.25*(var_psi[0:Mm,0:Lm]+var_psi[0:Mm,1:L]+var_psi[1:M,0:Lm]+var_psi[1:M,1:L])
        var_rho[0,:]    = var_rho[1,:]
        var_rho[Mp-1,:] = var_rho[M-1,:]
        var_rho[:,0]    = var_rho[:,1]
        var_rho[:,Lp-1] = var_rho[:,L-1]
        return var_rho

def psi2rho_3d(var_psi):                                # this is for a 3D variable only
        [N,M,L]         = var_psi.shape
        Mp              = M+1
        Lp              = L+1
        Mm              = M-1
        Lm              = L-1
        var_rho         = zeros((N,Mp,Lp))
        var_rho[:,1:M,1:L] = 0.25*(var_psi[:,0:Mm,0:Lm] + var_psi[:,0:Mm,1:L]\
                                  +var_psi[:,1:M,0:Lm]  + var_psi[:,1:M,1:L])
        var_rho[:,0,:]    = var_rho[:,1,:]
        var_rho[:,Mp-1,:] = var_rho[:,M-1,:]
        var_rho[:,:,0]    = var_rho[:,:,1]
        var_rho[:,:,Lp-1] = var_rho[:,:,L-1]
        return var_rho

# --------------- get u- v- and psi- masks from maks at rho point ---------------

def uvp_mask(rfield):
        [Mp,Lp]         = rfield.shape
        M               = Mp-1
        L               = Lp-1
        vfield          = rfield[0:M,:] * rfield[1:Mp,:]
        ufield          = rfield[:,0:L] * rfield[:,1:Lp]
        pfield          = ufield[0:M,:] * ufield[1:Mp,:]
        return ufield,vfield,pfield


# --------------- 9 points avg ---------------

def nine_pts_avg(var,mask):
        var = var * mask

        num=var[2:  :3, :-2:3]+var[2:  :3,1:-1:3]+var[2:  :3,2::3]+\
            var[1:-1:3, :-2:3]+var[1:-1:3,1:-1:3]+var[1:-1:3,2::3]+\
            var[ :-2:3, :-2:3]+var[ :-2:3,1:-1:3]+var[ :-2:3,2::3]

        den=mask[2:  :3, :-2:3]+mask[2:  :3,1:-1:3]+mask[2:  :3,2::3]+\
            mask[1:-1:3, :-2:3]+mask[1:-1:3,1:-1:3]+mask[1:-1:3,2::3]+\
            mask[ :-2:3, :-2:3]+mask[ :-2:3,1:-1:3]+mask[ :-2:3,2::3]

        den[den==0]=nan
        var=num/den
        
        return var


# --------------- vorticity ---------------

def vort(ubar,vbar,pm,pn):

        [Mp,Lp] = pm.shape
        L=Lp-1
        M=Mp-1
        Lm=L-1
        Mm=M-1
        xi=zeros((M,L))
        mn_p=zeros((M,L))
        uom=zeros((M,Lp))
        von=zeros((Mp,L))
        uom=2*ubar/(pm[:,0:L]+pm[:,1:Lp])
        von=2*vbar/(pn[0:M,:]+pn[1:Mp,:])
        mn=pm*pn
        mn_p=(mn[0:M ,0:L ]+mn[0:M ,1:Lp]+\
              mn[1:Mp,1:Lp]+mn[1:Mp,0:L ])/4
        xi=mn_p*(von[:,1:Lp]-von[:,0:L]-uom[1:Mp,:]+uom[0:M,:])

        return xi


# --------------- vorticity ---------------

def vort3d(u,v,pm,pn):

        [N,Mp,L] = u.shape
        Lp=L+1
        M=Mp-1
        
        om=2/(pm[:,0:L]+pm[:,1:Lp])
        on=2/(pn[0:M,:]+pn[1:Mp,:])
        uom=u*np.tile(om,(N,1,1))
        von=v*np.tile(on,(N,1,1))
        mn=pm*pn
        mn_p=(mn[0:M ,0:L ]+mn[0:M ,1:Lp]+\
              mn[1:Mp,1:Lp]+mn[1:Mp,0:L ])/4
        xi=np.tile(mn_p,(N,1,1))*(von[:,:,1:Lp]-von[:,:,0:L]-uom[:,1:Mp,:]+uom[:,0:M,:])

        return xi

#
# --------------- corrected and stable arange function ---------------
#
# Function arange like matlab
#
def matarange(start,step,stop):
  out=np.arange(start,stop+step,step+1.123456789123456789e-20)
  return out


#
# --------------- ^2 more efficient ---------------
#
# Function square
#
def square(varin):
  varout=varin*varin
  return varout

#
# --------------- put nan on masked values ---------------
#
# Function nanmask
#
def nanmask(varin,maskin):
  
  varin[np.where(maskin==0.)]=np.nan
  varout=varin+0.
  return varout



# CROCO Geometries
#=====================================

def dist_spheric2(lat1,lon1,lat2,lon2,R): # function that takes angles in deg
    #R= 6371.008*10**3
    l=np.abs(lon2-lon1)
    if ((np.size(lat1)>1) | (np.size(lat2)>1)):
        l[l>=180]=360-l[l>=180]
    else:
        if l>180:
            l=360-l
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)
    l=np.radians(l)
    dist=R*np.arctan2(np.sqrt((np.sin(l)*np.cos(lat2))**2 +(np.sin(lat2)*np.cos(lat1)
                     -np.cos(lat2)*np.sin(lat1)*np.cos(l))**2 ),
                          np.sin(lat2)*np.sin(lat1)+ np.cos(lat2)*np.cos(lat1)*np.cos(l)
                          )
    return dist

def gnomonic(lon,lat,lon0,lat0,R):
    #Gnomonic projection is distance preserving for
    #interpolation purposes.
    lat = lat*np.pi/180
    lon = lon*np.pi/180
    lat0= lat0*np.pi/180
    lon0= lon0*np.pi/180
    cosc = np.sin(lat0)*np.sin(lat) + np.cos(lat0)*np.cos(lat)*np.cos(lon-lon0)
    xg = R*np.cos(lat)*np.sin(lon-lon0)/cosc
    yg = R*(np.cos(lat0)*np.sin(lat) - np.sin(lat0)*np.cos(lat)*np.cos(lon-lon0) )/cosc
    return xg,yg


def ignomonic(x,y,lon0,lat0,R):
    #Gnomonic projection is distance preserving for
    #interpolation purposes.
    lat0= lat0*np.pi/180
    lon0= lon0*np.pi/180
    rho=np.sqrt(x**2+y**2)
    c=np.arctan2(rho,R)
    if (rho!=0):
        lat=np.arcsin(np.cos(c)*np.sin(lat0) + (y*np.sin(c)*np.cos(lat0))/rho)
        if ((lat!=np.pi/2) & (lat!=-np.pi/2) ):
            lon=lon0+np.arctan2(x*np.sin(c),(rho*np.cos(lat0)*np.cos(c)-y*np.sin(lat0)*np.sin(c)))
        elif (lat==np.pi/2):
            lon=lon0+np.arctan2(x,-y)
        elif (lat==-np.pi/2):
            lon=lon0+np.arctan2(x,y)
    elif (rho==0):
        lat=lat0
        lon=lon0
    lat = lat*180/np.pi
    lon = lon*180/np.pi
    return lon,lat

def rotated_grid2(lon0_south,lat0_south,lon0_north,lat0_north,dgcx,dgcy,distx,zonal_orientation,R=6367442.76):
    
    ##1. define the most meridional transect (xg_y,yg_y)
    disty=dist_spheric2(lat0_south,lon0_south,lat0_north,lon0_north, R)
    npsecy=np.int(disty//dgcy)+1
    #project on tangent plane at lon0_south,lat0_south
    xg1,yg1 = gnomonic(lon0_north,lat0_north,lon0_south,lat0_south,R)
    ag_y=yg1/xg1
    xg_y=np.zeros((1,npsecy))
    xg_y[0,0]=0
    xg_y[0,1:]=R*np.tan(np.arange(1,npsecy)*dgcy/R)/(1+np.abs(ag_y)**2)**0.5
    yg_y=ag_y*xg_y
    #go back to the lon,lat coordinates
    long_y=np.zeros((1,npsecy))
    latg_y=np.zeros((1,npsecy))
    for ig in range(0,np.size(xg_y)):
        long_y[0,ig],latg_y[0,ig] = ignomonic(xg_y[0,ig],yg_y[0,ig],lon0_south,lat0_south,R)

    ##2. define the most zonal transects (xg_x,yg_x)
    npsecx=np.int(distx//dgcx)
    if zonal_orientation=='east':
        ag_x=-1/ag_y
    elif zonal_orientation=='west':
        ag_x=+1/ag_y
        
    #print(ag_y)
    xg_x=np.zeros((1,npsecx))
    xg_x[0,0]=0
    xg_x[0,1:]=R*np.tan(np.arange(1,npsecx)*dgcx/R)/(1+np.abs(ag_x)**2)**0.5
    yg_x=ag_x*xg_x
    long_x=np.zeros((1,npsecx))
    latg_x=np.zeros((1,npsecx))
    for ig in range(0,np.size(xg_x)):
        long_x[0,ig],latg_x[0,ig] = ignomonic(xg_x[0,ig],yg_x[0,ig],lon0_south,lat0_south,R)

    #define all arrays
    dlon=np.diff(long_y,1,1)
    dlat=np.diff(latg_y,1,1)

    londom=np.zeros((npsecy,npsecx))
    latdom=np.zeros((npsecy,npsecx))
    londom[0,:]=long_x
    latdom[0,:]=latg_x
    for ig in range(0,npsecx):
        #print(ig)
        londom[1:,ig]=long_x[0,ig]+np.cumsum(dlon)
        latdom[1:,ig]=latg_x[0,ig]+np.cumsum(dlat)
    
    #define X,Y grid in meters with origin at lon0,lat0
    xrot=np.zeros_like(londom)
    yrot=np.zeros_like(londom)
    for i in range(npsecy):
        xrot[i,1:]=np.cumsum(dist_spheric2(latdom[i,:-1],londom[i,:-1],
                                           latdom[i,1:],londom[i,1:],R=6367442.76))

    for j in range(npsecx):
        yrot[1:,j]=np.cumsum(dist_spheric2(latdom[:-1,j],londom[:-1,j],
                                            latdom[1:,j],londom[1:,j],R=6367442.76))
        
    return londom,latdom,xrot,yrot

def transect_grid(lon0,lat0,lon1,lat1,dgc,R=6367442.76):
    
    ##1. define the most meridional transect (xg_y,yg_y)
    distsec=dist_spheric2(lat0,lon0,lat1,lon1,R)
    npsec=np.int(distsec//dgc)+1
    #project on tangent plane at lon0_south,lat0_south
    xg,yg = gnomonic(lon1,lat1,lon0,lat0,R)
    ag=yg/xg
    #print(ag)
    xg=np.zeros((1,npsec))
    xg[0,0]=0
    xg[0,1:]=R*np.tan(np.arange(1,npsec)*dgc/R)/(1+np.abs(ag)**2)**0.5
    yg=ag*xg
    #go back to the lon,lat coordinates
    long=np.zeros((1,npsec))
    latg=np.zeros((1,npsec))
    for ig in range(0,np.size(xg)):
        long[0,ig],latg[0,ig] = ignomonic(xg[0,ig],yg[0,ig],lon0,lat0,R)
    
    #define X grid in meters with origin at lon0,lat0
    xrot=np.zeros_like(long)
    xrot[0,1:]=np.cumsum(dist_spheric2(latg[0,:-1],long[0,:-1],
                                           latg[0,1:],long[0,1:],R=6367442.76))
    return long,latg,xrot


def zlevs(h,zeta,theta_s,theta_b,hc,N,type,vtransform):
    [M,L]=h.shape
    sc_r=np.zeros(N)
    Cs_r=np.zeros(N)
    sc_w=np.zeros(N+1)
    Cs_w=np.zeros(N+1)
    if (vtransform == 2):
        ds=1./N
        if type=='w':
            sc_w[0]   = -1.0
            sc_w[N]   =  0
            Cs_w[0]   = -1.0
            Cs_w[N]   =  0
            sc_w[1:N] = sc_w[1:N]+ds*(np.arange(1,N)-N)
            Cs_w      = csf(sc_w, theta_s,theta_b)
            N=N+1;
        else:
            sc= ds*(np.arange(1,N+1)-N-0.5)
            Cs_r=csf(sc, theta_s,theta_b)
            sc_r=sc
    else:
        cff1=1./np.sinh(theta_s)
        cff2=0.5/np.tanh(0.5*theta_s)
        if type=='w':
            sc=(np.arange(0,N+1)-N)/float(N)
            N = N+1
        else:
            sc = (np.arange(1,N+1)-N-0.5)/float(N)

        Cs = (1-theta_b)*cff1*np.sinh(theta_s*sc)+theta_b*(cff2*np.tanh(theta_s*(sc+0.5))-0.5)
        
    h[h==0] = 1.e-14
    hinv    = 1./h
    z       = np.zeros((N,M,L))
    if (vtransform == 2):
        if type=='w':
            cff1 = Cs_w
            cff2 = sc_w+1
            sc   = sc_w
        else:
            cff1 = Cs_r
            cff2 = sc_r+1
            sc   = sc_r

        h2   = (h+hc)
        cff  = hc*sc
        h2inv = 1./h2
        for k in range(0,N):
            z0       = cff[k]+cff1[k]*h;
            z[k,:,:] = z0*h/(h2) + zeta*(1.+z0*h2inv)
    else:
        print("OH YEAH")
        cff1 = Cs
        cff2 = sc+1
        cff  = hc*(sc-Cs)
        cff2 = sc+1
        for k in range(0,N):
            z0       = cff[k]+cff1[k]*h
            z[k,:,:] = z0+zeta*(1.+z0*hinv)

    return z

def csf(sc,theta_s,theta_b):
    if (theta_s > 0):
            csfr = (1-np.cosh(sc*theta_s))/(np.cosh(theta_s)-1)
    else:
            csfr = -sc**2
    if (theta_b >0):
            h = (np.exp(theta_b*csfr)-1)/(1-np.exp(-theta_b))
    else:
            h = csfr
    return h

def get_tri_coef(X, Y, newX, newY, verbose=0):

    """
    Inputs:
        origin lon and lat 2d arrays (X,Y)
        child lon and lat 2d arrays (newX,newY)
    Ouputs:
        elem - pointers to 2d gridded data (at lonp,latp locations) from
            which the interpolation is computed (3 for each child point)
        coef - linear interpolation coefficients
    Use:
        To subsequently interpolate data from Fp to Fc, the following
        will work:      Fc  = sum(coef.*Fp(elem),3);  This line  should come in place of all
        griddata calls. Since it avoids repeated triangulations and tsearches (that are done
        with every call to griddata) it should be much faster.
    """

    Xp = np.array([X.ravel(), Y.ravel()]).T
    Xc = np.array([newX.ravel(), newY.ravel()]).T


    #Compute Delaunay triangulation
    if verbose==1: tstart = tm.time()
    tri = Delaunay(Xp)
    if verbose==1: print('Delaunay Triangulation', tm.time()-tstart)

    #Compute enclosing simplex and barycentric coordinate (similar to tsearchn in MATLAB)
    npts = Xc.shape[0]
    p = np.zeros((npts,3))

    points = tri.points[tri.vertices[tri.find_simplex(Xc)]]
    if verbose==1: tstart = tm.time()
    for i in range(npts):

        if verbose==1: print(np.float(i)/npts)

        if tri.find_simplex(Xc[i])==-1:  #Point outside triangulation
             p[i,:] = p[i,:] * np.nan

        else:

            if verbose==1: tstart = tm.time()
            A = np.append(np.ones((3,1)),points[i] ,axis=1)
            if verbose==1: print('append A', tm.time()-tstart)

            if verbose==1: tstart = tm.time()
            B = np.append(1., Xc[i])
            if verbose==1: print('append B', tm.time()-tstart)

            if verbose==1: tstart = tm.time()
            p[i,:] = np.linalg.lstsq(A.T,B.T)[0]
            if verbose==1: print('solve', tm.time()-tstart)


    if verbose==1: print('Coef. computation 1', tm.time()-tstart)

    if verbose==1: tstart = tm.time()
    elem = np.reshape(tri.vertices[tri.find_simplex(Xc)],(newX.shape[0],newY.shape[1],3))
    coef = np.reshape(p,(newX.shape[0],newY.shape[1],3))
    if verbose==1: print('Coef. computation 2', tm.time()-tstart)

    return(elem,coef)

def horiz_interp_delaunay(lonold,latold,varold,lonnew,latnew,elem=0,coef=0):
    #lonold: 2D original longitude matrix
    #latold: 2D original longitude matrix
    #varold: 2D original datra matrix
    #lonnew: 2D new longitude matrix
    #latnew: 2D new longitude matrix
    #print(len(args*))
    
    ## Horizontal Interpolation from croco varoables'grid to new grid
    ##: get interpolation coefficients
    if np.all(elem==0):
        [elem,coef] = get_tri_coef(lonold, latold,lonnew, latnew)
        coefnorm=np.sum(coef,axis=2)
        coef=coef/coefnorm[:,:,np.newaxis]
        varnew = np.sum(coef*varold.ravel()[elem],2)
        return elem,coef,varnew
    else:
        varnew = np.sum(coef*varold.ravel()[elem],2)
        return varnew




def read_croco_grid(gridname):
    ''' 
    This function reads in variables from the croco grid and closes the nc file afterwards.
    Inputs:
    gridname : path to grid and file name in string format
    
    Outputs:
    lonr : longitude in rho points
    latr : latitude in rho points
    h : depths 
    hc : horizontal stretching parameter
    theta_s : surface stretching parameter
    theta_b : bottom stretiching parameter
    N : depth levels            
    '''
    ncroms=nc.Dataset(gridname,'r')
    lonr=ncroms['lon_rho'][:]
    latr=ncroms['lat_rho'][:]
    h=ncroms['h'][:]
    hc = ncroms['hc'][:]
    theta_s = ncroms.theta_s
    theta_b = ncroms.theta_b
    N=ncroms.dimensions['s_rho'].size
    ncroms.close()
    
    #Reconstruct missing values if necessary
    if np.any(lonr.mask==False):
        for i in range(np.shape(lonr)[1]):
            lonr[:,i]=np.min(lonr[:,i])
        for j in range(np.shape(latr)[0]):
            latr[j,:]=np.min(latr[j,:])
    
    return lonr,latr,h,hc,theta_s,theta_b,N


#import crocopy.croco_functions as cfunctions

# this function is used in the zlevs function. It returns the depths
def csf(sc,theta_s,theta_b):
    """
    Get CS-Curves for the new s-ccordinate system
    """
    if (theta_s > 0):
        csfr = (1-np.cosh(sc*theta_s))/(np.cosh(theta_s)-1)
    
    else:
        csfr = -sc**2
    
    if (theta_b >0):
        h = (np.exp(theta_b*csfr)-1)/(1-np.exp(-theta_b))
    
    else:
        h = csfr
    
    return h


# get index of particular coordinate
def geo_idx(dd, dd_array):
    """
     - dd - the decimal degree (latitude or longitude)
     - dd_array - the list of decimal degrees to search.
     search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
   """
    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx

def get_tri_coef(X, Y, newX, newY, verbose=0):

    """
    Inputs:
        origin lon and lat 2d arrays (X,Y)
        child lon and lat 2d arrays (newX,newY)
    Ouputs:
        elem - pointers to 2d gridded data (at lonp,latp locations) from
            which the interpolation is computed (3 for each child point)
        coef - linear interpolation coefficients
    Use:
        To subsequently interpolate data from Fp to Fc, the following
        will work:      Fc  = sum(coef.*Fp(elem),3);  This line  should come in place of all
        griddata calls. Since it avoids repeated triangulations and tsearches (that are done
        with every call to griddata) it should be much faster.
    """

    Xp = np.array([X.ravel(), Y.ravel()]).T
    Xc = np.array([newX.ravel(), newY.ravel()]).T


    #Compute Delaunay triangulation
    if verbose==1: tstart = tm.time()
    tri = Delaunay(Xp)
    if verbose==1: print('Delaunay Triangulation', tm.time()-tstart)

    #Compute enclosing simplex and barycentric coordinate (similar to tsearchn in MATLAB)
    npts = Xc.shape[0]
    p = np.zeros((npts,3))

    points = tri.points[tri.vertices[tri.find_simplex(Xc)]]
    if verbose==1: tstart = tm.time()
    for i in range(npts):

        if verbose==1: print(np.float(i)/npts)

        if tri.find_simplex(Xc[i])==-1:  #Point outside triangulation
             p[i,:] = p[i,:] * np.nan

        else:

            if verbose==1: tstart = tm.time()
            A = np.append(np.ones((3,1)),points[i] ,axis=1)
            if verbose==1: print('append A', tm.time()-tstart)

            if verbose==1: tstart = tm.time()
            B = np.append(1., Xc[i])
            if verbose==1: print('append B', tm.time()-tstart)

            if verbose==1: tstart = tm.time()
            p[i,:] = np.linalg.lstsq(A.T,B.T)[0]
            if verbose==1: print('solve', tm.time()-tstart)


    if verbose==1: print('Coef. computation 1', tm.time()-tstart)

    if verbose==1: tstart = tm.time()
    elem = np.reshape(tri.vertices[tri.find_simplex(Xc)],(newX.shape[0],newY.shape[1],3))
    coef = np.reshape(p,(newX.shape[0],newY.shape[1],3))
    if verbose==1: print('Coef. computation 2', tm.time()-tstart)

    return(elem,coef)

# horizontal interpolation
def horiz_interp_delaunay(lonold,latold,varold,lonnew,latnew,elem=0,coef=0):
    """
    lonold: 2D original longitude matrix
    latold: 2D original longitude matrix
    varold: 2D original datra matrix
    lonnew: 2D new longitude matrix
    latnew: 2D new longitude matrix
    print(len(args*))
    """
    ## Horizontal Interpolation from croco varoables'grid to new grid
    ##: get interpolation coefficients
    if np.all(elem==0):
        [elem,coef] = get_tri_coef(lonold, latold,lonnew, latnew)
        coefnorm=np.sum(coef,axis=2)
        coef=coef/coefnorm[:,:,np.newaxis]
        varnew = np.sum(coef*varold.ravel()[elem],2)
        return elem,coef,varnew
    else:
        varnew = np.sum(coef*varold.ravel()[elem],2)
        return varnew

# get sigma levels 
def zlevs(h,zeta,theta_s,theta_b,hc,N,type,vtransform):
    [M,L]=h.shape
    sc_r=np.zeros(N)
    Cs_r=np.zeros(N)
    sc_w=np.zeros(N+1)
    Cs_w=np.zeros(N+1)
    if (vtransform == 2):
        ds=1./N
        if type=='w':
            sc_w[0]   = -1.0
            sc_w[N]   =  0
            Cs_w[0]   = -1.0
            Cs_w[N]   =  0
            sc_w[1:N] = sc_w[1:N]+ds*(np.arange(1,N)-N)
            Cs_w      = csf(sc_w, theta_s,theta_b)
            N=N+1;
        else:
            sc= ds*(np.arange(1,N+1)-N-0.5)
            Cs_r=csf(sc, theta_s,theta_b)
            sc_r=sc
    else:
        cff1=1./np.sinh(theta_s)
        cff2=0.5/np.tanh(0.5*theta_s)
        if type=='w':
            sc=(np.arange(0,N+1)-N)/float(N)
            N = N+1
        else:
            sc = (np.arange(1,N+1)-N-0.5)/float(N)

        Cs = (1-theta_b)*cff1*np.sinh(theta_s*sc)+theta_b*(cff2*np.tanh(theta_s*(sc+0.5))-0.5)
        
    h[h==0] = 1.e-14
    hinv    = 1./h
    z       = np.zeros((N,M,L))
    if (vtransform == 2):
        if type=='w':
            cff1 = Cs_w
            cff2 = sc_w+1
            sc   = sc_w
        else:
            cff1 = Cs_r
            cff2 = sc_r+1
            sc   = sc_r

        h2   = (h+hc)
        cff  = hc*sc
        h2inv = 1./h2
        for k in range(0,N):
            z0       = cff[k]+cff1[k]*h;
            z[k,:,:] = z0*h/(h2) + zeta*(1.+z0*h2inv)
    else:
        print("OH YEAH")
        cff1 = Cs
        cff2 = sc+1
        cff  = hc*(sc-Cs)
        cff2 = sc+1
        for k in range(0,N):
            z0       = cff[k]+cff1[k]*h
            z[k,:,:] = z0+zeta*(1.+z0*hinv)

    return z



def scoordinate(theta_s,theta_b,N,hc,vtransform):
    """ 
    Set S-Curves in domain [-1 < sc < 0] at vertical W- and RHO-points.
    sc_r = np.zeros(N)
    Cs_r = np.zeros(N)
    sc_w = np.zeros(N+1)
    Cs_w = np.zeros(N+1)
    """  
    
    if vtransform == 2:
        print('NEW_S_COORD')
        ds=1./N
        sc_r= ds*(np.arange(1,N+1)-N-0.5)
        Cs_r=csf(sc_r,theta_s,theta_b)
        #
        #    sc_w[0]   = -1.
        #    sc_w[N]   =  0.
        #    Cs_w[0]   = -1.
        #    Cs_w[N]   =  0.
        sc_w = ds*(np.arange(0,N+1)-N)
        Cs_w=csf(sc_w, theta_s,theta_b)
    else:
        print('OLD_S_COORD')
        cff1 = 1.0 / np.sinh(theta_s)
        cff2 = 0.5 / np.tanh(0.5*theta_s)
        sc_w = (np.arange(0,N+1) - N)/N
        Cs_w = (1. - theta_b) * cff1 * np.sinh(theta_s * sc_w) + \
        theta_b * (cff2 * np.tanh(theta_s * (sc_w + 0.5)) - 0.5)
        sc_r= (np.arange(1,N+1)-N-0.5)/N
        Cs_r = (1. - theta_b) * cff1 * np.sinh(theta_s * sc_r) + \
        theta_b * (cff2 * np.tanh(theta_s * (sc_r + 0.5)) - 0.5)
    
    return sc_r,Cs_r,sc_w,Cs_w


# Post Processing Functions for CROCO
#=======================================
#
def get_section(lon1,lon2,lat1,lat2,dgcx,depthsec,hisfile,gridfile,zeta,var):
        """
        This function interpolates along a croco section.

        Input:
        lon1,lon2,lat1,lat2 = longs and lats of starting and ending points of the desired section.
        dgcx     : x - resolution (generally the same horizontal resolution as the model being used)
        depthsec : 1D array of depths increasing (negative)
        hisfile  : path to history file
        gridfile : path to grid file
        zeta     : 2D variable of sea-surface height 
        var      : 3D variable to interpolate 

        Output:
        londom   : longitudes along the x dimension (1D)
        latdom   : latitudes along the y dimension (1D)
        depthsec : depths (1D)
        SECTION  : Interpolated section of the variable (2D) 

        Example:
        lon1,lon2 = 27.8546, 29
        lat1,lat2 = -33.0292,-36.
        dgcx = 3e3
        depthsec = np.arange(-1000,0,5)
        hisfile = '/path/to/file/croco_grd.nc'
        gridfile = '/path/to/file/croco_grd.nc'
        
        crocofile = nc.Dataset('/path/to/file/croco_avg_Y2017M2.nc','r')
        temp = crocofile.variables['temp'][0,:,:,:]
        zeta = crocofile.variables['zeta'][0,:,:]

        londom, depthsec, SECTION_var = get_section(lon1,lon2,lat1,lat2,dgcx,depthsec,hisfile,gridfile,zeta,temp)
        """
        bad_value = 9999
        lonr,latr,h,hc,theta_s,theta_b,N = read_croco_grid(hisfile)
        grd  = nc.Dataset(gridfile,'r')
        lonr = grd['lon_rho'][:]
        latr = grd['lat_rho'][:]
        maskr= grd['mask_rho'][:]
        grd.close
        londom, latdom, xrot = transect_grid(lon1, lat1, lon2, lat2, dgcx, R=6367442.76)
        xrot = xrot/1000
        nzsec     = np.size(depthsec)
        npsec     = np.shape(londom)
        zsec_r    = np.zeros((N+1,npsec[0], npsec[1]))
        # make empty arrays (lower case is for horizontal interpolation & and upper case is for vertical interpolation)
        section = np.zeros((N+1,npsec[0], npsec[1]))
        SECTION =np.zeros((nzsec,npsec[0], npsec[1])) + bad_value
        z_depths  = zlevs(h,zeta,theta_s,theta_b,hc,N,'r',2)
        [elem, coef] = get_tri_coef(lonr, latr, londom, latdom)
        masksec = np.sum(coef*maskr.ravel()[elem],2)
        toposec = np.sum(coef*h.ravel()[elem],2)
        # horizontal interpolation
        for k in range(N):
                zsec_r[k,:,:] = np.squeeze(np.sum(coef*z_depths[k,:,:].ravel()[elem],2))
                var_k = var[k,:,:]
                section[k,:,:] = np.squeeze(np.sum(coef*var_k.ravel()[elem],2)) * masksec
        # vertical interpolation
        for i in range(npsec[0]):
                for j in range(npsec[1]):
                        water_column_depth = np.sum(depthsec>zsec_r[0,i,j])
                        k_start = nzsec - water_column_depth
                        if water_column_depth!=0:
                                f_section = interpolate.interp1d(zsec_r[:,i,j], section[:,i,j], kind='cubic')
                                SECTION[k_start:,i,j] = np.squeeze(f_section(depthsec[k_start:]))
        # mask the section
        SECTION = np.squeeze((np.ma.masked_where((SECTION==bad_value),SECTION)),axis=1)
        londom  = np.squeeze(londom,axis=0)
        return latdom, londom, depthsec, SECTION


def haversine(lat1, lon1, lat2, lon2):
        """
        This function calculates the distance between lon and lat coordinates.
        
        Input:
        lat1, lon1, lat2, lon2 : lons and lats of coordinates in decimal degrees.       

        Output:
        distance in km

        Usage example:
        lon1 = -103.548851
        lat1 = 32.0004311
        lon2 = -103.6041946
        lat2 = 33.374939

        print(haversine(lat1, lon1, lat2, lon2))
                
        """
        R = 6372.8

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))

        return R * c


def get_qpoint_transect(crocofile,lon1,lon2,lat1,lat2,dgc,vtransform):
        """
        This function retrieves the q-point transect. It does this by calculating the 
        q-points from the u- and v-points. A complex algoryth is used to iterate through
        the transect to identify the closest points to the transect. 
        Input:
        crocofile  : path to the crocofile being used (string)
        lon1, lon2, lat1, lat2 : lon and lat positions of the transect. lon1 and lat1 refers
        to the start of the transect and lon2 and lat2 refers to the end of the transect
        dgc        : grid resolution of the model - needs to be equal to or greater than the 
        model gridresolution in orderfor the function to work properly. 
        vtransform : 1 or 2
        Output:
        idx_croco_brokenl : q-point transects
        zu_at_wl, zv_at_wl, dzu, dzv, pnu, pmv : mostly used for the volume transport function 
        below.
        """
    # import important variables
        lonr,latr,h,hc,theta_s,theta_b,N = read_croco_grid(crocofile)
        it=0
        ncroms=nc.Dataset(crocofile)
        pm=ncroms['pm'][:]
        pn=ncroms['pn'][:]
        zeta=ncroms['zeta'][it]
        u=ncroms['u'][it]
        v=ncroms['v'][it]
        ncroms.close()
        # assign some constants
        R=6367442.76
        g=9.806
        rho0=1025.
        #  Define the coordinates at u and v points and calculate q points
        lonu= 0.5*(lonr[:,:-1]+lonr[:,1:])
        latu= 0.5*(latr[:,:-1]+lonr[:,1:])
        lonv= 0.5*(lonr[:-1,:]+lonr[1:,:])
        latv= 0.5*(latr[:-1,:]+latr[1:,:])
        lonq= 0.25*(lonr[:-1,:-1]+lonr[1:,:-1]+lonr[1:,1:]+lonr[:-1,1:])
        latq= 0.25*(latr[:-1,:-1]+latr[1:,:-1]+latr[1:,1:]+latr[:-1,1:])
        lon=lonq
        lat=latq
        #pn-> 1/dy at rho rho point (dy:dist between v point)
        #pm -> 1/dx at rho point (dx: dist between u points)
        pnu=0.5*(pn[:,:-1]+pn[:,1:])
        pmv=0.5*(pm[:-1,:]+pm[1:,:])
        #Build croco z at w levels and on rho ponts C grid, u points C grig  and v points C-grid
        zr_at_wl =  zlevs(h,zeta,theta_s,theta_b,hc,N,'w',vtransform)
        zu_at_wl = 0.5*(zr_at_wl[:,:,:-1]+zr_at_wl[:,:,1:])
        zv_at_wl =  0.5*(zr_at_wl[:,:-1,:]+zr_at_wl[:,1:,:])
        dzu=zu_at_wl[1:,:,:]-zu_at_wl[:-1,:,:]
        dzv=zv_at_wl[1:,:,:]-zv_at_wl[:-1,:,:]
        # Computes the long and latg points of the great circle that goes through the section
        anglesec  = np.pi/180*(lat2-lon1)/(lon1-lat1)
        long,latg,xrot = transect_grid(lon1, lat1, lon2, lat2, dgc, R)
        # Seek the ROMS points clostest to the section
        idx_incroco=[]
        for ip in range(long.size):
            dist=dist_spheric2(latg[0,ip],long[0,ip],lat.ravel(),lon.ravel(),R)
            idx_incroco.append(np.unravel_index(np.argmin(dist),np.shape(lat),order='C'))


        ip1=len(idx_incroco)-1
        while (ip1!=0):
                ip2=ip1-1
                while (ip2!=0):
                        if idx_incroco[ip1]==idx_incroco[ip2]:
                                del idx_incroco[ip1]
                                ip2=0
                        else:
                                ip2=ip2-1
                ip1=ip1-1

        dlonmax=np.max(np.diff(lon[0,:]))
        dlatmax=np.max(np.diff(lat[:,0]))

        idx_croco_brokenl = []
        ip2=-1
        ng_idx = len(idx_incroco)

        for ip in range(ng_idx-1):
            ip2+=1
            idx_croco_brokenl.append(idx_incroco[ip])

            ii_bl=idx_croco_brokenl[ip2][0]
            jj_bl=idx_croco_brokenl[ip2][1]
            ii_ic=idx_incroco[ip+1][0]
            jj_ic=idx_incroco[ip+1][1]

            iloop=0

            while ( (np.abs(lat[ii_bl,jj_bl]-lat[ii_ic,jj_ic])>dlatmax) or \
                    (np.abs(lon[ii_bl,jj_bl]-lon[ii_ic,jj_ic])>dlonmax) or \
                    ( (np.abs(lat[ii_bl,jj_bl]-lat[ii_ic,jj_ic])>1e-6) and \
                      (np.abs(lon[ii_bl,jj_bl]-lon[ii_ic,jj_ic])>1e-6)
                    )
                  ):

                ih=0

                if (np.abs(lat[ii_bl,jj_bl]-lat[ii_ic,jj_ic])>1e-6):
                    ih=ih+1
                if  (np.abs(lon[ii_bl,jj_bl]-lon[ii_ic,jj_ic])>1e-6):
                    ih=ih+1


                    step=1
                    if (ip==np.size(latg)-1):
                        step=-1

                if ih>1:
                    ip2=ip2+1

                    if \
                     (lat[ii_ic,jj_ic]-lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] > 0) and \
                     (lon[ii_ic,jj_ic]-lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] > 0):

                        d1=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1],
                                         lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1],R)

                        d2=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]],
                                         lon[idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]],R)


                        if d1<d2:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1))

                        else:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]))

                    elif \
                     (lat[ii_ic,jj_ic]-lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] < 0) and \
                     (lon[ii_ic,jj_ic]-lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] > 0):

                        d1=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1],
                                         lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1],R)

                        d2=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]],
                                         lon[idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]],R)

                        if d1<d2:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1))                
                        else:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]))


                    elif \
                    (lat[ii_ic,jj_ic]-lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] < 0) and \
                    (lon[ii_ic,jj_ic]-lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] < 0):

                        d1=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1],
                                         lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1],R)

                        d2=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]],
                                         lon[idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]],R)

                        if d1<d2:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1))                
                        else:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]))

                    elif \
                    (lat[ii_ic,jj_ic]-lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] > 0) and \
                    (lon[ii_ic,jj_ic]-lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]] < 0):
                        d1=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                        lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1],
                                        lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1],R)

                        d2=dist_spheric2(lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lat[idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]],
                                         lon[idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]],R)

                        if d1<d2:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1))                
                        else:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]))
                elif ih==1:
                    ip2=ip2+1

                    if np.abs(lat[ii_ic,jj_ic]-lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]]) > dlatmax:

                        d1=dist_spheric2(lat[idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]],
                                         lon[idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]],
                                         lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],R)

                        d2=dist_spheric2(lat[idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]],
                                         lon[idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]],
                                         lat[idx_incroco[ip+1][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+1][0],idx_incroco[ip+step][1]],R)

                        if d1<d2:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0]+1,idx_croco_brokenl[ip2-1][1]))     
                        else:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0]-1,idx_croco_brokenl[ip2-1][1]))    

                    elif np.abs(lon[ii_ic,jj_ic]-lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]]) > dlonmax:

                        d1=dist_spheric2(lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1],
                                         lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1],
                                         lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],R)

                        d2=dist_spheric2(lat[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1],
                                         lon[idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1],
                                         lat[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],
                                         lon[idx_incroco[ip+step][0],idx_incroco[ip+step][1]],R)

                        if d1<d2:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]+1))     
                        else:
                            idx_croco_brokenl.append((idx_croco_brokenl[ip2-1][0],idx_croco_brokenl[ip2-1][1]-1))

                ii_bl=idx_croco_brokenl[ip2][0]
                jj_bl=idx_croco_brokenl[ip2][1]

        idx_croco_brokenl.append(idx_incroco[ip+1])

        return idx_croco_brokenl, zu_at_wl, zv_at_wl, dzu, dzv, pnu, pmv



def volume_transport(idx_croco_brokenl, u, v, zu_at_wl, zv_at_wl, dzu, dzv, pnu, pmv,depth_bl):
        """
        This function calculates the volume transport along the q-point transect. Still needs to be converted
        Sverdrup. 

        Inputs: 
        dx_croco_brokenl = q-point transect defined in the previous function
        depth_bl = max depth to calculate the volume transport.
        u, v = u and v velocity components in 3D
        zu_at_wl, zv_at_wl, dzu, dzv, pnu, pmv = from the q-point transect function above
        
        Outputs:
        voltransport = volume transport of the transect in one time-step.

        """

        voltransport=0

        for ip2 in range(len(idx_croco_brokenl)-1):

                if (idx_croco_brokenl[ip2][1]==idx_croco_brokenl[ip2+1][1]): # Same Longitude
                        if (zu_at_wl[0,idx_croco_brokenl[ip2][0]+1,idx_croco_brokenl[ip2][1]]<= depth_bl):
                                kb=np.argmin(np.abs(zu_at_wl[:,idx_croco_brokenl[ip2][0]+1,idx_croco_brokenl[ip2][1]]-depth_bl))
                        else:
                                kb=0
                        voltransport+=np.sum(u[kb:,idx_croco_brokenl[ip2][0]+1,idx_croco_brokenl[ip2][1]]*
                                                dzu[kb:,idx_croco_brokenl[ip2][0]+1,idx_croco_brokenl[ip2][1]])/\
                                                pnu[idx_croco_brokenl[ip2][0]+1,idx_croco_brokenl[ip2][1]]
                elif (idx_croco_brokenl[ip2][0]==idx_croco_brokenl[ip2+1][0]): #Samre latitude
                        if (zv_at_wl[0,idx_croco_brokenl[ip2][0],idx_croco_brokenl[ip2][1]+1]<= depth_bl):
                                kb=np.argmin(np.abs(zv_at_wl[:,idx_croco_brokenl[ip2][0],idx_croco_brokenl[ip2][1]+1]-depth_bl))
                        else:
                                kb=0
                        voltransport+=np.sum(v[kb:,idx_croco_brokenl[ip2][0],idx_croco_brokenl[ip2][1]+1]*
                                                dzv[kb:,idx_croco_brokenl[ip2][0],idx_croco_brokenl[ip2][1]+1])/\
                                                pmv[idx_croco_brokenl[ip2][0],idx_croco_brokenl[ip2][1]+1]
                elif ( (idx_croco_brokenl[ip2][0]!=idx_croco_brokenl[ip2+1][0]) & 
                                (idx_croco_brokenl[ip2][1]!=idx_croco_brokenl[ip2+1][1])
                                ):
                        print(ip2)
                        print('BUG')

        return voltransport


def rho_eos_v1(zeta,z_r,Tt,Ts,rho0,DUKO_2001,SPLIT_EOS):
        """
        Calculate density anomaly via EOS.

        Inputs:
        zeta : Sea-surface height (2D)
        z_r  : Number of depth levels (float)
        Tt   : Temperature (3D)
        Ts   : Salinity (3D)
        rho0 : Referance Density
        DUKO_2001, SPLIT_EOS : Techniques used to calculate denisty (True/False) 

        Outputs:
        rho, rho1

        """
        qp2=0.0000172
        (N,M,L)=np.shape(Tt)
        dpth=np.tile(zeta,(N,1,1))-z_r
        r00=999.842594
        r01=6.793952E-2
        r02=-9.095290E-3
        r03=1.001685E-4
        r04=-1.120083E-6
        r05=6.536332E-9
        r10=0.824493
        r11=-4.08990E-3
        r12=7.64380E-5
        r13=-8.24670E-7
        r14=5.38750E-9
        rS0=-5.72466E-3
        rS1=1.02270E-4
        rS2=-1.65460E-6
        r20=4.8314E-4
        K00=19092.56
        K01=209.8925
        K02=-3.041638
        K03=-1.852732e-3
        K04=-1.361629e-5
        K10=104.4077
        K11=-6.500517
        K12=0.1553190
        K13=2.326469e-4
        KS0=-5.587545
        KS1=+0.7390729
        KS2=-1.909078e-2
        B00=0.4721788
        B01=0.01028859
        B02=-2.512549e-4
        B03=-5.939910e-7
        B10=-0.01571896
        B11=-2.598241e-4
        B12=7.267926e-6
        BS1=2.042967e-3
        E00=+1.045941e-5
        E01=-5.782165e-10
        E02=+1.296821e-7
        E10=-2.595994e-7
        E11=-1.248266e-9
        E12=-3.508914e-9
        #
        if DUKO_2001:
                Tt0=3.8e0
                Ts0=34.5e0
                sqrtTs0=np.sqrt(Ts0)
                K0_Duk= Tt0*( K01+Tt0*( K02+Tt0*( K03+Tt0*K04 )))    \
                        +Ts0*( K10+Tt0*( K11+Tt0*( K12+Tt0*K13 ))        \
                        +sqrtTs0*( KS0+Tt0*( KS1+Tt0*KS2 )))
        #
        #  compute rho as a perturbation to rho0 (at the surface)
        #
        dr00=r00-rho0
        sqrtTs=np.sqrt(Ts)
        rho1=( dr00 +Tt*( r01+Tt*( r02+Tt*( r03+Tt*(          \
                                            r04+Tt*r05 )))) \
                         +Ts*( r10+Tt*( r11+Tt*( r12+Tt*(   \
                                            r13+Tt*r14 )))  \
                              +sqrtTs*(rS0+Tt*(             \
                                    rS1+Tt*rS2 ))+Ts*r20 ))

        K0= Tt*( K01+Tt*( K02+Tt*( K03+Tt*K04 )))             \
         +Ts*( K10+Tt*( K11+Tt*( K12+Tt*K13 ))              \
              +sqrtTs*( KS0+Tt*( KS1+Tt*KS2 ))) 
        if  SPLIT_EOS:
                if DUKO_2001:
                    qp1=0.1*(rho0+rho1)*(K0_Duk-K0)                 \
                                       /((K00+K0)*(K00+K0_Duk))                                                 
                else:
                        qp1=0.1*(K00*rho1-rho0*K0)/(K00*(K00+K0))
                        rho=rho1+qp1*dpth*(1.-qp2*dpth)
        else:
                K1=B00+Tt*(B01+Tt*(B02+Tt*B03)) +Ts*( B10+Tt*( B11  \
                                            +Tt*B12 )+sqrtTs*BS1 )
                K2=E00+Tt*(E01+Tt*E02) +Ts*(E10+Tt*(E11+Tt*E12))
                cff=K00-0.1*dpth
                cff1=K0+dpth*(K1+K2*dpth)
                rho=( rho1*cff*(K00+cff1)                           \
                                   -0.1*dpth*rho0*cff1              \
                                    )/(cff*(cff+cff1))

        return rho, rho1, #qp1, qp2

def get_relative_vort(pm,pn,lonr,latr,u,v):
        # U[M,L-1]
        #zonal u at u point on one z level (2D horizontal)
        # We take the first value of u just east of the first value of rho
        # We take the last value of u just west of the last value of rho
        # V[M-1,L]
        #meridional v at v point on one z level (2D horizontal)
        # we take the first value of v just north of the first value of rho
        # we take the last value of v just south of the last value of rho

        #pn-> 1/dy at rho rho point (dy:dist between v point)
        #pm -> 1/dx at rho point (dx: dist between u points)
        curlz=0.25*(pm[:-1,:-1]+pm[:-1,1:]+pm[1:,:-1]+pm[1:,1:])*np.diff(v[:,:],1,1)\
        - 0.25*(pn[:-1,:-1]+pn[:-1,1:]+pn[1:,:-1]+pn[1:,1:])*np.diff(u[:,:],1,0)
        lonq=0.25*(lonr[:-1,:-1]+lonr[:-1,1:]+lonr[1:,:-1]+lonr[1:,1:])
        latq=0.25*(latr[:-1,:-1]+latr[:-1,1:]+latr[1:,:-1]+latr[1:,1:])
        return lonq,latq,curlz

def get_potential_vort(u, v, rho, pm, pn, z_simu, N):
    '''
    Calculates the PV using the hydrostatic and Boussinesq assumptions.
    INPUTS
    u, v : zonal and meridional velocity components (3D arrays)
    rho : density (3D array)
    pm, pn : grid spacing from gridfile (2D arrays)
    z_simu : depths of z levels using zlevs function (3D array)
    N : number of z levels (float)

    OUTPUT
    PV : potential vorticity
    '''

    # set constants
    g = 9.81
    rho_0 = 1025
    Y, X = np.shape(pm)
    
    # import variables from grid file
    dx_2d = 1/pm
    dy_2d = 1/pn
    dx = np.zeros((N, Y, X), dtype=float)
    dy = np.zeros((N, Y, X), dtype=float)
    dx_u = np.zeros((N, Y, X-1), dtype=float)
    dx_v = np.zeros((N, Y-1, X-1), dtype=float)
    dy_v = np.zeros((N, Y-1, X), dtype=float)
    dy_u = np.zeros((N, Y-1, X-1), dtype=float)
    
    for i in range(N):
        # deviations along x direction
        dx[i,:,:] = dx_2d
        dx_u[i,:,:] = 0.5 * (dx_2d[:,1:] + dx_2d[:,:-1])
        dx_v[i,:,:] =  0.25 * (dx_2d[:-1,:-1] + dx_2d[:-1,1:] + dx_2d[1:,:-1] + dx_2d[1:,1:])
        
        # deviations along y direction
        dy[i,:,:] = dy_2d
        dy_v[i,:,:] = 0.5 * (dy_2d[1:,:] + dy_2d[:-1,:])
        dy_u[i,:,:] = 0.25 * (dy_2d[:-1,:-1] + dy_2d[1:,:-1] + dy_2d[:-1,1:] + dy_2d[1:,1:])
        
    # deviations along z direction
    dz =  z_simu[1:,:,:] - z_simu[:-1,:,:]
    
    # Partial derivatives at q-point
    # For speed
    dudy_q = (u[:,1:,:] - u[:,:-1,:]) / dy_u         
    dvdx_q = (v[:,:,1:] - v[:,:,:-1]) / dx_v
    
    dvds_q_below = 0.5 * ((v[1:-1, :, :-1] - v[:-2, :, :-1]) / dz[:-1,:-1,:-1] + 
                              (v[1:-1, :, 1:] - v[:-2, :, :-1]) / dz[:-1,:-1,1:])
    dvds_q_above = 0.5 * ((v[2:, :, :-1] - v[1:-1, :, :-1]) / dz[1:,:-1,:-1] + 
                              (v[2:, :, 1:] - v[1:-1, :, :-1]) / dz[1:,:-1,1:]) 
    dvds_q = 0.5 * (dvds_q_above + dvds_q_below)
    
    duds_q_below = 0.5 * ((u[1:-1, 1:, :] - u[:-2, 1:, :]) / dz[:-1, 1:, :-1] + 
                             (u[1:-1, :-1, :] - u[:-2, :-1, :]) / dz[:-1, :-1, :-1])
    duds_q_above = 0.5 * ((u[2:, 1:,:] - u[1:-1, 1:, :]) / dz[:-1, 1:, :-1] +
                             (u[2:, :-1, :] - u[1:-1, :-1, :]) / dz[:-1, :-1, :-1])
    duds_q = 0.5 * (duds_q_above + duds_q_below)
    
    # for densities
    drhodx_q = 0.5 * ((rho[:,:-1, 1:] - rho[:,:-1,:-1])/dx_u[:, :-1,:] +
                      (rho[:,1:, 1:] - rho[:,1:,:-1])/dx_u[:, 1:,:])
    
    drhody_q = 0.5 * ((rho[:,1:,:-1] - rho[:,:-1,:-1])/dy_v[:, :,:-1] +
                      (rho[:,1:,1:] - rho[:,:-1,1:])/dy_v[:, :,1:])
    
    drhods_q_below = 0.25 * ((rho[1:-1, :-1, :-1] - rho[:-2, :-1, :-1])/dz[:-1, :-1, :-1] +
                                (rho[1:-1, 1:, :-1] - rho[:-2, 1:, :-1])/dz[:-1, 1:, :-1] +
                                (rho[1:-1, 1:, 1:] - rho[:-2, 1:, 1:])/dz[:-1,1:,1:] +
                                (rho[1:-1, :-1, 1:] - rho[:-2, :-1, 1:])/dz[:-1, :-1, 1:] )
    drhods_q_above = 0.25 * ((rho[2:, :-1, :-1] - rho[1:-1, :-1, :-1])/dz[1:, :-1, :-1] +
                                (rho[2:, 1:, :-1] - rho[1:-1, 1:, :-1])/dz[1:, 1:, :-1] +
                                (rho[2:, 1:, 1:] - rho[1:-1, 1:, 1:])/dz[1:,1:,1:] +
                                (rho[2:, :-1, 1:] - rho[1:-1, :-1, 1:])/dz[1:, :-1, 1:] )
    drhods_q = 0.5 * (drhods_q_above + drhods_q_below)
    
    # get x,y and z terms from speed and density derivatives (eg. term = distance * density)
    terme_x = - dvds_q * drhodx_q[1:-1, :, :]
    terme_y = duds_q * drhody_q[1:-1, :, :]
    terme_z = (dvdx_q[1:-1, :, :] - dudy_q[1:-1, :, :] + 2 * (2*np.pi/(24*3600))) * drhods_q
    
    # calculate PV using the above terms
    PV = - (g/rho_0) * (terme_x + terme_y + terme_z)
    
    return PV



def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()