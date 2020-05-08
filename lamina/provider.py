# # encoding: utf-8
# """
# @author: Michael
# @file: provider.py
# @time: 2020/4/15 10:51 AM
# @desc:
#
# Adapt leaflet plugin https://github.com/htoooth/Leaflet.ChineseTmsProviders to python
#
#
# """
# import itertools
# from enum import IntFlag, Enum, IntEnum, _decompose, auto
# from functools import lru_cache
# from typing import Any, List
#
# import folium
# import folium.plugins
# from branca.element import JavascriptLink, Figure, Html, Element, MacroElement
# from folium import TileLayer, FeatureGroup, GeoJson, GeoJsonTooltip, Map
# from folium.utilities import get_obj_in_upper_tree
#
# from py_leaflet.mesh_viewer.tms_provider.dgeojson import DynamicGeoJson
#
#
# # from py_leaflet.mesh_viewer.tms_provider.dynamic_geojson import MapDraggingAction
#
#
# class Provider(IntEnum):
#     TianDiTu = 0
#     GaoDe = 1
#     Google = 2
#     Geoq = 3
#     Osm = 4
#     Baidu = 5
#
#
# class MapType(IntFlag):
#     NormalMap = auto()
#     NormalAnnotation = auto()
#
#     SatelliteMap = auto()
#     SatelliteAnnotation = auto()
#
#     TerrainMap = auto()
#     TerrainAnnotation = auto()
#
#     NormalPurplishBlue = auto()
#     NormalGray = auto()
#     NormalWarm = auto()
#
#     ThemeHydro = auto()
#
#
# class LayerType(object):
#
#     def __init__(self, provider_type, map_type):
#         self._provider_type = provider_type
#         self._map_type = map_type
#
#     @classmethod
#     @lru_cache()
#     def create(cls, provider_type, map_type):
#         return cls(provider_type, map_type)
#
#     @property
#     def provider_type(self):
#         return self._provider_type
#
#     @property
#     def map_type(self):
#         return self._map_type
#
#     def __eq__(self, other):
#         if not isinstance(other, LayerType):
#             return False
#         return self.provider_type == other.provider_type and self.map_type == other.map_type
#
#     def __or__(self, other):
#         map_type = self.map_type | other.map_type
#         return LayerType(self.provider_type, map_type)
#
#     def __contains__(self, other):
#         if not isinstance(other, self.__class__):
#             return False
#
#         return self.provider_type == other.provider_type and self.map_type & other.map_type
#
#     def __iter__(self):
#         values = _decompose(self.map_type.__class__, self.map_type)[0]
#         for val in values:
#             yield LayerType.create(self.provider_type, val)
#
#     def __str__(self):
#         return f'{self.provider_type.name} {self.map_type.name}'
#
#
# class TmsLayerProvider(object):
#     _SUBDOMAINS = []
#
#     _LayerTypes = []
#
#     def __init__(self):
#         self._options = {}
#
#     # def layer(self, layer_type: Any, name=None):
#     #     raise NotImplementedError
#
#     def layer(self, layer_type: LayerType, name=None):
#         name = name if name is not None else self._default_group_name(layer_type)
#         values = list(layer_type)
#         if len(values) == 1:
#             return self._layer_simple(values[0], name)
#         else:
#             fg = FeatureGroup(name=name, overlay=False)
#             [fg.add_chil(self._layer_simple(layer_type)) for layer_type in values]
#             return fg
#
#     def layers(self, layer_types: List[LayerType] = None):
#         layer_types = layer_types if layer_types is not None else self._LayerTypes
#         return [self.layer(layer_type) for layer_type in layer_types]
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         raise NotImplementedError
#
#     def _create_layer(self, tiles, name):
#         return TileLayer(tiles=tiles, name=name, **self._options)
#
#     def _default_layer_name(self, method):
#         name = method.__name__
#         name = ''.join(map(str.capitalize, name.split('_')))
#         return f'{self.__class__.__name__} {name}'
#
#     def _default_group_name(self, layer_type: LayerType):
#         return f'{self.__class__.__name__} {layer_type.map_type.name}'
#
#
# class TianDiTu(TmsLayerProvider):
#     _KEY = "174705aebfe31b79b3587279e211cb9a"
#     _SUBDOMAINS = ['0', '1', '2', '3', '4', '5', '6', '7']
#
#     NormalMap = LayerType(Provider.TianDiTu, MapType.NormalMap)
#     NormalAnnotation = LayerType(Provider.TianDiTu, MapType.NormalAnnotation)
#
#     SatelliteMap = LayerType(Provider.TianDiTu, MapType.SatelliteMap)
#     SatelliteAnnotation = LayerType(Provider.TianDiTu, MapType.SatelliteAnnotation)
#
#     TerrainMap = LayerType(Provider.TianDiTu, MapType.TerrainMap)
#     TerrainAnnotation = LayerType(Provider.TianDiTu, MapType.TerrainAnnotation)
#
#     Normal = NormalMap | NormalAnnotation
#     Satellite = SatelliteMap | SatelliteAnnotation
#     Terrain = TerrainMap | TerrainAnnotation
#
#     _LayerTypes = [
#         NormalMap,
#         NormalAnnotation,
#         SatelliteMap,
#         SatelliteAnnotation,
#         TerrainMap,
#         TerrainAnnotation,
#     ]
#
#     def __init__(self, key=None):
#         super(TianDiTu, self).__init__()
#
#         # Map provider specific options
#         key = key if key is not None else self._KEY
#         subdomains = self._SUBDOMAINS
#
#         self._options = {
#             'key': key,
#             'subdomains': subdomains,
#             'attr': 'TianDiTu'
#         }
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         if layer_type not in self._LayerTypes:
#             raise ValueError(f'Unsupported layer {layer_type}')
#         assert layer_type.provider_type == Provider.TianDiTu
#
#         if layer_type == self.NormalMap:
#             return self.normal_map(name)
#         elif layer_type == self.NormalAnnotation:
#             return self.normal_annotation(name)
#         elif layer_type == self.SatelliteMap:
#             return self.satellite_map(name)
#         elif layer_type == self.SatelliteAnnotation:
#             return self.satellite_annotation(name)
#         elif layer_type == self.TerrainMap:
#             return self.terrain_map(name)
#         elif layer_type == self.TerrainAnnotation:
#             return self.terrain_annotation(name)
#
#     def normal_map(self, name=None) -> TileLayer:
#         tiles = "http://t{s}.tianditu.com/DataServer?T=vec_w&X={x}&Y={y}&L={z}&tk={key}"
#         name = name if name is not None else self._default_layer_name(self.normal_map)
#         # name = name if name is not None else TianDiTu.LayerType.NormalMap.name
#         return self._create_layer(tiles=tiles, name=name)
#
#     def normal_annotation(self, name=None) -> TileLayer:
#         tiles = "http://t{s}.tianditu.com/DataServer?T=cva_w&X={x}&Y={y}&L={z}&tk={key}"
#         name = name if name is not None else self._default_layer_name(self.normal_annotation)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_map(self, name=None) -> TileLayer:
#         tiles = "http://t{s}.tianditu.com/DataServer?T=img_w&X={x}&Y={y}&L={z}&tk={key}"
#         name = name if name is not None else self._default_layer_name(self.satellite_map)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_annotation(self, name=None) -> TileLayer:
#         tiles = "//t{s}.tianditu.com/DataServer?T=cia_w&X={x}&Y={y}&L={z}&tk={key}"
#         name = name if name is not None else self._default_layer_name(self.satellite_annotation)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def terrain_map(self, name=None) -> TileLayer:
#         tiles = "http://t{s}.tianditu.com/DataServer?T=ter_w&X={x}&Y={y}&L={z}&tk={key}"
#         name = name if name is not None else self._default_layer_name(self.terrain_map)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def terrain_annotation(self, name=None) -> TileLayer:
#         tiles = "//t{s}.tianditu.com/DataServer?T=cta_w&X={x}&Y={y}&L={z}&tk={key}"
#         name = name if name is not None else self._default_layer_name(self.terrain_annotation)
#         return self._create_layer(tiles=tiles, name=name)
#
#
# class GaoDe(TmsLayerProvider):
#     _SUBDOMAINS = ["1", "2", "3", "4"]
#
#     NormalMap = LayerType(Provider.GaoDe, MapType.NormalMap)
#
#     SatelliteMap = LayerType(Provider.GaoDe, MapType.SatelliteMap)
#     SatelliteAnnotation = LayerType(Provider.GaoDe, MapType.SatelliteAnnotation)
#
#     Normal = NormalMap
#     Satellite = SatelliteMap | SatelliteAnnotation
#
#     _LayerTypes = [
#         NormalMap,
#         SatelliteMap,
#         SatelliteAnnotation
#     ]
#
#     def __init__(self):
#         super(GaoDe, self).__init__()
#
#         # Map provider specific options
#         subdomains = self._SUBDOMAINS
#
#         self._options = {
#             'subdomains': subdomains,
#             'attr': 'AutoNavi'
#         }
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         if layer_type not in self._LayerTypes:
#             raise ValueError(f'Unsupported layer {layer_type}')
#         assert layer_type.provider_type == Provider.GaoDe
#
#         if layer_type == self.NormalMap:
#             return self.normal_map(name)
#         elif layer_type == self.SatelliteMap:
#             return self.satellite_map(name)
#         elif layer_type == self.SatelliteAnnotation:
#             return self.satellite_annotation(name)
#
#     def normal_map(self, name=None):
#         tiles = "//webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}"
#         name = name if name is not None else self._default_layer_name(self.normal_map)
#         # name = name if name is not None else GaoDe.LayerType.NormalMap.name
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_map(self, name=None):
#         tiles = "//webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}"
#         name = name if name is not None else self._default_layer_name(self.satellite_map)
#         # name = name if name is not None else GaoDe.LayerType.SatelliteMap.name
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_annotation(self, name=None):
#         tiles = "//webst0{s}.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}"
#         name = name if name is not None else self._default_layer_name(self.satellite_annotation)
#         # name = name if name is not None else GaoDe.LayerType.SatelliteAnnotation.name
#         return self._create_layer(tiles=tiles, name=name)
#
#
# class Google(TmsLayerProvider):
#     NormalMap = LayerType(Provider.Google, MapType.NormalMap)
#
#     SatelliteMap = LayerType(Provider.Google, MapType.SatelliteMap)
#     SatelliteAnnotation = LayerType(Provider.Google, MapType.SatelliteAnnotation)
#
#     Normal = NormalMap
#     Satellite = SatelliteMap | SatelliteAnnotation
#
#     _LayerTypes = [
#         NormalMap,
#         SatelliteMap,
#         SatelliteAnnotation,
#     ]
#
#     def __init__(self):
#         super(Google, self).__init__()
#
#         # Map provider specific options
#         subdomains = self._SUBDOMAINS
#
#         self._options = {
#             'subdomains': subdomains,
#             'attr': 'Google Map'
#         }
#
#         # Terrain = TerrainMap | TerrainAnnotation
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         if layer_type not in self._LayerTypes:
#             raise ValueError(f'Unsupported layer {layer_type}')
#         assert layer_type.provider_type == Provider.Google
#
#         if layer_type == self.NormalMap:
#             return self.normal_map(name)
#         elif layer_type == self.SatelliteMap:
#             return self.satellite_map(name)
#         elif layer_type == self.SatelliteAnnotation:
#             return self.satellite_annotation(name)
#
#     def normal_map(self, name=None):
#         tiles = "//www.google.cn/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}"
#         name = name if name is not None else self._default_layer_name(self.normal_map)
#         # name = name if name is not None else GaoDe.LayerType.NormalMap.name
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_map(self, name=None):
#         tiles = "//www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"
#         name = name if name is not None else self._default_layer_name(self.satellite_map)
#         # name = name if name is not None else GaoDe.LayerType.NormalMap.name
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_annotation(self, name=None):
#         tiles = "//www.google.cn/maps/vt?lyrs=y@189&gl=cn&x={x}&y={y}&z={z}"
#         name = name if name is not None else self._default_layer_name(self.satellite_annotation)
#         # name = name if name is not None else GaoDe.LayerType.NormalMap.name
#         return self._create_layer(tiles=tiles, name=name)
#
#
# class Geoq(TmsLayerProvider):
#     NormalMap = LayerType(Provider.Geoq, MapType.NormalMap)
#     NormalPurplishBlue = LayerType(Provider.Geoq, MapType.NormalPurplishBlue)
#     NormalGray = LayerType(Provider.Geoq, MapType.NormalGray)
#     NormalWarm = LayerType(Provider.Geoq, MapType.NormalWarm)
#     ThemeHydro = LayerType(Provider.Geoq, MapType.ThemeHydro)
#
#     Normal = NormalMap
#
#     _LayerTypes = [
#         NormalMap,
#         NormalPurplishBlue,
#         NormalGray,
#         NormalWarm,
#
#         ThemeHydro,
#     ]
#
#     def __init__(self):
#         super(Geoq, self).__init__()
#
#         # Map provider specific options
#         subdomains = self._SUBDOMAINS
#
#         self._options = {
#             'subdomains': subdomains,
#             'attr': 'Geoq Map'
#         }
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         if layer_type not in self._LayerTypes:
#             raise ValueError(f'Unsupported layer {layer_type}')
#         assert layer_type.provider_type == Provider.Geoq
#
#         if layer_type == self.NormalMap:
#             return self.normal_map(name)
#         elif layer_type == self.NormalPurplishBlue:
#             return self.normal_purplish_blue(name)
#         elif layer_type == self.NormalWarm:
#             return self.normal_warm(name)
#         elif layer_type == self.NormalGray:
#             return self.normal_gray(name)
#         elif layer_type == self.ThemeHydro:
#             return self.theme_hydro(name)
#
#     def normal_map(self, name=None):
#         tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}"
#         name = name if name is not None else self._default_layer_name(self.normal_map)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def normal_purplish_blue(self, name=None):
#         tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}"
#         name = name if name is not None else self._default_layer_name(self.normal_purplish_blue)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def normal_gray(self, name=None):
#         tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}"
#         name = name if name is not None else self._default_layer_name(self.normal_gray)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def normal_warm(self, name=None):
#         tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetWarm/MapServer/tile/{z}/{y}/{x}"
#         name = name if name is not None else self._default_layer_name(self.normal_warm)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def theme_hydro(self, name=None):
#         tiles = "//thematic.geoq.cn/arcgis/rest/services/ThematicMaps/WorldHydroMap/MapServer/tile/{z}/{y}/{x}"
#         name = name if name is not None else self._default_layer_name(self.theme_hydro)
#         return self._create_layer(tiles=tiles, name=name)
#
#
# class Osm(TmsLayerProvider):
#     _SUBDOMAINS = ['a', 'b', 'c']
#
#     NormalMap = LayerType(Provider.Osm, MapType.NormalMap)
#
#     Normal = NormalMap
#
#     def __init__(self):
#         super(Osm, self).__init__()
#
#         # Map provider specific options
#         subdomains = self._SUBDOMAINS
#
#         self._options = {
#             'subdomains': subdomains,
#             'attr': 'OpenStreetMap'
#         }
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         if layer_type not in self._LayerTypes:
#             raise ValueError(f'Unsupported layer {layer_type}')
#         assert layer_type.provider_type == Provider.Osm
#
#         if layer_type == self.NormalMap:
#             return self.normal_map(name)
#
#     def normal_map(self, name):
#         tiles = "//{s}.tile.osm.org/{z}/{x}/{y}.png"
#         name = name if name is not None else self._default_layer_name(self.normal_map)
#         return self._create_layer(tiles=tiles, name=name)
#
#
# class Baidu(TmsLayerProvider):
#     _SUBDOMAINS = '0123456789'
#
#     NormalMap = LayerType(Provider.Baidu, MapType.NormalMap)
#
#     SatelliteMap = LayerType(Provider.Baidu, MapType.SatelliteMap)
#     SatelliteAnnotation = LayerType(Provider.Baidu, MapType.SatelliteAnnotation)
#
#     Normal = NormalMap
#     Satellite = SatelliteMap | SatelliteAnnotation
#
#     _LayerTypes = [
#         NormalMap,
#         SatelliteMap,
#         SatelliteAnnotation,
#     ]
#
#     def __init__(self):
#         super(Baidu, self).__init__()
#
#         # Map provider specific options
#         subdomains = self._SUBDOMAINS
#
#         self._options = {
#             'subdomains': subdomains,
#             'attr': 'Baidu',
#             'tms': True
#         }
#
#     def _layer_simple(self, layer_type: LayerType, name=None):
#         if layer_type not in self._LayerTypes:
#             raise ValueError(f'Unsupported layer {layer_type}')
#
#         if layer_type == self.NormalMap:
#             return self.normal_map(name)
#         elif layer_type == self.SatelliteMap:
#             return self.satellite_map(name)
#         elif layer_type == self.SatelliteAnnotation:
#             return self.satellite_annotation(name)
#
#     def normal_map(self, name=None):
#         tiles = "//online{s}.map.bdimg.com/onlinelabel/?qt=tile&x={x}&y={y}&z={z}&styles=pl&scaler=1&p=1"
#         name = name if name is not None else self._default_layer_name(self.normal_map)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_map(self, name=None):
#         tiles = "//shangetu{s}.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46"
#         name = name if name is not None else self._default_layer_name(self.satellite_map)
#         return self._create_layer(tiles=tiles, name=name)
#
#     def satellite_annotation(self, name=None):
#         tiles = "//online{s}.map.bdimg.com/tile/?qt=tile&x={x}&y={y}&z={z}&styles=sl&v=020"
#         name = name if name is not None else self._default_layer_name(self.satellite_annotation)
#         return self._create_layer(tiles=tiles, name=name)
#
#     class BaiduTileLayer(TileLayer):
#         def __init__(self, tiles, name, **kwargs):
#             super(Baidu.BaiduTileLayer, self).__init__(tiles=tiles, name=name, **kwargs)
#
#         def render(self, **kwargs):
#             # check crs
#             app_map = self._get_app_map()
#             if app_map.crs != 'Baidu':
#                 raise ValueError(f"folium.Map's crs '{app_map.crs}' conflicts with Baidu Map's crs 'Baidu',"
#                                  f" please consider set folium.Map's crs to 'Baidu' or remove Baidu Map ")
#
#             # render BaiduTileLayer
#             super(Baidu.BaiduTileLayer, self).render(**kwargs)
#
#             # add links
#             figure = self.get_root()
#             assert isinstance(figure, Figure), ('You cannot render this Element '
#                                                 'if it is not in a Figure.')
#
#             figure.header.add_child(JavascriptLink("https://cdn.bootcss.com/proj4js/2.4.3/proj4.js"), name='proj4.js')
#             figure.header.add_child(JavascriptLink("https://cdn.bootcss.com/proj4leaflet/1.0.1/proj4leaflet.min.js"),
#                                     name='proj4leaflet.min.js'
#                                     )
#
#             pro_crs = """
#             <script>
#                if (L.Proj) {
#                 L.CRS.Baidu = new L.Proj.CRS('EPSG:900913', '+proj=merc +a=6378206 +b=6356584.314245179 +lat_ts=0.0 +lon_0=0.0 +x_0=0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs', {
#                     resolutions: function () {
#                         level = 19
#                         var res = [];
#                         res[0] = Math.pow(2, 18);
#                         for (var i = 1; i < level; i++) {
#                             res[i] = Math.pow(2, (18 - i))
#                         }
#                         return res;
#                     }(),
#                     origin: [0, 0],
#                     bounds: L.bounds([20037508.342789244, 0], [0, 20037508.342789244])
#                 });
#             }
#             </script>
#             """
#             figure.html.add_child(Element(pro_crs), name='L.CRS.Baidu')
#
#         def _get_app_map(self):
#             # parent = self._parent
#             # while parent:
#             #     if isinstance(parent, folium.Map):
#             #         return parent
#             #
#             #     # traverse to root, but Map not found
#             #     if parent == parent._parent:
#             #         break
#             #
#             #     parent = parent._parent
#             return get_obj_in_upper_tree(self, Map)
#
#     def _create_layer(self, tiles, name):
#         return Baidu.BaiduTileLayer(tiles=tiles, name=name, **self._options)
#
#
# @lru_cache()
# def create_provider(provider_type: Provider):
#     if provider_type == Provider.TianDiTu:
#         return TianDiTu()
#     elif provider_type == Provider.GaoDe:
#         return GaoDe()
#     elif provider_type == Provider.Google:
#         return Google()
#     elif provider_type == Provider.Geoq:
#         return Geoq()
#     elif provider_type == Provider.Osm:
#         return Osm()
#     elif provider_type == Provider.Baidu:
#         return Baidu()
#     else:
#         raise ValueError(f'Unsupported provider type {provider_type}')
#
#
# def create_layer(layer_type: LayerType):
#     provider_type = layer_type.provider_type
#     return create_provider(provider_type).layer(layer_type)
#
#
# def create_layers(layer_types: List[LayerType]):
#     return (create_layer(layer_type=layer_type) for layer_type in layer_types)
#
#
# # ----------------------------------------------------------------
#
#
# def create_base_map(location=None,
#                     zoom_start=10):
#     # Base map
#     base_map = folium.Map(
#         # location=(31.0, 121.0),
#         location=location,
#         zoom_start=zoom_start,
#         tiles=None,
#     )
#
#     # Add layers to app map
#     providers = [TianDiTu(), GaoDe(), Google(), Geoq(), Osm()]
#     for layer in itertools.chain(p.layers() for p in providers):
#         layer.add_to(base_map)
#
#     return base_map
#
#
# def create_baidu_map(location=None,
#                      zoom_start=10):
#     baidu_map = folium.Map(
#         location=location,
#         zoom_start=zoom_start,
#         tiles=None,
#         crs='Baidu',
#     )
#
#     for layer in Baidu().layers():
#         layer.add_to(baidu_map)
#
#     return baidu_map
#
#
# def create_map_apps():
#     import os
#     app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app'))
#
#     # init location
#     location = (31.28664929, 121.60358643)
#     zoom_start = 15
#
#     # base map
#     base_map = create_base_map(location=location, zoom_start=zoom_start)
#
#     create_geo_json_layer().add_to(base_map)
#     folium.LayerControl().add_to(base_map)
#     folium.plugins.MousePosition(position='bottomleft', empty_string='').add_to(base_map)
#
#     base_map.save(os.path.join(app_dir, 'base_map_app.html'))
#
#     # baidu map
#     baidu_map = create_baidu_map(location=location, zoom_start=zoom_start)
#
#     create_geo_json_layer().add_to(baidu_map)
#     folium.LayerControl().add_to(baidu_map)
#     folium.plugins.MousePosition(position='bottomleft', empty_string='').add_to(baidu_map)
#
#     baidu_map.save(os.path.join(app_dir, 'baidu_map_app.html'))
#
#     return {
#         'Base': base_map,
#         'Baidu': baidu_map,
#     }
#
#
# def create_geo_json_layer():
#     def geo_color(fc):
#         return ['red', 'orange', 'lightblue', 'green', 'darkgreen'][fc - 1]
#
#     def geo_fill_color(fc):
#         return 'red' if fc == 1 else "transparent"
#
#     tooltip = GeoJsonTooltip(
#         fields=["fc", "rt", "rst", "nr", "isbridge"],
#         # aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
#         aliases=["fc", "rt", "rst", "nr", "isbridge"],
#         localize=True,
#         sticky=False,
#         labels=True,
#         style="""
#             background-color: #F0EFEF;
#             border: 1px solid gray;
#             border-radius: 3px;
#             box-shadow: 3px;
#         """,
#         # max_width=800,
#     )
#
#     base_url = 'http://127.0.0.1:5000/links?box={xmin},{ymin},{xmax},{ymax}'
#     # layer = DynamicGeoJson(base_url='http://127.0.0.1:5000/links',
#     layer = DynamicGeoJson(base_url=base_url,
#                            # queries={'box': '121.59930775,31.28129225,121.62129250,31.29743295'},
#                            init_bounds=[121.59930775, 31.28129225, 121.62129250, 31.29743295],
#                            style_function=lambda x: {
#                                "fillColor": geo_fill_color(x["properties"]["fc"]),
#                                "color": geo_color(x["properties"]["fc"]),
#                                "fillOpacity": 0.4,
#                            },
#                            name="HDMap",
#                            show=False,
#                            tooltip=tooltip,
#                            )
#
#     return layer
#
#
# def main():
#     pa  # encoding: utf-8


