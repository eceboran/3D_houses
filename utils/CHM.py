


class CHM():
    """
    A class to represent an building in Flanders
    Inherits from class Address
    ...
    Attributes
    ----------
    input_address : str
        Input address from the user
    metadata_file_path: str (optional)
        File path for the metadata csv file
    valid_address_conditional: bool
        True if the input address is valid
    suggestions: dict
        Suggestions for the input address
    address_info: dict
        Detailed address information, including location
    address: str
        Formatted address
    street_name: str
        Street name
    house_no: str
        House number
    municipality: str
        Municipality name
    zipcode: str
        Municipality zipcode
    Location: dict
        Location in WGS87 and Lambert73 coordinates
    building_polygon
        Shapely polygon object representing the building
    building_coords
        Coordinates of the building polygon with n sides in the form
        [[x1, y1]
         [x2, y2]
         ...
         [xn, yn]]
    area: float
        Area of the building
    default_metadata_file_path: str
        Default path for GeoTIFF metadata csv file
        Used if metadata_file_path is not given
    metadata_all_files
        DataFrame for GeoTIFF metadata for all files
    metadata_single_file
        DataFrame for GeoTIFF file(s) containing the building polygon

    Methods
    -------
    get_default_GeoTIFF_metadata_file_path(cls)
        Gets the default file path for the GeoTIFF metadata csv file
    load_GeoTIFF_metadata(cls, csv_file_path: str)
        Loads GeoTIFF metadata from given csv file
    get_GeoTIFF_file_index_single_point(self, x: float, y: float)
        Gets the GeoTIFF file number for the file containing the point (x,y)
    get_building_GeoTIFF_metadata(self)
        Gets the GeoTIFF metadata for the file(s) containing the building polygon
    """

    def __init__(self, input_address: str, metadata_file_path: str = ""):
        """
        Initializes an instance of the class Building
        :param input_address: input address from the user
        """
        # Initialize the instance from the parent class
        super().__init__(input_address)

        # For a valid address, get the building information
        if self.valid_address_conditional:
            self.address_info = self.get_address_location(self.input_address)
        else:
            return

        # Generate default (relative) file path for GeoTIFF metadata
        self.get_default_GeoTIFF_metadata_file_path()

        # GeoTIFF Metadata file path
        if len(metadata_file_path) > 0:
            self.metadata_file_path = metadata_file_path
        else:
            self.metadata_file_path = self.default_metadata_file_path

        # Load GeoTIFF metadata
        self.load_GeoTIFF_metadata(self.metadata_file_path)

        # Get GeoTIFF file numbers corresponding to the building polygon
        self.get_building_GeoTIFF_metadata()

    def __str__(self):
        """
        Prints the address
        """
        return f"{self.address}"

    @classmethod
    def get_default_GeoTIFF_metadata_file_path(cls):
        """
        Gets the default file path for the GeoTIFF metadata csv file
        """
        # File paths for metadata for DSM and DTM datasets
        metadata_folder_path = ".\\data\\metadata\\"

        # Metadata csv file path
        default_metadata_file_path = os.path.join(
            metadata_folder_path, "GeoTIFF_1m_metadata_processed.csv"
        )

        cls.default_metadata_file_path = default_metadata_file_path

    @classmethod
    def load_GeoTIFF_metadata(cls, csv_file_path: str):
        """
        Loads GeoTIFF metadata from given csv file
        :param csv_file_path: A string representing an address
        """
        # Load metadata DataFrame
        df_metadata = pd.read_csv(csv_file_path, sep=",", index_col=0)
        cls.metadata_all_files = df_metadata

    def get_GeoTIFF_file_index_single_point(self, x: float, y: float):
        """
        Gets the GeoTIFF file number for the file containing the point (x,y)
        :param x: x-coordinate of the point
        :param y: y-coordinate of the point
        """
        df = self.metadata_all_files
        index_cond = (x > df.left) & (x <= df.right) & (y > df.bottom) & (y <= df.top)
        index_file = np.flatnonzero(index_cond)[0]

        return index_file

    def get_building_GeoTIFF_metadata(self):
        """
        Gets the GeoTIFF metadata for the file(s) containing the building polygon
        """
        # Boundaries of the polygon (left bottom right top)
        polygon_bounds = self.building_polygon.bounds

        index_file = []
        # Top left
        index_file.append(
            self.get_GeoTIFF_file_index_single_point(
                polygon_bounds[0], polygon_bounds[3]
            )
        )
        # Top right
        index_file.append(
            self.get_GeoTIFF_file_index_single_point(
                polygon_bounds[2], polygon_bounds[3]
            )
        )
        # Bottom left
        index_file.append(
            self.get_GeoTIFF_file_index_single_point(
                polygon_bounds[0], polygon_bounds[1]
            )
        )
        # Bottom right
        index_file.append(
            self.get_GeoTIFF_file_index_single_point(
                polygon_bounds[2], polygon_bounds[1]
            )
        )

        self.metadata_building = (
            self.metadata_all_files.iloc[index_file]
        ).drop_duplicates()
