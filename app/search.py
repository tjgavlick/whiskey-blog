# -*- coding: utf-8 -*-

import re

from flask import render_template, request, redirect, url_for

from app import app, db


@app.route('/search/')
def search():

    # hoo boy. compile reviews into full-text 'documents' and search on them
    tmp = db.session.execute("SELECT r_id, r_title, r_subtitle FROM ( \
                                  SELECT review.id AS r_id, \
                                         review.title AS r_title, \
                                         review.subtitle AS r_subtitle, \
                                         to_tsvector(review.title) || \
                                         to_tsvector(review.subtitle) || \
                                         to_tsvector(distiller.name) || \
                                         to_tsvector(review.body) \
                                         AS document \
                                  FROM review \
                                  LEFT JOIN distiller ON distiller.id = review.distiller_id \
                                  WHERE review.is_published \
                                  GROUP BY review.id, distiller.id) article_search \
                              WHERE article_search.document @@ to_tsquery('craig');")
    for row in tmp:
        print(row)

    r = re.compile(r'[^a-zA-Z0-9_\-]')
    keywords = re.sub(r, ' ', request.args.get('q', ''))
    if keywords:
        return keywords
    return ''
