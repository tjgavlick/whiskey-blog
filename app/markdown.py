# -*- coding: utf-8 -*-

import re

from mistune import Renderer, Markdown, InlineGrammar, InlineLexer


class TdwInlineLexer(InlineLexer):

    def __init__(self, renderer):
        super(TdwInlineLexer, self).__init__(renderer)

        # insert fragment searching: [Fragment text #id]
        self.rules.fragment = re.compile(r'\[(.+?)\s#([a-zA-Z0-9]+?)\]')
        self.default_rules.insert(0, 'fragment')

    def output_fragment(self, m):
        text = m.group(1)
        id = m.group(2)
        return '<span id="{}" class="fragment">{}</span>'.format(id, text)


renderer = Renderer(escape=True, use_xhtml=True)
inline = TdwInlineLexer(renderer)
markdown = Markdown(renderer=renderer, inline=inline)
