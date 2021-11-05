import os
import numpy as np
import rasterio as rs
from rasterio.mask import mask as rs_mask
import plotly.graph_objects as go


class CHM:
    """
    A class to represent surface of a building
    ...
    Attributes
    ----------
    building
        An instance of class Building representing a building in Flanders

    Methods
    -------
    dilate_building_polygon(dilation: int)
        Dilates the polygon
    get_masked_raster(file_link)
    get_local_zip_file_path(file_link)
    get_CHM()
    """

    dem_data_types = ["DSM", "DTM"]

    def __init__(self, selected_building, use_local_copy=False):
        """
        Initializes an instance of the class CHM (Canopy Height Model)
        :param selected_building: An instance of class Building
        """
        # Assign the building object
        self.building = selected_building

        # Dilate the building polygon
        dilation = 5  # in meters
        self.dilate_building_polygon()

        # Load masked data for both DSM and DTM
        self.file_links = []
        self.masked_rasters = []
        self.masked_transforms = []
        self.nodata_values = []
        for dem_data_type in self.dem_data_types:
            file_link = self.building.metadata_building[
                dem_data_type.lower() + "_file_link"
            ].values[0]

            # If use_local_copy is True, a local copy of the zip file can be used
            if use_local_copy:
                file_link = self.get_local_zip_file_path(file_link)

            self.file_links.append(file_link)
            masked_raster, masked_transform, nodata_value = self.get_masked_raster(
                file_link
            )
            # masked_raster = []
            # masked_transform = []
            # nodata_value = []

            print(file_link)

            self.masked_rasters.append(masked_raster)
            self.masked_transforms.append(masked_transform)
            self.nodata_values.append(nodata_value)

        # Calculate the CHM (Canopy Height Model) from DSM and DTM data
        if masked_raster != (0,):  # if valid data was extracted
            self.get_CHM()
        else:
            return

        # Calculate the height of the building
        self.height = np.nanmax(self.masked_raster_chm)

    def __str__(self):
        """
        Prints the address
        """
        return f"{self.building.address}, maximum height: {self.height:.1f} meters"

    def dilate_building_polygon(self, dilation: float = 2):

        self.dilated_polygon = self.building.building_polygon.buffer(dilation)

    def get_masked_raster(self, file_link):

        # GeoTIFF file path
        file_path = file_link

        # Polygon for masking
        dilated_polygon = self.dilated_polygon

        # Access the TIFF file
        try:
            with rs.open(file_path) as src:
                # Mask the file with the dilated polygon
                nodata_value = src.nodata
                masked_raster, masked_transform = rs_mask(
                    src,
                    [dilated_polygon],
                    all_touched=True,
                    nodata=nodata_value,
                    filled=True,
                    crop=True,
                    pad=True,
                    indexes=1,
                )
        except:
            masked_raster, masked_transform = np.ndarray(0), np.ndarray(0)
            nodata_value = np.nan

        return masked_raster, masked_transform, nodata_value

    def get_local_zip_file_path(self, file_link):

        local_file_link = file_link.replace(
            "zip+https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dsm-raster-1m/",
            "zip://.\\data\\",
        )
        local_file_link = local_file_link.replace(
            "zip+https://downloadagiv.blob.core.windows.net/dhm-vlaanderen-ii-dtm-raster-1m/",
            "zip://" + os.getcwd() + "\\data\\",
        )
        local_file_link.replace("\\", "/")
        return local_file_link

    def get_CHM(self):
        # Gets the Canopy Height Model for the building

        # Subtract the DSM data from DTM
        self.masked_raster_chm = self.masked_rasters[0] - self.masked_rasters[1]
        # Set values out of the mask to numpy nan
        mask_nodata = self.masked_rasters[0] == self.nodata_values[0]
        self.masked_raster_chm[mask_nodata] = np.nan

    def plot_CHM_3d(self):

        z_data = self.masked_raster_chm
        x, y = np.arange(z_data.shape[1]), np.arange(z_data.shape[0])
        fig = go.Figure(data=[go.Surface(z=z_data, x=x, y=y)])
        fig.update_layout(
            title=print(self),
            xaxis_title="x",
            yaxis_title="y",
            width=800,
            height=800,
        )
        fig.show()

        return fig