"""
@author: Michael
@file: provider.py
@time: 2020/4/15 10:51 AM
@desc:

Adapt leaflet plugin https://github.com/htoooth/Leaflet.ChineseTmsProviders to python


"""
import itertools
from enum import IntFlag, Enum, IntEnum, _decompose, auto
from functools import lru_cache
from operator import itemgetter
from typing import Any, List

import folium
import folium.plugins
from branca.element import JavascriptLink, Figure, Html, Element, MacroElement
from folium import TileLayer, FeatureGroup, GeoJson, GeoJsonTooltip, Map
from folium.utilities import get_obj_in_upper_tree


class Provider(IntEnum):
    TianDiTu = 0
    GaoDe = 1
    Google = 2
    Geoq = 3
    Osm = 4
    Baidu = 5


class MapType(IntFlag):
    NormalMap = auto()
    NormalAnnotation = auto()

    SatelliteMap = auto()
    SatelliteAnnotation = auto()

    TerrainMap = auto()
    TerrainAnnotation = auto()

    NormalPurplishBlue = auto()
    NormalGray = auto()
    NormalWarm = auto()

    ThemeHydro = auto()

    # def __str__(self):
    #     cls = self.__class__
    #     members, uncovered = _decompose(cls, self._value_)
    #     if len(members) == 1 and members[0]._name_ is None:
    #         return '%s.%r' % (cls.__name__, members[0]._value_)
    #     else:
    #         return '%s.%s' % (
    #             cls.__name__,
    #             '|'.join([str(m._name_ or m._value_) for m in members]),
    #         )


