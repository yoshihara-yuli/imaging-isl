import sys,os
import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as cm
import cv2

plt.rcParams["font.size"]=16

def main():

    data = np.loadtxt("data.txt",delimiter=" ",skiprows=1).T
    plot(data[0],data[1],data[2],filname="1")
    data2 = np.loadtxt("data2.txt",delimiter=" ",skiprows=1).T
    plot(data2[0],data2[1],data2[2],filname="2")

    data = np.hstack((data,data2)) # merge data
    print np.shape(data)
    data_x = data[0] # x [mm]
    data_y = data[1] # y [mm]
    data_A = data[2] # A [mA]

    plot(data_x,data_y,data_A,filname="sum")

    xbins,ybins = 21,31
    x = np.linspace(-10,60,xbins)
    y = np.linspace(-10,80,ybins)
    X = np.meshgrid(x,y)[0]
    Y = np.meshgrid(x,y)[1]
    #map_ = np.zeros((ybins,xbins))

    map_ = mapping(data_x,data_y,data_A,X,Y,False,100)
    map_ = cv2.blur(map_,(5,5))
    plt.figure(figsize=(5,6))
    plt.title("mapping")
    plt.pcolor(X,Y,map_,cmap=cm.jet)
    plt.colorbar()
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.tight_layout()
    plt.savefig("mapping.png")
    plt.show()

def plot(data_x,data_y,data_A,filname=""):
    plt.figure(figsize=(5,6))
    plt.title("Track-%s"%filname)
    plt.plot(data_x,data_y,"k",linewidth=1)
    plt.scatter(data_x,data_y,c=data_A,s=60,alpha=0.5,cmap=cm.jet)
    cbar = plt.colorbar()
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    cbar.set_label('Current [mA]', rotation=90)
    plt.tight_layout()
    plt.savefig("measured_track_%s.png"%filname)

def mapping(data_x,data_y,data_A,X,Y,weight=False,noise=10):

    map_ = np.zeros(np.shape(X))
    dr2_sum = np.zeros((len(data_x),np.shape(X)[0],np.shape(X)[1]))

    for i in range(len(data_x)):

        if data_A[i]<noise: continue
        dr2 = np.square(X-data_x[i])+np.square(Y-data_y[i])
        dr2[dr2<1]=1. # to prevent memory consuming (<1mm)
        
        if weight==True: # w. weighting factor
            dr2_sum = dr2_sum + dr2
            tempmap = data_A[i]/dr2/np.sqrt(dr2) 
        else:            # w.o. weighting factor
            tempmap = data_A[i]/dr2 

        tempmap[np.isnan(tempmap)]=0.
        map_ = map_ + tempmap

    if weight==True:
        map_ = map_*np.sum(np.sqrt(dr2_sum))

    return map_



if __name__=="__main__":
    main()
    sys.exit("fin")
