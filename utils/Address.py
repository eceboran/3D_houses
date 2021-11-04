import requests as req
import shapely.geometry as geom


class Address:
    """
    A class to represent an address in Flanders
    ...
    Attributes
    ----------
    input_address : str
        Input address from the user
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

    Methods
    -------
    verify_address(address: str)
        Checks if a given address is a valid address in Flanders
        Makes suggestions for incomplete addresses
    get_address_location(address: str) -> dict
        Gets the location and formatted address for an address in Flanders
    get_building_shape(address_params: dict)
        Gets the shape of a building in Flanders with a given address
    """

    def __init__(self, input_address: str):
        """
        Initializes an instance of the class Address
        :param input_address: input address from the user
        """
        # Assign attribute icon
        self.input_address = input_address

        # Verify the address
        self.valid_address_conditional, self.suggestions = self.verify_address(
            self.input_address
        )

        # For a valid address, get the location
        if self.valid_address_conditional:
            self.address_info = self.get_address_location(self.input_address)
        else:
            return

        # Attributes for address information
        location_result = self.address_info["LocationResult"][0]
        self.address = location_result["FormattedAddress"]
        self.street_name = location_result["Thoroughfarename"]
        self.house_no = location_result["Housenumber"]
        self.municipality = location_result["Municipality"]
        self.zipcode = location_result["Zipcode"]
        self.Location = location_result["Location"]

        # Get the polygon representing the building
        address_params = {
            attr: getattr(self, attr)
            for attr in ["municipality", "zipcode", "street_name", "house_no"]
        }

        self.building_polygon, self.building_coords = self.get_building_shape(
            address_params
        )

    def __str__(self):
        """
        Prints the address
        """
        return f"{self.address}"

    @staticmethod
    def verify_address(address: str, no_suggestions=10):
        """
        Verifies whether an address is in Flanders
        Makes suggestions for incomplete addresses
        :param address: A string representing an address
        :param no_suggestions: An integer for the number of suggestions
        :return valid_address_conditional: A boolean that is True if the address is valid
        :return suggestions: Suggestions for addresses
        """
        # API request from Geopunt Flanders
        url = f"https://loc.geopunt.be/v4/Suggestion?q={address}&c={no_suggestions}"
        # Get the address suggestions
        try:
            suggestions = req.get(url)
            suggestions = suggestions.json()
            valid_address_conditional = len(suggestions["SuggestionResult"]) == 1
        except:
            valid_address_conditional = False  # address not found
            suggestions = {}

        return valid_address_conditional, suggestions

    @staticmethod
    def get_address_location(address: str) -> dict:
        """
        Gets the location and formatted address for an address in Flanders
        :param address: A string representing an address
        :return address_info: Suggestions for addresses
        """
        # API request from Geopunt Flanders
        no_suggestions = 1
        url = f"https://loc.geopunt.be/v4/Location?q={address}&c={no_suggestions}"
        # Get the address suggestions
        try:
            address_info = req.get(url)
            address_info = address_info.json()
        except:
            address_info = {}

        return address_info

    @staticmethod
    def get_building_shape(address_params: dict):
        """
        Gets the shape of a building in Flanders with a given address
        :param address_params: A dictionary representing an address
        :return polygon_building: Suggestions for addresses
        """
        # URL for the address match
        url_address_match = "https://api.basisregisters.vlaanderen.be/v1/adresmatch"
        # API request for the address match
        address_match = req.get(
            url_address_match,
            params={
                "gemeentenaam": address_params["municipality"],
                "postcode": address_params["zipcode"],
                "straatnaam": address_params["street_name"],
                "huisnummer": address_params["house_no"],
            },
        )
        address_match = address_match.json()

        # URL for the building unit
        url_building_unit = address_match["adresMatches"][0]["adresseerbareObjecten"][
            0
        ]["detail"]

        # API request for the building unit
        building_unit = req.get(url_building_unit)
        building_unit = building_unit.json()

        # URL for the building
        url_building = building_unit["gebouw"]["detail"]

        # API request for the building
        building = req.get(url_building)
        building = building.json()

        # Coordinates of the polygon for the building
        building_coords = building["geometriePolygoon"]["polygon"]["coordinates"][0]

        # Polygon for the building
        building_polygon = geom.Polygon(building_coords)

        return building_polygon, building_coords
