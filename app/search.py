# -*- coding: utf-8 -*-

import re

from flask import render_template, request, redirect, url_for

from app import app, db

# hoo boy. compile reviews and articles into full-text 'documents' and search on them
db.session.execute("SET LOCAL maintenance_work_mem = '1GB';")
db.session.execute("SET LOCAL work_mem = '100MB';")
db.session.execute("CREATE MATERIALIZED VIEW IF NOT EXISTS search_index AS \
                    SELECT p_id, p_title, p_subtitle, p_url, p_image, document FROM ( \
                        SELECT review.id AS p_id, \
                               review.title AS p_title, \
                               review.subtitle AS p_subtitle, \
                               review.url AS p_url, \
                               review.image_list AS p_image, \
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
                               article.image_list AS p_image, \
                               setweight(to_tsvector(article.title), 'A') || \
                               setweight(to_tsvector(article.subtitle), 'A') || \
                               setweight(to_tsvector(article.body), 'B') \
                               AS document \
                        FROM article \
                        WHERE article.is_published \
                    ) p_search;")
db.session.execute("CREATE INDEX IF NOT EXISTS idx_fts_search ON search_index USING gin(document);")
db.session.commit()


@app.route('/search/')
def search():
    tmp = db.session.execute("SELECT p_id, p_title, p_subtitle, p_url, p_image \
                              FROM search_index \
                              WHERE document @@ to_tsquery('alcohol') \
                              ORDER BY ts_rank(document, to_tsquery('alcohol')) DESC;")
    for row in tmp:
        print(row)

    r = re.compile(r'[^a-zA-Z0-9_\-]')
    keywords = re.sub(r, ' ', request.args.get('q', ''))
    if keywords:
        return keywords
    return ''