class LayerType(object):

    def __init__(self, provider_type: Provider, map_type: MapType):
        self._provider_type = provider_type
        self._map_type = map_type

    @classmethod
    @lru_cache()
    def create(cls, provider_type, map_type):
        return cls(provider_type, map_type)

    @property
    def provider_type(self):
        return self._provider_type

    @property
    def map_type(self):
        return self._map_type

    def __eq__(self, other):
        if not isinstance(other, LayerType):
            return False
        return self.provider_type == other.provider_type and self.map_type == other.map_type

    def __or__(self, other):
        # map_type = self.map_type | other.map_type
        return LayerType(self.provider_type, self.map_type | other.map_type)

    def __contains__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.provider_type == other.provider_type and self.map_type & other.map_type

    def __iter__(self):
        members, not_covered = _decompose(self.map_type.__class__, self.map_type)
        members.sort(key=lambda x: x._value_)
        for val in members:
            yield LayerType.create(self.provider_type, val)

    # def __repr__(self):
    #     cls = self.map_type.__class__
    #     members, uncovered = _decompose(cls, self.map_type.value)
    #     map_types = '%s' % '|'.join([str(m._name_ or m._value_) for m in members])
    #
    #     return f'{self.provider_type.name} {map_types}'

    def __str__(self):
        cls = self.map_type.__class__
        members, uncovered = _decompose(cls, self.map_type.value)
        members.sort(key=lambda m: m._value_)
        map_types = '%s' % '|'.join([str(m._name_ or m._value_) for m in members])

        return f'{self.provider_type.name} {map_types}'


