# encoding: utf-8
"""
@author: Michael
@file: ugeojson_demo.py
@time: 2020/4/30 5:17 PM
@desc:
"""
import folium

from lamina import DynamicGeoJsonTooltip, create_baidu_map, DynamicGeoJson
from lamina.provider import create_gaode_map, create_tianditu_map


def create_style_mapping():
    def geo_color(fc):
        fc = int(fc)
        # return ['gray', 'lightblue', 'pink', 'orange', 'purple'][fc - 1]
        return ['gray', 'lightblue', 'pink', 'orange', 'purple'][5-fc]

    def geo_fill_color(fc):
        fc = int(fc)
        return 'red' if fc == 1 else "transparent"
        # fc = int(fc)
        # return ['gray', 'lightblue', 'green', 'orange', 'darkgreen'][fc - 1]

    def get_weight(fc):
        fc = int(fc)
        return [8, 6, 4, 3, 2][fc - 1]

    mapping = {}
    for i in range(1, 6):
        style = {
            'fillColor': geo_fill_color(i),
            'color': geo_color(i),
            "fillOpacity": 0.4,
            'weight': get_weight(i)
        }
        mapping[i] = style

    return mapping


def main():
    location = (31.28664929, 121.60358643)
    zoom_start = 15

    tooltip = DynamicGeoJsonTooltip(
        fields=["fc", "rt", "rst", "name"],
        # aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
        aliases=["fc", "road type", "road sub type", "name"],
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

    # map = create_baidu_map(location=location, zoom_start=zoom_start)
    map = create_tianditu_map(location=location, zoom_start=zoom_start)
    ugeo_layer = DynamicGeoJson(url='http://127.0.0.1:5000/links',
                                use_bbox=True,
                                min_zoom=15,
                                name='HDMap',
                                style_field='fc',
                                style_map=create_style_mapping(),
                                tooltip=tooltip,
                                )
    ugeo_layer.add_to(map)

    folium.LayerControl().add_to(map)  # NOTE: controller should be init after geo layers
    folium.plugins.MousePosition(position='bottomleft', empty_string='').add_to(map)

    map.save('../app/dgeojson_demo.html')


if __name__ == '__main__':
    main()
