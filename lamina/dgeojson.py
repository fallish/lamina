# encoding: utf-8
"""
@author: Michael
@file: ugeojson.py
@time: 2020/4/30 4:30 PM
@desc:
"""
import json
import os

from branca.element import Figure, JavascriptLink
from folium import Map
from folium.map import Layer, Tooltip
from folium.utilities import get_obj_in_upper_tree
from jinja2 import Template

from .config import js_dir
from .dgeojson_tooltip import DynamicGeoJsonTooltip


class DynamicGeoJson(Layer):
    _template = Template(u"""
        {% macro script(this, kwargs) %}

            {%- if this.style %}
            function {{ this.get_name() }}_style(feature) {
                if (!feature.properties) {
                    return {{ this.style_map['default'] }};
                }
                var field_name = '{{ this.style_field }}';
                var val = feature.properties[field_name];
                switch(val) {
                    {%- for field_val, style in this.style_map.items() if field_val != 'default' %}
                    case {{ field_val|tojson }}:
                        return {{ style }};
                    {%- endfor %}
                    default:
                        return {{ this.style_map['default'] }};
                    }
            }
            {%- endif %}
            
            function {{ this.get_name() }}_oneachfeature(feature, layer) {
                if ("setStyle" in layer) {
                    layer.on({
                        // mouseout: resetHighlight,
                        mouseover: function (e) {
                            e.target.setStyle({weight: 9, border: 1});
                            //e.target.openPopup(e.latlng);
                        }
                    });
                }
            }
            
            var {{ this.get_name() }} =  
            L.dGeoJSONLayer({
                {%- if this.use_bbox %}
                usebbox: true,
                {%- endif %}

                {%- if this.min_zoom %}
                minZoom: {{ this.min_zoom }},
                {%- endif %}

                enctype: "urlencoded",
                debug: true,
                
                {% if this.style %}
                style: {{ this.get_name() }}_style,
                {%- endif %}
                
                onEachFeature: {{ this.get_name() }}_oneachfeature, 

                endpoint: "{{ this.url }}"
            }
            ).addTo({{ this.parent_map.get_name() }});
            
        {% endmacro %}
    """)

    def __init__(self, url, use_bbox=True, min_zoom=None,
                 style_field=None, style_map=None,
                 name=None, overlay=True, control=True, show=True,
                 tooltip=None,
                 dgeojson_js=None
                 ):
        super(DynamicGeoJson, self).__init__(name=name, overlay=overlay,
                                             control=control, show=show)

        self._name = "DynamicGeoJson"

        self.url = url
        self.use_bbox = use_bbox
        self.min_zoom = min_zoom

        self.parent_map = None

        self.style = style_field is not None and style_map is not None
        self.style_field = style_field
        self.style_map = self._create_style_map(style_map)

        if isinstance(tooltip, (DynamicGeoJsonTooltip, Tooltip)):
            self.add_child(tooltip)
        elif tooltip is not None:
            self.add_child(Tooltip(tooltip))

        self.dgeojson_js = dgeojson_js

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)
        super(DynamicGeoJson, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # TODO: Add web link instead of link
        if self.dgeojson_js:
            figure.header.add_child(JavascriptLink(self.dgeojson_js))
        else:
            figure.header.add_child(JavascriptLink(os.path.join(js_dir, 'lamina/leaflet.dGeoJSON.js')))  # noqa

    def _create_style_map(self, styles):
        style_map = {}
        for field_val, style in styles.items():
            if isinstance(style, dict):
                style = self._to_key(style)
            style_map[field_val] = style

        default_key = next(iter(sorted(style_map.keys())))
        style_map['default'] = style_map[default_key]

        return style_map

    @staticmethod
    def _to_key(d):
        """Convert dict to str and enable Jinja2 template syntax."""
        as_str = json.dumps(d, sort_keys=True)
        return as_str.replace('"{{', '{{').replace('}}"', '}}')
