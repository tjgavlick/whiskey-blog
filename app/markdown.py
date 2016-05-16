# -*- coding: utf-8 -*-

import re

from mistune import Renderer, Markdown, InlineGrammar, InlineLexer


class TdwInlineLexer(InlineLexer):

    def __init__(self, renderer):
        super(TdwInlineLexer, self).__init__(renderer)

        # insert fragment searching: [#fragment]
        self.rules.fragment = re.compile(r'\[#([a-zA-Z0-9]+?)\]')
        self.default_rules.insert(0, 'fragment')

    def output_fragment(self, m):
        text = m.group(1)
        return '<span id="{}"></span>'.format(text)


renderer = Renderer(escape=True, use_xhtml=True)
inline = TdwInlineLexer(renderer)
markdown = Markdown(renderer=renderer, inline=inline)
