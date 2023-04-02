import csv
import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapMarker
from kivy.uix.button import Button
from kivy_garden.mapview import MapMarkerPopup, MapView


def load_csv(file_path):
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        data = list(csvreader)

    return data


class SchoolMarker(MapMarker):
    color = (0, 0, 1, 1)


class Mapp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        mapview = MapView(zoom=11, lat=48.7145, lon=21.2503)

        max_zoom = 20
        min_zoom = 11

        def on_zoom(mapview, zoom):
            if zoom > max_zoom:
                mapview.zoom = max_zoom
            elif zoom < min_zoom:
                mapview.zoom = min_zoom
        mapview.bind(zoom=on_zoom)

        file_path = "Stredne skoly.csv"
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)
            data = list(csvreader)

        markers = list()
        visible_markers = True

        for marker in data:
            
            map_marker = MapMarkerPopup(lat=marker[19], lon=marker[20], popup_size=(100, 50))
            map_marker.add_widget(Label(text=marker[2], color=(1,0,1,1)))
            markers.append(map_marker)
            mapview.add_marker(map_marker)

        def toggle_markers_visibility(button):
            nonlocal visible_markers
            if visible_markers:
                for marker in markers:
                    mapview.remove_marker(marker)
                button.text = "Show schools"
            else:
                for marker in markers:
                    mapview.add_marker(marker)
                button.text = "Hide schools"
            visible_markers = not visible_markers

        hide_markers_button = Button(text="Hide markers", size_hint=(0.5, 0.5))
        hide_markers_button.bind(on_press=toggle_markers_visibility)

        layout.add_widget(mapview)
        layout.add_widget(hide_markers_button)

        return layout


if __name__ == '__main__':
    Mapp().run()