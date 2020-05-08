# encoding: utf-8
"""
@author: Michael
@file: dsearch.py
@time: 2020/5/7 3:32 PM
@desc:
"""
from branca.element import MacroElement, Figure
from folium import Map
from folium.utilities import get_obj_in_upper_tree
from jinja2 import Template
from branca.element import Figure, JavascriptLink, CssLink


class DynamicSearch(MacroElement):
    """
    Adds a dynamic search tool to your map.



    """

    _template = Template("""
        {% macro script(this, kwargs) %}
        
            var {{this.get_name()}} = new L.Control.Search({
                    url: '{{ this.url }}',
                    propertyName: 'display_name',
                    jsonpParam: 'json_callback',
                    propertyLoc: ['lat', 'lon'],
                    autoCollapse: true,
                    autoType: false,
                    minLength: 2,
                    position: '{{ this.position }}',
                    moveToLocation: function(latlng, title, map) {
                        var zoom =  {{ this.search_zoom }};
                        map.flyTo(latlng, zoom); // access the zoom
                    }
                });
            {{this.parent_map.get_name()}}.addControl({{ this.get_name() }});
            
        {% endmacro %}
        """)  # noqa

    def __init__(self, url, position='topleft', placeholder='Search', collapsed=False, search_zoom=15,
                 **kwargs):
        super(DynamicSearch, self).__init__()

        self._name = 'DynamicSearch'
        self.url = url
        self.position = position
        self.placeholder = placeholder
        self.collapsed = collapsed
        self.search_zoom = search_zoom

        self.parent_map = None

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)

        super(DynamicSearch, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        figure.header.add_child(
            JavascriptLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.9.7/dist/leaflet-search.min.js'),  # noqa
            name='Leaflet.Search.js'
        )

        figure.header.add_child(
            CssLink('https://cdn.jsdelivr.net/npm/leaflet-search@2.9.7/dist/leaflet-search.min.css'),  # noqa
            name='Leaflet.Search.css'
        )
