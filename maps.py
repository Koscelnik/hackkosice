import csv
import sys
import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup, Canvas
from kivy.graphics.vertex_instructions import Ellipse
from kivy.properties import ObjectProperty

from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup
from kivy.app import App
from kivy.lang import Builder

kv = '''
FloatLayout:
    MyMapView:
        m1: marker1
        m2: marker2
        size_hint: 1, 0.9
        pos_hint: {'y':0.1}
        zoom: 15
        lat: 48.7145
        lon: 21.2503
        double_tap_zoom: True
        MapMarker:
            id: marker1
            lat: 48.7144
            lon: 21.2506
            on_release: app.marker_released(self)
        MapMarker:
            id: marker2
            lat:  48.7154
            lon: 21.2506
            on_release: app.marker_released(self)
            
    Button:
        size_hint: 0.1, 0.1
        text: 'info'
        on_release: app.info()
'''

class MyMapView(MapView):
    grp = ObjectProperty(None)

    def do_update(self, dt):  # this over-rides the do_update() method of MapView
        super(MyMapView, self).do_update(dt)
        self.draw_lines()

    # draw the lines
    def draw_lines(self):
        # Define the radius of the Earth in kilometers
        R = 6371.01

        # Define the center point as a list of latitude and longitude coordinates in degrees
        center_point = [self.m1.lat, self.m1.lon]

                # Convert the latitude and longitude coordinates to radians
                lat1 = math.radians(map_marker.lat)
                lon1 = math.radians(map_marker.lon)

                # Calculate the distance from the center point to a point 1 kilometer to the north, south, east, and west
                d = 2  # 2x0.5 kilometer
                lat_north = math.degrees(math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(0)))
                lon_north = math.degrees(lon1 + math.atan2(math.sin(0) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_north)))

                north_point = [lat_north, lon_north]
                markers.append([map_marker, north_point])

            return markers

        
        super().__init__(**kwargs)
        self.Markers = loadMarkers()

class Mapp(App):
    def build(self):
        return Builder.load_string(kv)

    def info(self, *args):
        print(self.root.ids.marker1)
        print(self.root.ids.marker2)

    def marker_released(self, marker):
        print(marker)

MapViewApp().run()