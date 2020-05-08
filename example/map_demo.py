# encoding: utf-8
"""
@author: Michael
@file: map_demo.py
@time: 2020/4/21 3:48 PM
@desc:
"""
import folium
from folium import GeoJsonTooltip

from lamina import DynamicGeoJson, create_base_map, DynamicGeoJsonTooltip


def create_geo_layer():
    def geo_color(fc):
        return ['red', 'orange', 'lightblue', 'green', 'darkgreen'][fc - 1]

    def geo_fill_color(fc):
        return 'red' if fc == 1 else "transparent"

    tooltip = DynamicGeoJsonTooltip(
        fields=["fc", "rt", "rst", "nr", "isbridge"],
        # aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
        aliases=["fc", "rt", "rst", "nr", "isbridge"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 1px solid gray;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        # max_width=800,
    )

    base_url = 'http://127.0.0.1:5000/links'
    layer = DynamicGeoJson(url=base_url,
                           style_field='fc',
                           style_map=create_style_mapping(),
                           name="HDMap",
                           show=False,
                           tooltip=tooltip,
                           )

    return layer


def create_style_mapping():
    def geo_color(fc):
        fc = int(fc)
        return ['red', 'orange', 'lightblue', 'green', 'darkgreen'][fc - 1]

    def geo_fill_color(fc):
        fc = int(fc)
        return 'red' if fc == 1 else "transparent"

    mapping = {}
    for i in range(1, 6):
        style = {
            'fillColor': geo_color(i),
            'color': geo_color(i),
            "fillOpacity": 0.4,
        }
        mapping[str(i)] = style

    return mapping


def create_map():
    import os
    app_dir = '../app'

    # init location
    location = (31.28664929, 121.60358643)
    zoom_start = 15

    # base map
    base_map = create_base_map(location=location, zoom_start=zoom_start)

    create_geo_layer().add_to(base_map)
    folium.LayerControl().add_to(base_map)  # NOTE: controller should be init after geo layers
    folium.plugins.MousePosition(position='bottomleft', empty_string='').add_to(base_map)

    base_map.save(os.path.join(app_dir, 'dynamic_geo.html'))


def main():
    create_map()


if __name__ == '__main__':
    main()