class TmsLayerProvider(object):
    _SUBDOMAINS = []

    _LayerTypes = []

    def __init__(self):
        self._options = {}

    # def layer(self, layer_type: Any, name=None):
    #     raise NotImplementedError

    def layer(self, layer_type: LayerType, name=None):
        name = name if name is not None else self._default_group_name(layer_type)
        values = list(layer_type)

        if len(values) == 1:
            return self._layer_simple(values[0], name)
        else:
            fg = FeatureGroup(name=name, overlay=False)
            [fg.add_child(self._layer_simple(layer_type)) for layer_type in values]
            # for layer_type in values:
            #     fg.add_child(self._layer_simple(layer_type))
            return fg

    def layers(self, layer_types: List[LayerType] = None):
        layer_types = layer_types if layer_types is not None else self._LayerTypes
        return [self.layer(layer_type) for layer_type in layer_types]

    def _layer_simple(self, layer_type: LayerType, name=None):
        raise NotImplementedError

    def _create_layer(self, tiles, name):
        return TileLayer(tiles=tiles, name=name, **self._options)

    def _default_layer_name(self, method):
        name = method.__name__
        name = ''.join(map(str.capitalize, name.split('_')))
        return f'{self.__class__.__name__} {name}'

    def _default_group_name(self, layer_type: LayerType):
        # return f'{self.__class__.__name__} {layer_type}'
        return f'{layer_type}'


