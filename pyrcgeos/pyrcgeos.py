"""Main module."""

import random
import string
import ipyleaflet

class Map(ipyleaflet.Map):
    """Map class to add Map, basemap, layers and controls

    Args:
        ipyleaflet (ipyleaflet.Map): An ipyleaflet map.
    """    
    def __init__(self, **kwargs) -> None:
        """Add center (Lat, Lon), zoom

        Args:
            center (_type_): _description_
            zoom (_type_): _description_
        """   
        if "center" not in kwargs:
            kwargs["center"] = [40, -100]

        if "zoom" not in kwargs:
            kwargs["zoom"] = 4        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"]=True
        super().__init__(**kwargs)

        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True
        if "layers_control":
            self.add_layers_control()
        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
        if "fullscreen_control":
            self.add_fullscreen_control(position="topleft")
        self.add_draw_control()
        self.add_search_control(position="topleft")

    def add_search_control(self, position="topleft",**kwargs):
        """Add Search Control button 
        """        
        if "url" not in kwargs:
            kwargs['url'] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
      
        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

    def add_draw_control(self,**kwargs):
        """Adds a draw control to the map.
        Args: 
            kwargs: Keyword arguments to pass to the draw control
        """        
        draw_control = ipyleaflet.DrawControl(**kwargs)
        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }
        self.add_control(draw_control)

    def add_layers_control(self, position="topright", **kwargs):
        """Add a layers control to the map. 
        Args: 
            kwargs: Keyword arguments to pass to the layers control
        """        
        layers_control = ipyleaflet.LayersControl(position=position,**kwargs)
        self.add_control(layers_control)

    def add_fullscreen_control(self, position="topleft"):
        """Add a fullscreen control to the map

        Args:
            position (str, optional): _description_. Defaults to "topleft".
        """        
        fullscreen_control=ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)

    def add_tile_layer(self, url, name, attribution,**kwargs):
        """Adds a tile layer to the map.

        Args:
            url (_type_): _description_
            name (_type_): _description_
            attribution (_type_): _description_
        """        
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)

    def add_basemap(self, basemap, **kwargs):

        import xyzservices.providers as xyz

        if basemap.lower()=="roadmap":
            url='http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, attribution='Google Roadmap', **kwargs)
        elif basemap.lower()=="satellite":
            url='http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, attribution='Google Satellite', **kwargs)
        else: 
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution,**kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found")
    def add_geojson(self, data, name="GeoJSON",**kwargs): 
        """Adds a GeoJSON layer to the map

        Args:
            data (dict): The GeoJSON data
        """    
        if isinstance(data,str):
            import json
            with open(data, "r") as f:
                data = json.load(f)    
        geojson = ipyleaflet.GeoJSON(data=data, name=name,**kwargs)
        self.add_layer(geojson)

    def add_shp(self, data, name="Shapefile", **kwargs):
        """Add a Shapefile layer to the map

        Args:
            data (str): The Path to the Shapefile
            name (str, optional): Name of the layer. Defaults to "Shapefile".
        """        
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)
    
    
    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Adds a raster layer to the map.
        Args:
            url (str): The URL of the raster layer.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the map bounds to the raster layer. Defaults to True.
        """
        import httpx

        titiler_endpoint = "https://titiler.xyz"

        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }, 
            verify=False # Added this to address SSL certificate missing temporarily
        ).json()

        bounds = r["bounds"]

        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            },
            verify=False # Added this to address SSL certificate missing temporarily
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

def generate_random_string(length=10, upper=False, digits=False, punctuation=False):
    """Generate a random string of a given length

    Args:
        length (int, optional): _description_. Defaults to 10.
        upper (bool, optional): _description_. Defaults to False.
        digits (bool, optional): _description_. Defaults to False.
        punctuation (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: The generated string
    """    
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_lowercase
    if digits:
        letters += string.digits
    if punctuation:
        letters += string.punctuation
    #print(letters)
    return ''.join(random.choice(letters) for i in range(length))

def generate_lucky_number(length=1):
    """Generate a random string of a given length

    Args:
        length (int, optional): _description_. Defaults to 1.

    Returns:
        _type_: Digits of a defined length
    """    
    result_str = ''.join(random.choice(string.digits) for i in range(length))
    return int(result_str)