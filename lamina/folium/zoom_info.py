# encoding: utf-8
"""
@author: Michael
@file: zoom_info.py
@time: 2020/4/23 3:28 PM
@desc:
"""
import os

from branca.element import Figure, JavascriptLink, CssLink
from folium import MacroElement, Map
from folium.utilities import get_obj_in_upper_tree
from jinja2 import Template

from ..config import js_dir, css_dir


class ZoomInfo(MacroElement):
    """Add a field that shows the coordinates of the mouse position.

    Uses the Leaflet plugin by Ardhi Lukianto under MIT license.
    https://github.com/ardhi/Leaflet.MousePosition

    Parameters
    ----------


    Examples
    --------

    """
    _template = Template("""
    """)

    def __init__(self, zoominfoControl=True, zoomControl=False):
        super(ZoomInfo, self).__init__()

        self._zoominfoControl = zoominfoControl
        self._zoomControl = zoomControl

        self.parent_map = None
        self._name = "ZoomInfo"

    def add_to(self, parent, name=None, index=None):
        assert isinstance(parent, Map)

        # Set Zoom Control and ZoomInfo Control
        options = {'zoomControl': self._zoomControl, 'zoominfoControl': self._zoominfoControl}
        parent.options.update(options)

        parent.add_child(self, name=self._name)

    def render(self, **kwargs):
        self.parent_map = get_obj_in_upper_tree(self, Map)
        assert self.parent_map.options.get('zoominfoControl') is True, "Map must set zoominfoControl to True"

        super(ZoomInfo, self).render()

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')

        # TODO: Add web link instead of link
        # figure.header.add_child(JavascriptLink('../static/js/leaflet/plugins/L.Control.Zoominfo.js'))  # noqa

        # figure.header.add_child(CssLink('../static/css/leaflet/plugins/L.Control.Zoominfo.css'))  # noqa

        figure.header.add_child(JavascriptLink(os.path.join(js_dir, 'folium/L.Control.Zoominfo.js')))  # noqa
        figure.header.add_child(CssLink(os.path.join(css_dir, 'folium/L.Control.Zoominfo.css')))  # noqa