class TianDiTu(TmsLayerProvider):
    _KEY = "174705aebfe31b79b3587279e211cb9a"
    _SUBDOMAINS = ['0', '1', '2', '3', '4', '5', '6', '7']

    NormalMap = LayerType(Provider.TianDiTu, MapType.NormalMap)
    NormalAnnotation = LayerType(Provider.TianDiTu, MapType.NormalAnnotation)

    SatelliteMap = LayerType(Provider.TianDiTu, MapType.SatelliteMap)
    SatelliteAnnotation = LayerType(Provider.TianDiTu, MapType.SatelliteAnnotation)

    TerrainMap = LayerType(Provider.TianDiTu, MapType.TerrainMap)
    TerrainAnnotation = LayerType(Provider.TianDiTu, MapType.TerrainAnnotation)

    Normal = NormalMap | NormalAnnotation
    Satellite = SatelliteMap | SatelliteAnnotation
    Terrain = TerrainMap | TerrainAnnotation

    _LayerTypes = [
        NormalMap,
        NormalAnnotation,
        SatelliteMap,
        SatelliteAnnotation,
        TerrainMap,
        TerrainAnnotation,
    ]

    def __init__(self, key=None):
        super(TianDiTu, self).__init__()

        # Map provider specific options
        key = key if key is not None else self._KEY
        subdomains = self._SUBDOMAINS

        self._options = {
            'key': key,
            'subdomains': subdomains,
            'attr': 'TianDiTu'
        }

    def _layer_simple(self, layer_type: LayerType, name=None):
        if layer_type not in self._LayerTypes:
            raise ValueError(f'Unsupported layer {layer_type}')
        assert layer_type.provider_type == Provider.TianDiTu

        if layer_type == self.NormalMap:
            return self.normal_map(name)
        elif layer_type == self.NormalAnnotation:
            return self.normal_annotation(name)
        elif layer_type == self.SatelliteMap:
            return self.satellite_map(name)
        elif layer_type == self.SatelliteAnnotation:
            return self.satellite_annotation(name)
        elif layer_type == self.TerrainMap:
            return self.terrain_map(name)
        elif layer_type == self.TerrainAnnotation:
            return self.terrain_annotation(name)

    def normal_map(self, name=None) -> TileLayer:
        tiles = "http://t{s}.tianditu.com/DataServer?T=vec_w&X={x}&Y={y}&L={z}&tk={key}"
        name = name if name is not None else self._default_layer_name(self.normal_map)
        # name = name if name is not None else TianDiTu.LayerType.NormalMap.name
        return self._create_layer(tiles=tiles, name=name)

    def normal_annotation(self, name=None) -> TileLayer:
        tiles = "http://t{s}.tianditu.com/DataServer?T=cva_w&X={x}&Y={y}&L={z}&tk={key}"
        name = name if name is not None else self._default_layer_name(self.normal_annotation)
        return self._create_layer(tiles=tiles, name=name)

    def satellite_map(self, name=None) -> TileLayer:
        tiles = "http://t{s}.tianditu.com/DataServer?T=img_w&X={x}&Y={y}&L={z}&tk={key}"
        name = name if name is not None else self._default_layer_name(self.satellite_map)
        return self._create_layer(tiles=tiles, name=name)

    def satellite_annotation(self, name=None) -> TileLayer:
        tiles = "//t{s}.tianditu.com/DataServer?T=cia_w&X={x}&Y={y}&L={z}&tk={key}"
        name = name if name is not None else self._default_layer_name(self.satellite_annotation)
        return self._create_layer(tiles=tiles, name=name)

    def terrain_map(self, name=None) -> TileLayer:
        tiles = "http://t{s}.tianditu.com/DataServer?T=ter_w&X={x}&Y={y}&L={z}&tk={key}"
        name = name if name is not None else self._default_layer_name(self.terrain_map)
        return self._create_layer(tiles=tiles, name=name)

    def terrain_annotation(self, name=None) -> TileLayer:
        tiles = "//t{s}.tianditu.com/DataServer?T=cta_w&X={x}&Y={y}&L={z}&tk={key}"
        name = name if name is not None else self._default_layer_name(self.terrain_annotation)
        return self._create_layer(tiles=tiles, name=name)


