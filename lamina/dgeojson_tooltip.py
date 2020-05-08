# encoding: utf-8
"""
@author: Michael
@file: dgeojson_tooltip.py
@time: 2020/5/1 5:46 PM
@desc:
"""
import warnings

from folium import Tooltip
from jinja2 import Template


class DynamicGeoJsonTooltip(Tooltip):
    """
    Create a tooltip that uses data from either geojson or topojson.

    Parameters
    ----------
    fields: list or tuple.
        Labels of GeoJson/TopoJson 'properties' or GeoPandas GeoDataFrame
        columns you'd like to display.
    aliases: list/tuple of strings, same length/order as fields, default None.
        Optional aliases you'd like to display in the tooltip as field name
        instead of the keys of `fields`.
    labels: bool, default True.
        Set to False to disable displaying the field names or aliases.
    localize: bool, default False.
        This will use JavaScript's .toLocaleString() to format 'clean' values
        as strings for the user's location; i.e. 1,000,000.00 comma separators,
        float truncation, etc.
        Available for most of JavaScript's primitive types (any data you'll
        serve into the template).
    style: str, default None.
        HTML inline style properties like font and colors. Will be applied to
        a div with the text in it.
    sticky: bool, default True
        Whether the tooltip should follow the mouse.
    **kwargs: Assorted.
        These values will map directly to the Leaflet Options. More info
        available here: https://leafletjs.com/reference-1.5.1#tooltip

    Examples
    --------
    # Provide fields and aliases, with Style.
    >>> DynamicGeoJsonTooltip(
    >>>     fields=['CNTY_NM', 'census-pop-2015', 'census-md-income-2015'],
    >>>     aliases=['County', '2015 Census Population', '2015 Median Income'],
    >>>     localize=True,
    >>>     style=('background-color: grey; color: white; font-family:'
    >>>            'courier new; font-size: 24px; padding: 10px;')
    >>> )
    # Provide fields, with labels off and fixed tooltip positions.
    >>> DynamicGeoJsonTooltip(fields=('CNTY_NM',), labels=False, sticky=False)
    """
    _template = Template(u"""
        {% macro script(this, kwargs) %}
        {{ this._parent.get_name() }}.bindTooltip(
            function(layer){
            // Convert non-primitive to String.
            let handleObject = (feature)=> typeof(feature)=='object' ? JSON.stringify(feature) : feature;
            let fields = {{ this.fields|tojson }};
            {%- if this.aliases %}
            let aliases = {{ this.aliases|tojson }};
            {%- endif %}
            return '<table{% if this.style %} style={{ this.style|tojson }}{% endif%}>' +
            String(
                fields.map(
                columnname=> {
                    var val = layer.feature.properties[columnname];
                    val = val == undefined ? '' : val;
                    return `<tr style="text-align: left;">{% if this.labels %}
                    <th style="padding: 4px; padding-right: 10px;">{% if this.aliases %}
                        ${aliases[fields.indexOf(columnname)]
                        {% if this.localize %}.toLocaleString(){% endif %}}
                    {% else %}
                    ${ columnname{% if this.localize %}.toLocaleString(){% endif %}}
                    {% endif %}</th>
                    {% endif %}
                    <td style="padding: 4px;">${handleObject(val)
                    {% if this.localize %}.toLocaleString(){% endif %}}</td></tr>`; 
                    }
                ).join(''))
                +'</table>'
            }, {{ this.options|tojson }});
        {% endmacro %}
        """)

    def __init__(self, fields, aliases=None, labels=True,
                 localize=False, style=None, sticky=True, **kwargs):
        super(DynamicGeoJsonTooltip, self).__init__(
            text='', style=style, sticky=sticky, **kwargs
        )
        self._name = 'GeoJsonTooltip'

        assert isinstance(fields, (list, tuple)), 'Please pass a list or ' \
                                                  'tuple to fields.'
        if aliases is not None:
            assert isinstance(aliases, (list, tuple))
            assert len(fields) == len(aliases), 'fields and aliases must have' \
                                                ' the same length.'
        assert isinstance(labels, bool), 'labels requires a boolean value.'
        assert isinstance(localize, bool), 'localize must be bool.'
        assert 'permanent' not in kwargs, 'The `permanent` option does not ' \
                                          'work with GeoJsonTooltip.'

        self.fields = fields
        self.aliases = aliases
        self.labels = labels
        self.localize = localize
        if style:
            assert isinstance(style, str), \
                'Pass a valid inline HTML style property string to style.'
            # noqa outside of type checking.
            self.style = style

    def warn_for_geometry_collections(self):
        """Checks for GeoJson GeometryCollection features to warn user about incompatibility."""
        geom_collections = [
            feature.get('properties') if feature.get('properties') is not None else key
            for key, feature in enumerate(self._parent.data['features'])
            if feature['geometry']['type'] == 'GeometryCollection'
        ]
        if any(geom_collections):
            warnings.warn(
                "DynamicGeoJsonTooltip is not configured to render tooltips for GeoJson GeometryCollection geometries. "
                "Please consider reworking these features: {} to MultiPolygon for full functionality.\n"
                "https://tools.ietf.org/html/rfc7946#page-9".format(geom_collections), UserWarning)

    def render(self, **kwargs):
        """Renders the HTML representation of the element."""
        # if isinstance(self._parent, DynamicGeoJson):
        #     keys = tuple(self._parent.data['features'][0]['properties'].keys())
        #     self.warn_for_geometry_collections()
        # else:
        #     raise TypeError('You cannot add a GeoJsonTooltip to anything else '
        #                     'than a DynamicGeoJson  object.')
        # keys = tuple(x for x in keys if x not in ('style', 'highlight'))
        # for value in self.fields:
        #     assert value in keys, ('The field {} is not available in the data. '
        #                            'Choose from: {}.'.format(value, keys))

        super(DynamicGeoJsonTooltip, self).render(**kwargs)