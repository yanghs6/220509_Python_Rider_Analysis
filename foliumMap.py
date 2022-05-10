import folium
import pandas as pd
import json


class FoliumMap:
    """map class using folium
    """
    def __init__(self, center:tuple, zoom_scale=12) -> None:
        """Initialize map object of type folium.Map

        Args:
            center (tuple): (latitude, longitude) tuple
            zoom_scale (int, optional): Zoom scale. Defaults to 12.
        """
        self.folium_map = folium.Map(location=center, zoom_start=zoom_scale)
        
    def set_center(self, lat:float, lng:float) -> None:
        """Set center of folium map

        Args:
            lat (float): Latitude
            lng (float): Longitude
            
        Raises:
            Exception: If lat or lng is not numeric
        """
        if type(lat) in [int, float] and type(lng) in [int, float]:
            self.folium_map.location = (lat, lng)
        else:
            raise Exception("TypeError: latitude and longitude must be numeric")
        
    def set_zoom_scale(self, zoom:int) -> None:
        """Set zoom scale

        Args:
            zoom (int): Zoom scale(1~18).

        Raises:
            Exception: If zoom is not interger
        """
        if type(zoom) == int:
            if zoom < 1:
                zoom = 1
            if zoom > 18:
                zoom = 18
                
            self.folium_map.options["zoom"] = zoom
        else:
            raise Exception("TypeError: latitude and longitude must be integer")
    
    def get_map_info(self) -> dict:
        """Return map basic info.

        Returns:
            dict: Dictionary with center of map and options
        """
        info = {"center": self.folium_map.location,
                "options": self.folium_map.options,}
        
        return info
        
    def make_marker(self, loc_df:pd.DataFrame) -> None:
        """Make marker on folium map.

        Args
            center (tuple): latitude, longitude
            loc_df (pandas.Dataframe): dataframe with columns(name, lat, lng)
        """
        for i in range(loc_df.shape[0]):
            name, lat, lng = loc_df.loc[i, ["name", "lat", "lng"]]
            popup = f'<div style="width:150px">{name}</div>'
            
            folium.Marker([lat, lng], popup=popup).add_to(self.folium_map)
            
    def make_bound(self, geo_path:str) -> None:
        """Make boundary with geojson

        Args:
            geo_path (str): Geojson file path
        """
        geo_str = json.load(open(geo_path, encoding='utf-8'))
        folium.GeoJson(geo_str, name="seoul", style_function=lambda x:{"fillColor":"yellow", "color":"black", "weight":2, "fillOpacity":0.15}, popup=folium.GeoJsonPopup(fields=['name']))\
            .add_to(self.folium_map)
            
    def make_circle(self, loc_df:pd.DataFrame, **kwargs) -> None:
        """Make circle on folium map.

        Args:
            loc_df (pd.DataFrame): dataframe with columns(name, lat, lng)
        Kwargs:
            radius (int): Radius. unit is "m". Defaults to 5000
            weight (float): Weight of line. Defaults to 3
            color (str): Color of line. Defaults to brown
            fill (bool): Whether to color. Defaults to True
            fill_opacity (str): Fill opacity. Defaults to 0.3
            fill_color (str): Fill color. Defaults to coral
        """
        radius = kwargs["radius"] if "radius" in kwargs else 5000
        weight = kwargs["weight"] if "weight" in kwargs else 3
        color = kwargs["color"] if "color" in kwargs else 'brown'
        fill = kwargs["fill"] if "fill" in kwargs else True
        fill_opacity = kwargs["fill_opacity"] if "fill_opacity" in kwargs else 0.3
        fill_color = kwargs["fill_color"] if "fill_color" in kwargs else 'coral'
        
        for i in range(loc_df.shape[0]):
            name, lat, lng = loc_df.loc[i,["name", "lat", "lng"]]
            popup = f'<div style="width:150px">{name}</div>'
            
            folium.Circle([lat, lng],
                          radius=radius,
                          weight=weight,
                          color=color,
                          fill=fill,
                          fill_color=fill_color,
                          fill_opacity=fill_opacity,
                          popup=popup
            ).add_to(self.folium_map)

    def clear(self) -> None:
        """initialize map and clear marker.
        """
        center = self.folium_map.location
        zoom = self.folium_map.options["zoom"]
        self.folium_map = folium.Map(center, zoom_start=zoom)

    def display(self) -> None:
        """display folium map. works only in jupyter(.ipynb).
        """
        try:
            display(self.folium_map)
        except NameError:
            print(f"현재 파일에서는 화면 출력이 어렵습니다.")
            print("ipynb 확장자에서 실행할 수 있습니다.")
            
    def save(self, outfile, close_file: bool = True) -> None:
        """Saves an Element into a file.
        """
        self.folium_map.save(outfile, close_file)


if __name__ == "__main__":
    # Seoul center
    center = (37.55, 126.98)
    # zoom scale
    scale = 12
    # locations
    loc_df = pd.DataFrame({
                            "name": ["강남역", "서울역", "구로디지털단지"],
                            "lat": [37.4979126, 37.5546, 37.4853],
                            "lng": [127.0276946, 126.9708, 126.9015]
                          })
    
    folium_map = FoliumMap(center)
    folium_map.make_marker(loc_df)
    folium_map.make_circle(loc_df)
    folium_map.display()
    folium_map.set_zoom_scale(10)
    folium_map.clear()
    folium_map.display()
    print(folium_map.get_map_info())
