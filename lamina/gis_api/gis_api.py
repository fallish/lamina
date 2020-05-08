# encoding: utf-8
"""
@author: Michael
@file: gis_api.py
@time: 2020/4/17 9:57 AM
@desc:
"""
from functools import lru_cache

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine

from lamina.gis_api.sqls.sqls import sql_query_links

app = Flask(__name__)
CORS(app)


@lru_cache()
def engine_map():
    host = 'localhost'
    passwd = 'xxxx'
    url = f'postgresql://postgres:{passwd}@{host}/hdmap'

    return create_engine(url)


@app.route('/links', methods=['GET'])
def query_links():
    box_opt = request.args.get('bbox')
    if not box_opt:
        return {}
    box = map(float, box_opt.split(','))

    sql = sql_query_links(box)
    first_row = engine_map().execute(sql).first()
    result = first_row.data if first_row else {}

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
