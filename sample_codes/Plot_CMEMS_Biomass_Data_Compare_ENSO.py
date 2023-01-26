
## Plot CMEMS Biomass (ZOOC) by ENSO Phases

#%%

import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from PIL import Image
import glob

## Boundaries to plot
eez = gpd.read_file("V:/Global_Ocean_Data/Boundary/EEZ/EEZ_v11/eez_boundaries_v11.shp")

gac = gpd.read_file("V:/ffem_sargasso_crtd/Data/Boundary/FFEM_Sargasso_CRTD_Boundary.gdb", layer="CRTD_Geographical_Area_of_Collaboration")


base_path = "V:/ffem_sargasso_crtd/Data"
graphics_path = f"{base_path}/CMEMS_Biomass/graphics/enso"

cmems_folder = f"{base_path}/CMEMS_Biomass/climatology"


#%% Plot by month
c_colors = ['lime','aqua']

for month in range(1,13):

    ## Biomass Rasters
    zooc_pos_raster = xr.open_dataset(f'{cmems_folder}/enso/ZOOC_{month:02d}_positive.nc')
    zooc_neut_raster = xr.open_dataset(f'{cmems_folder}/enso/ZOOC_{month:02d}_neutral.nc')
    zooc_neg_raster = xr.open_dataset(f'{cmems_folder}/enso/ZOOC_{month:02d}_negative.nc')


    ## Plot
    fig = plt.figure(figsize=(9,2.5), tight_layout=True)
    title_text = f"Month {month:02d} - Zooplankton Biomass and ENSO Phase"
    fig.suptitle(title_text)

    # ENSO Positive ZOOC
    ax1 = fig.add_subplot(1,3,1, projection=ccrs.PlateCarree())
    ax1.add_feature(cfeature.LAND, zorder=10)
    ax1.add_feature(cfeature.COASTLINE, linewidth=0.2, edgecolor="dimgrey", zorder=11)

    zooc_pos_raster['zooc'].plot(cmap="plasma", vmin=0, vmax=2, add_colorbar=False)
    CS = zooc_pos_raster['zooc'].plot.contour(levels=[0.7,0.4,0], colors=c_colors, linewidths=.8, add_labels=True)

    labels = ['0.7 g/m$^2$', '0.4 g/m$^2$']
    for i in range(len(labels)): 
        CS.collections[i].set_label(labels[i])
    plt.legend(loc='lower left',prop={'size': 6})

    eez.plot(edgecolor="dimgrey", facecolor="none", linewidth=0.5, ax=ax1)
    gac.plot(edgecolor="darkorange", facecolor="none", linewidth=0.7, ax=ax1) 

    ax1.set_xlim(-112, -77) 
    ax1.set_ylim(0, 20)
    ax1.set_title("ENSO Positive")


    # ENSO Neutral ZOOC
    ax2 = fig.add_subplot(1,3,2, projection=ccrs.PlateCarree())
    ax2.add_feature(cfeature.LAND, zorder=10)
    ax2.add_feature(cfeature.COASTLINE, linewidth=0.2, edgecolor="dimgrey", zorder=11)

    zooc_neut_raster['zooc'].plot(cmap="plasma", vmin=0, vmax=2, add_colorbar=False)
    zooc_neut_raster['zooc'].plot.contour(levels=[0.7,0.4,0], colors=c_colors, linewidths=.8)

    eez.plot(edgecolor="dimgrey", facecolor="none", linewidth=0.5, ax=ax2)
    gac.plot(edgecolor="darkorange", facecolor="none", linewidth=0.7, ax=ax2) 

    ax2.set_xlim(-112, -77) 
    ax2.set_ylim(0, 20)
    ax2.set_title("ENSO Neutral")


    # ENSO Negative ZOOC
    ax3 = fig.add_subplot(1,3,3, projection=ccrs.PlateCarree())
    ax3.add_feature(cfeature.LAND, zorder=10)
    ax3.add_feature(cfeature.COASTLINE, linewidth=0.2, edgecolor="dimgrey", zorder=11)

    zooc_neg_raster['zooc'].plot(cmap="plasma", vmin=0, vmax=2, add_colorbar=False)
    zooc_neg_raster['zooc'].plot.contour(levels=[0.7,0.4,0], colors=c_colors, linewidths=.8)
    eez.plot(edgecolor="dimgrey", facecolor="none", linewidth=0.5, ax=ax3)
    gac.plot(edgecolor="darkorange", facecolor="none", linewidth=0.7, ax=ax3) 

    ax3.set_xlim(-112, -77) 
    ax3.set_ylim(0, 20)
    ax3.set_title("ENSO Negative")


    plt.savefig(f"{graphics_path}/CMEMS_Biomass_ZOOC_ENSO_{month:02d}.png", dpi=300)
    plt.close()

#%% Make GIF
file_list = glob.glob(f"{graphics_path}/CMEMS_Biomass_ZOOC_ENSO_*.png")

frames = [Image.open(image) for image in file_list]
frame_one = frames[0]
frame_one.save(f"{graphics_path}/CMEMS_Biomass_ZOOC_ENSO.gif",        format="GIF", append_images=frames, save_all=True, duration=700, loop=20)
# %%
