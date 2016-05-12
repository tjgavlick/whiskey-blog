# -*- coding: utf-8 -*-

import re

from flask import render_template, request, redirect, url_for

from app import app, db

# hoo boy. compile reviews and articles into full-text 'documents' and search on them
tmp = db.session.execute("SELECT p_id, p_title, p_subtitle FROM ( \
                              SELECT review.id AS p_id, \
                                     review.title AS p_title, \
                                     review.subtitle AS p_subtitle, \
                                     review.url AS p_url, \
                                     setweight(to_tsvector(review.title), 'A') || \
                                     setweight(to_tsvector(review.subtitle), 'A') || \
                                     setweight(to_tsvector(distiller.name), 'C') || \
                                     setweight(to_tsvector(review.body), 'B') || \
                                     setweight(to_tsvector(review.drink_type), 'D') \
                                     AS document \
                              FROM review \
                              LEFT JOIN distiller ON distiller.id = review.distiller_id \
                              WHERE review.is_published \
                              GROUP BY review.id, distiller.id \
                              UNION \
                              SELECT article.id AS p_id, \
                                     article.title AS p_title, \
                                     article.subtitle AS p_subtitle, \
                                     article.url AS p_url, \
                                     setweight(to_tsvector(article.title), 'A') || \
                                     setweight(to_tsvector(article.subtitle), 'A') || \
                                     setweight(to_tsvector(article.body), 'B') \
                                     AS document \
                              FROM article \
                              WHERE article.is_published \
                          ) p_search \
                          WHERE p_search.document @@ to_tsquery('alcohol') \
                          ORDER BY ts_rank(p_search.document, to_tsquery('alcohol')) DESC;")
for row in tmp:
    print(row)

@app.route('/search/')
def search():


    r = re.compile(r'[^a-zA-Z0-9_\-]')
    keywords = re.sub(r, ' ', request.args.get('q', ''))
    if keywords:
        return keywords
    return ''
