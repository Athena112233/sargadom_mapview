
## D1 Report Maps
## SS CHLA


#%%
import geopandas as gpd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import calendar


## Folders
base_folder = "V:/ffem_sargasso_crtd/Data"
data_folder = f"{base_folder}/MODIS_CHLA/google_earthengine/climatologies/chlor_a/SS/None"
graphics_folder = f"{base_folder}/_D1_Report_Maps/graphics"

## Boundaries to plot
eez = gpd.read_file("V:/Global_Ocean_Data/Boundary/EEZ/EEZ_v11/eez_boundaries_v11.shp")

gac = gpd.read_file("V:/ffem_sargasso_crtd/Data/Boundary/FFEM_Sargasso_CRTD_Boundary.gdb", layer="SargassoSea_Geographical_Area_of_Collaboration")


#%% Plot
fig = plt.figure(figsize=(6.3, 7))
for month in range(1,13):

    ax1 = fig.add_subplot(4,3,month, projection=ccrs.PlateCarree())

    ax1.add_feature(cfeature.LAND, zorder=10)
    ax1.add_feature(cfeature.COASTLINE, linewidth=0.2, edgecolor="dimgrey", zorder=11)

    plot_raster = xr.open_rasterio(f'{data_folder}/MODIS_chlor_a_SS_{month:02d}.tif')
    plot_raster = plot_raster.sel(band=1)
    raster_in = plot_raster.plot(cmap="turbo", vmin=0, vmax=2, add_colorbar=False)

    eez.plot(edgecolor="lightgrey", facecolor="none", linewidth=0.5, ax=ax1)
    gac.plot(edgecolor="darkorange", facecolor="none", linewidth=0.7, ax=ax1) 

    ax1.set_xlim(-80,-25) 
    ax1.set_ylim(15,45)
    ax1.set_title('')

    month_str = calendar.month_abbr[month]
    ax1.text(0.97, 0.1, month_str, zorder=11, va="center", ha="right", bbox={'facecolor':'whitesmoke', 'alpha':0.9, 'pad':2}, transform=ax1.transAxes)

## color bar, left, bottom, width, height 
fig.subplots_adjust(bottom=0.09, top=1)
cbar_ax = fig.add_axes([0.2, 0.06, 0.6, 0.02])
fig.colorbar(raster_in, cax=cbar_ax, label="Chlorophyll A Concentration, mg/m$^3$", orientation="horizontal")

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.02, hspace=0.01)

fig.savefig(f"{graphics_folder}/SS_CHLA_Overview.png", dpi=300)

# %%
