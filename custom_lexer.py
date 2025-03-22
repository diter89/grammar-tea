# custom_lexer.py
from pygments.lexer import RegexLexer
from pygments.token import Token, Keyword, Name, Operator, Text

class CustomLexer(RegexLexer):
    name = "CustomLexer"
    aliases = ["custom"]
    filenames = ["*.custom"]

    tokens = {
        "root": [
            (r"RequireTea=", Keyword.Reserved),
            (r"warna", Keyword.Reserved),
            (r"ila", Operator),
            (r"BTC", Name.Entity),    
            (r"USDT", Name.Builtin),  
            (r"(biru|putih|orange)", Name.Color),
            (r'[("=")]', Operator),
            (r"\s+", Text),
            (r".+", Text),
        ],
    }
