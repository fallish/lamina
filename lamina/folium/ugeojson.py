# encoding: utf-8
"""
@author: Michael
@file: ugeojson.py
@time: 2020/4/30 4:30 PM
@desc:
"""
from branca.element import MacroElement, Figure, JavascriptLink
from folium import Map
from folium.utilities import get_obj_in_upper_tree
from jinja2 import Template


class UpdatingGeoJson(MacroElement):
    _template = Template(u"""
        {% macro script(this, kwargs) %}
    
            L.uGeoJSONLayer({
                {%- if this.use_bbox %}
                usebbox: true,
                {%- endif %}
                
                {%- if this.min_zoom %}
                minZoom: {{ this.min_zoom }},
                {%- endif %}
                
                enctype: "urlencoded",
                debug: true,
                
                endpoint: "{{ this.url }}"
            }).addTo({{ this.parent_map.get_name() }});
        
        {% endmacro %}
    """)

    def __init__(self, url, use_bbox=True, min_zoom=None, ):
        super(UpdatingGeoJson, self).__init__()

        self._name = "UpdatingGeoJson"

        self.url = url
        self.use_bbox = use_bbox
        self.min_zoom = min_zoom

        self.parent_map = None

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)
        super(UpdatingGeoJson, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # TODO: Add web link instead of link
        figure.header.add_child(JavascriptLink('../static/js/leaflet/plugins/leaflet.uGeoJSON.js'))  # noqa

