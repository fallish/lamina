# encoding: utf-8
"""
@author: Michael
@file: sqls.py
@time: 2020/4/22 9:08 AM
@desc:
"""


def sql_query_links(box):
    xmin, ymin, xmax, ymax = box
    # ymin, xmin, ymax, xmax = box
    envelope = f"ST_MakeEnvelope( {xmin}, {ymin}, {xmax}, {ymax}, 4326)"

    sql = f"""
        SELECT row_to_json(fc) AS data
        FROM (
                 SELECT 'FeatureCollection'         as "type",
                        array_to_json(array_agg(f)) AS features
                 FROM (
                          SELECT 'Feature'                AS type,
                                 (
                                     SELECT json_strip_nulls(row_to_json(t))
                                     FROM (SELECT id, fc, nr, rt, rst, isbridge ) AS t
                                 )                        AS properties,
                                 ST_AsGeoJSON(ST_Force2D(geom))::json AS geometry
                          FROM tnv_map.linktable
                          WHERE ST_Intersects(geom, {envelope})
                      ) AS f
             ) as fc
        """
    return sql



