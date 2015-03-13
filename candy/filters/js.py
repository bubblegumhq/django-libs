from __future__ import absolute_import
from compressor.filters import CallbackOutputFilter
import jsmin


from slimit.parser import Parser

def echo(str):
    return str

def dumbit(str):
    parser = Parser()
    tree = parser.parse(str)
    return tree.to_ecma()


class EchoFilter(CallbackOutputFilter):
    callback = "candy.filters.js.echo"

class JSMinFilter(CallbackOutputFilter):
    dependencies = ["jsmin"]
    callback = "jsmin.jsmin"


class SlimItNoMangleFilter(CallbackOutputFilter):
    dependencies = ["slimit"]
    callback = "slimit.minify"
    kwargs = {
        "mangle": False,
    }