class GaoDe(TmsLayerProvider):
    _SUBDOMAINS = ["1", "2", "3", "4"]

    NormalMap = LayerType(Provider.GaoDe, MapType.NormalMap)

    SatelliteMap = LayerType(Provider.GaoDe, MapType.SatelliteMap)
    SatelliteAnnotation = LayerType(Provider.GaoDe, MapType.SatelliteAnnotation)

    Normal = NormalMap
    Satellite = SatelliteMap | SatelliteAnnotation

    _LayerTypes = [
        NormalMap,
        SatelliteMap,
        SatelliteAnnotation
    ]

    def __init__(self):
        super(GaoDe, self).__init__()

        # Map provider specific options
        subdomains = self._SUBDOMAINS

        self._options = {
            'subdomains': subdomains,
            'attr': 'AutoNavi'
        }

    def _layer_simple(self, layer_type: LayerType, name=None):
        if layer_type not in self._LayerTypes:
            raise ValueError(f'Unsupported layer {layer_type}')
        assert layer_type.provider_type == Provider.GaoDe

        if layer_type == self.NormalMap:
            return self.normal_map(name)
        elif layer_type == self.SatelliteMap:
            return self.satellite_map(name)
        elif layer_type == self.SatelliteAnnotation:
            return self.satellite_annotation(name)

    def normal_map(self, name=None):
        tiles = "//webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}"
        name = name if name is not None else self._default_layer_name(self.normal_map)
        # name = name if name is not None else GaoDe.LayerType.NormalMap.name
        return self._create_layer(tiles=tiles, name=name)

    def satellite_map(self, name=None):
        tiles = "//webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}"
        name = name if name is not None else self._default_layer_name(self.satellite_map)
        # name = name if name is not None else GaoDe.LayerType.SatelliteMap.name
        return self._create_layer(tiles=tiles, name=name)

    def satellite_annotation(self, name=None):
        tiles = "//webst0{s}.is.autonavi.com/appmaptile?style=8&x={x}&y={y}&z={z}"
        name = name if name is not None else self._default_layer_name(self.satellite_annotation)
        # name = name if name is not None else GaoDe.LayerType.SatelliteAnnotation.name
        return self._create_layer(tiles=tiles, name=name)


class Google(TmsLayerProvider):
    NormalMap = LayerType(Provider.Google, MapType.NormalMap)

    SatelliteMap = LayerType(Provider.Google, MapType.SatelliteMap)
    SatelliteAnnotation = LayerType(Provider.Google, MapType.SatelliteAnnotation)

    Normal = NormalMap
    Satellite = SatelliteMap | SatelliteAnnotation

    _LayerTypes = [
        NormalMap,
        SatelliteMap,
        SatelliteAnnotation,
    ]

    def __init__(self):
        super(Google, self).__init__()

        # Map provider specific options
        subdomains = self._SUBDOMAINS

        self._options = {
            'subdomains': subdomains,
            'attr': 'Google Map'
        }

        # Terrain = TerrainMap | TerrainAnnotation

    def _layer_simple(self, layer_type: LayerType, name=None):
        if layer_type not in self._LayerTypes:
            raise ValueError(f'Unsupported layer {layer_type}')
        assert layer_type.provider_type == Provider.Google

        if layer_type == self.NormalMap:
            return self.normal_map(name)
        elif layer_type == self.SatelliteMap:
            return self.satellite_map(name)
        elif layer_type == self.SatelliteAnnotation:
            return self.satellite_annotation(name)

    def normal_map(self, name=None):
        tiles = "//www.google.cn/maps/vt?lyrs=m@189&gl=cn&x={x}&y={y}&z={z}"
        name = name if name is not None else self._default_layer_name(self.normal_map)
        # name = name if name is not None else GaoDe.LayerType.NormalMap.name
        return self._create_layer(tiles=tiles, name=name)

    def satellite_map(self, name=None):
        tiles = "//www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"
        name = name if name is not None else self._default_layer_name(self.satellite_map)
        # name = name if name is not None else GaoDe.LayerType.NormalMap.name
        return self._create_layer(tiles=tiles, name=name)

    def satellite_annotation(self, name=None):
        tiles = "//www.google.cn/maps/vt?lyrs=y@189&gl=cn&x={x}&y={y}&z={z}"
        name = name if name is not None else self._default_layer_name(self.satellite_annotation)
        # name = name if name is not None else GaoDe.LayerType.NormalMap.name
        return self._create_layer(tiles=tiles, name=name)


