# -*- coding: utf-8 -*-

import re

from flask import render_template, request, redirect, url_for

from app import app, db

# hoo boy. compile reviews and articles into full-text 'documents' and search on them
db.session.execute("CREATE MATERIALIZED VIEW IF NOT EXISTS search_index AS \
                    SELECT p_id, p_title, p_subtitle, p_url, p_image, p_abstract, p_type, document FROM ( \
                        SELECT review.id AS p_id, \
                               review.title AS p_title, \
                               review.subtitle AS p_subtitle, \
                               review.url AS p_url, \
                               review.image_list AS p_image, \
                               review.abstract AS p_abstract, \
                               'review' AS p_type, \
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
                               article.abstract AS p_abstract, \
                               'article' AS p_type, \
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
    bad_stuff = re.compile(r'[^a-zA-Z0-9_\-]')
    whitespace = re.compile(r'\s+')
    post_keys = ('id', 'title', 'subtitle', 'url', 'image_list', 'abstract', 'type')

    posts = []
    keywords = re.sub(bad_stuff, ' ', request.args.get('q', ''))
    keywords = re.sub(whitespace, ' ', keywords).strip()

    if keywords:
        # just OR queries for now
        search_query = ' | '.join(filter(len, map(lambda x: x.strip(), keywords.split(' '))))
        results = db.session.execute("SELECT p_id, p_title, p_subtitle, p_url, p_image, p_abstract, p_type \
                                      FROM search_index \
                                      WHERE document @@ to_tsquery('" + search_query + "') \
                                      ORDER BY ts_rank(document, to_tsquery('" + search_query + "')) DESC;")
        for row in results:
            posts.append(dict(zip(post_keys, row)))

    return render_template('search.html', posts=posts, keywords=keywords)
