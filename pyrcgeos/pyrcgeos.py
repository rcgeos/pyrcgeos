"""Main module."""

import random
import string
import ipyleaflet

class Map(ipyleaflet.Map):
    """Map class to add Map, basemap, layers and controls

    Args:
        ipyleaflet (_type_): _description_
    """    
    def __init__(self, center, zoom, **kwargs) -> None:
        """Add center (Lat, Lon), zoom

        Args:
            center (_type_): _description_
            zoom (_type_): _description_
        """        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"]=True
        super().__init__(center=center, zoom=zoom, **kwargs)

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