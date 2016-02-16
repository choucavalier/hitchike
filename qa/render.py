from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import hoedown as h

class PygmentRenderer(h.HtmlRenderer, h.SmartyPants):
    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % text.strip()
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(text, lexer, formatter)

def render(text):
    renderer = PygmentRenderer()
    md = h.Markdown(renderer,
                    extensions=h.EXT_FENCED_CODE | h.EXT_NO_INTRA_EMPHASIS)
    return md.render(text)
