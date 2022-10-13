import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pyresample as pr
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


def readPGMFile(pgm_file):
    cntS = np.fromfile(pgm_file,dtype='uint8')
    dsize=1800
    arraysize=dsize*dsize
    cntS = cntS[-arraysize:]
    cntS = cntS.reshape((dsize,dsize))
    return cntS

def plotTemp(cntS):
    Source_def = pr.load_area('Table/Projection.proj','KoChi_1800') # 原始FDK資料的投影
    Image_def = pr.load_area('Table/Projection.proj','LCC_1000')  # 輸出圖檔的投影
    cnts_new=pr.kd_tree.resample_nearest(Source_def,cntS,Image_def,radius_of_influence=50000)
    crs=Image_def.to_cartopy_crs()
    fig=plt.figure()
    ax=plt.axes(projection=crs)
    setGridAndCoastline(ax)
    ax.imshow(cnts_new,cmap='viridis',extent=crs.bounds)
    fig.savefig('PGM.png')

def setGridAndCoastline(ax):
    gl=ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_left = False
    gl.ylabels_right=True
    gl.xlines = True
    gl.xlocator = mticker.FixedLocator([100,120, 140])
    gl.ylocator = mticker.FixedLocator([20, 40])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'color': 'red', 'weight': 'bold'}
    ax.coastlines(resolution='10m',color='black',linewidth=1.3)   

if __name__ == '__main__':
    pgm_file='HMW822090416IR1.pgm'
    cnt=readPGMFile(pgm_file)
    plotTemp(cnt)