#import random
#import string
import folium

class Map(folium.Map):
    def __init__(self, center=[40,-100], zoom=2, **kwargs) -> None: 
        """Create a folium map object

        Args:
            center (list, optional): _description_. Defaults to [40,-100].
            zoom (int, optional): _description_. Defaults to 2.
        """        
        super().__init__(location=center, zoom_start=zoom, **kwargs)
    def add_tile_layer(self, url, name, attribution ="", **kwargs):
        """Add a tile layer

        Args:
            url (_type_): _description_
            name (_type_): _description_
            attribution (str, optional): _description_. Defaults to "".
        """        

        tile_layer = folium.TileLayer(
            tiles=url,
            name=name,
            attr=attribution,
            **kwargs
        )
        self.add_child(tile_layer)


