import csv
import sys
import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup, Canvas
from kivy.graphics.vertex_instructions import Ellipse
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup
from kivy.app import App
from kivy.lang import Builder

class SchoolMarker(MapMarker):
    color = (0, 0, 1, 0.5)

class Markers(MapMarker):

    def __init__(self, **kwargs):

        def loadMarkers():
            file_path = "stredne_skoly.csv"
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)
                data = list(csvreader)

            markers = list()

            for marker in data:
                map_marker = MapMarkerPopup(lat=marker[19], lon=marker[20], popup_size=(100, 50))
                map_marker.add_widget(Label(text=marker[2], color=(1,0,1,1)))
                
                
                # Define the radius of the Earth in kilometers
                R = 6371.01

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
        layout = BoxLayout(orientation='vertical')
        mapview = MapView(zoom=11, lat=48.7145, lon=21.2503)

        markers = Markers()

        max_zoom = 20
        min_zoom = 11

        def on_zoom(mapview, zoom):
            if zoom > max_zoom:
                mapview.zoom = max_zoom
            elif zoom < min_zoom:
                mapview.zoom = min_zoom
           
        mapview.bind(zoom=on_zoom)

        for marker in markers.Markers:
            mapview.add_marker(marker[0])

        def update(mapview, zoom):
            for child in mapview.canvas.children:
                if type(child) is Ellipse:
                    mapview.canvas.remove(child)
            print("newset")
            for marker in markers.Markers:
                tmp_marker = MapMarker(lat = marker[1][0], lon = marker[1][1])
                mapview.add_marker(tmp_marker)
                radius = tmp_marker.y - marker[0].y
                mapview.remove_marker(tmp_marker)

                with mapview.canvas:
                    Color(0,1,0,0.2)  # line color
                    circle = Ellipse(pos = (marker[0].center_x - radius/2, marker[0].center_y - radius/2), size = (radius, radius))
                    
                    west, south, east, north=mapview.get_bbox()
                    west, south = mapview.get_window_xy_from(west, south, mapview.zoom)
                    east, north = mapview.get_window_xy_from(east, north, mapview.zoom)
                    
                    if (west < marker[0].center_x - radius/2 and marker[0].center_x- radius/2 < east and south < marker[0].center_y- radius/2 and  marker[0].center_y- radius/2 < north and west < marker[0].center_x + radius/2 and marker[0].center_x+ radius/2 < east and south < marker[0].center_y+ radius/2 and  marker[0].center_y+ radius/2 < north):
                        mapview.canvas.add(circle)
                        print(str(west) +" < "+ str(marker[0].center_x + radius/2) +" and "+ str(marker[0].center_x- radius/2) +" < "+ str(east) +" and "+ str(south) +" < "+ str(marker[0].center_y- radius/2) +" and "+  str(marker[0].center_y+ radius/2) +" < "+ str(north))
                        print("add")
                    else:
                        mapview.canvas.remove(circle)
                        #print("remove")
    

        #mapview.bind(zoom = update)
        mapview.bind(lon=update)
        visible_markers = True

        def toggle_markers_visibility(button):
            nonlocal visible_markers
            if visible_markers:
                for marker in markers.Markers:
                    mapview.remove_marker(marker)
                button.text = "Show schools"
            else:
                for marker in markers.Markers:
                    mapview.add_marker(marker)
                button.text = "Hide schools"
            visible_markers = not visible_markers

        hide_markers_button = Button(text="Hide markers", size_hint=(0.5, 0.5))
        hide_markers_button.bind(on_press=toggle_markers_visibility)

        layout.add_widget(mapview)
        #layout.add_widget(hide_markers_button)

        return layout


Mapp().run()