from tonnikala.exceptions import ParseError
from tonnikala.ir.nodes import ExpressionNode

from jslex import JsLexer
import re

class JavascriptExpressionNode(ExpressionNode):
    pass

identifier_match = re.compile(r'[a-zA-Z_$][a-zA-Z_$0-9]*')

def parse_expression(text, start_pos=0):
    lex = JsLexer()
    nodes = []

    if text[start_pos + 1] != '{':
        m = identifier_match.match(text, start_pos + 1)
        identifier = m.group(0)
        return JavascriptExpressionNode('$' + identifier, [('id', identifier)])

    braces = 0
    length = 2
    valid  = False
    tokens = lex.lex(text, start_pos + 2)
    for type, content in tokens:
        if content == '}':
            if braces <= 0:
                length += 1
                valid = True
                break

            braces -= 1

        if content == '{':
            braces += 1
        
        length += len(content)
        nodes.append((type, content))

    if not valid:
        raise ParseError("Not finished javascript expression", charpos=length)

    return JavascriptExpressionNode(text[start_pos:start_pos + length], nodes)