class Geoq(TmsLayerProvider):
    NormalMap = LayerType(Provider.Geoq, MapType.NormalMap)
    NormalPurplishBlue = LayerType(Provider.Geoq, MapType.NormalPurplishBlue)
    NormalGray = LayerType(Provider.Geoq, MapType.NormalGray)
    NormalWarm = LayerType(Provider.Geoq, MapType.NormalWarm)
    ThemeHydro = LayerType(Provider.Geoq, MapType.ThemeHydro)

    Normal = NormalMap

    _LayerTypes = [
        NormalMap,
        NormalPurplishBlue,
        NormalGray,
        NormalWarm,

        ThemeHydro,
    ]

    def __init__(self):
        super(Geoq, self).__init__()

        # Map provider specific options
        subdomains = self._SUBDOMAINS

        self._options = {
            'subdomains': subdomains,
            'attr': 'Geoq Map'
        }

    def _layer_simple(self, layer_type: LayerType, name=None):
        if layer_type not in self._LayerTypes:
            raise ValueError(f'Unsupported layer {layer_type}')
        assert layer_type.provider_type == Provider.Geoq

        if layer_type == self.NormalMap:
            return self.normal_map(name)
        elif layer_type == self.NormalPurplishBlue:
            return self.normal_purplish_blue(name)
        elif layer_type == self.NormalWarm:
            return self.normal_warm(name)
        elif layer_type == self.NormalGray:
            return self.normal_gray(name)
        elif layer_type == self.ThemeHydro:
            return self.theme_hydro(name)

    def normal_map(self, name=None):
        tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineCommunity/MapServer/tile/{z}/{y}/{x}"
        name = name if name is not None else self._default_layer_name(self.normal_map)
        return self._create_layer(tiles=tiles, name=name)

    def normal_purplish_blue(self, name=None):
        tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}"
        name = name if name is not None else self._default_layer_name(self.normal_purplish_blue)
        return self._create_layer(tiles=tiles, name=name)

    def normal_gray(self, name=None):
        tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}"
        name = name if name is not None else self._default_layer_name(self.normal_gray)
        return self._create_layer(tiles=tiles, name=name)

    def normal_warm(self, name=None):
        tiles = "//map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetWarm/MapServer/tile/{z}/{y}/{x}"
        name = name if name is not None else self._default_layer_name(self.normal_warm)
        return self._create_layer(tiles=tiles, name=name)

    def theme_hydro(self, name=None):
        tiles = "//thematic.geoq.cn/arcgis/rest/services/ThematicMaps/WorldHydroMap/MapServer/tile/{z}/{y}/{x}"
        name = name if name is not None else self._default_layer_name(self.theme_hydro)
        return self._create_layer(tiles=tiles, name=name)


class Osm(TmsLayerProvider):
    _SUBDOMAINS = ['a', 'b', 'c']

    NormalMap = LayerType(Provider.Osm, MapType.NormalMap)

    Normal = NormalMap

    def __init__(self):
        super(Osm, self).__init__()

        # Map provider specific options
        subdomains = self._SUBDOMAINS

        self._options = {
            'subdomains': subdomains,
            'attr': 'OpenStreetMap'
        }

    def _layer_simple(self, layer_type: LayerType, name=None):
        if layer_type not in self._LayerTypes:
            raise ValueError(f'Unsupported layer {layer_type}')
        assert layer_type.provider_type == Provider.Osm

        if layer_type == self.NormalMap:
            return self.normal_map(name)

    def normal_map(self, name):
        tiles = "//{s}.tile.osm.org/{z}/{x}/{y}.png"
        name = name if name is not None else self._default_layer_name(self.normal_map)
        return self._create_layer(tiles=tiles, name=name)


class Baidu(TmsLayerProvider):
    _SUBDOMAINS = '0123456789'

    NormalMap = LayerType(Provider.Baidu, MapType.NormalMap)

    SatelliteMap = LayerType(Provider.Baidu, MapType.SatelliteMap)
    SatelliteAnnotation = LayerType(Provider.Baidu, MapType.SatelliteAnnotation)

    Normal = NormalMap
    Satellite = SatelliteMap | SatelliteAnnotation

    _LayerTypes = [
        NormalMap,
        SatelliteMap,
        SatelliteAnnotation,
    ]

    def __init__(self):
        super(Baidu, self).__init__()

        # Map provider specific options
        subdomains = self._SUBDOMAINS

        self._options = {
            'subdomains': subdomains,
            'attr': 'Baidu',
            'tms': True
        }

    def _layer_simple(self, layer_type: LayerType, name=None):
        if layer_type not in self._LayerTypes:
            raise ValueError(f'Unsupported layer {layer_type}')
        assert layer_type.provider_type == Provider.Baidu

        if layer_type == self.NormalMap:
            return self.normal_map(name)
        elif layer_type == self.SatelliteMap:
            return self.satellite_map(name)
        elif layer_type == self.SatelliteAnnotation:
            return self.satellite_annotation(name)

    def normal_map(self, name=None):
        tiles = "//online{s}.map.bdimg.com/onlinelabel/?qt=tile&x={x}&y={y}&z={z}&styles=pl&scaler=1&p=1"
        name = name if name is not None else self._default_layer_name(self.normal_map)
        return self._create_layer(tiles=tiles, name=name)

    def satellite_map(self, name=None):
        tiles = "//shangetu{s}.map.bdimg.com/it/u=x={x};y={y};z={z};v=009;type=sate&fm=46"
        name = name if name is not None else self._default_layer_name(self.satellite_map)
        return self._create_layer(tiles=tiles, name=name)

    def satellite_annotation(self, name=None):
        tiles = "//online{s}.map.bdimg.com/tile/?qt=tile&x={x}&y={y}&z={z}&styles=sl&v=020"
        name = name if name is not None else self._default_layer_name(self.satellite_annotation)
        return self._create_layer(tiles=tiles, name=name)

    class BaiduTileLayer(TileLayer):
        def __init__(self, tiles, name, **kwargs):
            super(Baidu.BaiduTileLayer, self).__init__(tiles=tiles, name=name, **kwargs)

        def render(self, **kwargs):
            # check crs
            app_map = self._get_app_map()
            if app_map.crs != 'Baidu':
                raise ValueError(f"folium.Map's crs '{app_map.crs}' conflicts with Baidu Map's crs 'Baidu',"
                                 f" please consider set folium.Map's crs to 'Baidu' or remove Baidu Map ")

            # render BaiduTileLayer
            super(Baidu.BaiduTileLayer, self).render(**kwargs)

            # add links
            figure = self.get_root()
            assert isinstance(figure, Figure), ('You cannot render this Element '
                                                'if it is not in a Figure.')

            figure.header.add_child(JavascriptLink("https://cdn.bootcss.com/proj4js/2.4.3/proj4.js"), name='proj4.js')
            figure.header.add_child(JavascriptLink("https://cdn.bootcss.com/proj4leaflet/1.0.1/proj4leaflet.min.js"),
                                    name='proj4leaflet.min.js'
                                    )

            pro_crs = """
            <script>
               if (L.Proj) {
                L.CRS.Baidu = new L.Proj.CRS('EPSG:900913', '+proj=merc +a=6378206 +b=6356584.314245179 +lat_ts=0.0 +lon_0=0.0 +x_0=0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs', {
                    resolutions: function () {
                        level = 19
                        var res = [];
                        res[0] = Math.pow(2, 18);
                        for (var i = 1; i < level; i++) {
                            res[i] = Math.pow(2, (18 - i))
                        }
                        return res;
                    }(),
                    origin: [0, 0],
                    bounds: L.bounds([20037508.342789244, 0], [0, 20037508.342789244])
                });
            } 
            </script>
            """
            figure.html.add_child(Element(pro_crs), name='L.CRS.Baidu')

        def _get_app_map(self):
            # parent = self._parent
            # while parent:
            #     if isinstance(parent, folium.Map):
            #         return parent
            #
            #     # traverse to root, but Map not found
            #     if parent == parent._parent:
            #         break
            #
            #     parent = parent._parent
            return get_obj_in_upper_tree(self, Map)

    def _create_layer(self, tiles, name):
        return Baidu.BaiduTileLayer(tiles=tiles, name=name, **self._options)


@lru_cache()
def create_provider(provider_type: Provider):
    if provider_type == Provider.TianDiTu:
        return TianDiTu()
    elif provider_type == Provider.GaoDe:
        return GaoDe()
    elif provider_type == Provider.Google:
        return Google()
    elif provider_type == Provider.Geoq:
        return Geoq()
    elif provider_type == Provider.Osm:
        return Osm()
    elif provider_type == Provider.Baidu:
        return Baidu()
    else:
        raise ValueError(f'Unsupported provider type {provider_type}')


def create_layer(layer_type: LayerType):
    provider_type = layer_type.provider_type
    return create_provider(provider_type).layer(layer_type)


def create_layers(layer_types: List[LayerType]):
    return (create_layer(layer_type=layer_type) for layer_type in layer_types)


# ----------------------------------------------------------------


def create_base_map(location=None,
                    zoom_start=15):
    # Base map
    base_map = folium.Map(
        location=location,
        zoom_start=zoom_start,
        tiles=None,
    )

    # Add layers to app map
    # providers = [TianDiTu(), GaoDe(), Google(), Geoq(), Osm()]
    providers = [TianDiTu(), GaoDe(), Osm()]
    for layer in itertools.chain(*(p.layers() for p in providers)):
        layer.add_to(base_map)

    return base_map


def create_baidu_map(location=None,
                     zoom_start=15):
    baidu_map = folium.Map(
        location=location,
        zoom_start=zoom_start,
        tiles=None,
        crs='Baidu',
    )

    Baidu().layer(Baidu.Normal, 'Map').add_to(baidu_map)
    Baidu().layer(Baidu.Satellite, 'Satellite').add_to(baidu_map)

    return baidu_map


def create_gaode_map(location=None, zoom_start=15):
    gaode_map = folium.Map(
        location=location,
        zoom_start=zoom_start,
        tiles=None,
    )

    GaoDe().layer(GaoDe.Normal, 'Map').add_to(gaode_map)
    GaoDe().layer(GaoDe.Satellite, 'Satellite').add_to(gaode_map)

    return gaode_map


def create_tianditu_map(location=None, zoom_start=15):
    tianditu_map = folium.Map(
        location=location,
        zoom_start=zoom_start,
        tiles=None,
    )

    TianDiTu().layer(TianDiTu.Normal, 'Map').add_to(tianditu_map)
    TianDiTu().layer(TianDiTu.Satellite, 'Satellite').add_to(tianditu_map)

    return tianditu_map

def create_app_maps():
    import os
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app'))

    # init location
    location = (31.28664929, 121.60358643)
    zoom_start = 15

    # base map
    base_map = create_base_map(location=location, zoom_start=zoom_start)
    folium.LayerControl().add_to(base_map)
    folium.plugins.MousePosition(position='bottomleft', empty_string='').add_to(base_map)

    base_map.save(os.path.join(app_dir, 'provider_base_map.html'))

    # baidu map
    baidu_map = create_baidu_map(location=location, zoom_start=zoom_start)
    folium.LayerControl().add_to(baidu_map)  # TODO: LayerControl must be added after all layers
    folium.plugins.MousePosition(position='bottomleft', empty_string='').add_to(baidu_map)

    baidu_map.save(os.path.join(app_dir, 'provider_baidu_map.html'))

    return {
        'Base': base_map,
        'Baidu': baidu_map,
    }


def main():
    create_app_maps()


if __name__ == '__main__':
    m_type = MapType.NormalMap | MapType.NormalAnnotation
    # print(repr(m_type))
    # print(repr(Baidu.Satellite))
    main()
