import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_raiz)

from antlr4 import *
from LenguajeLexer import LenguajeLexer
import os


def traducir_a_c(lexema):
    traducciones = {
        "entero": "int",
        "decimal": "float",
        "cadena": "char[]",
        "booleano": "int",
        "imprimir": "printf"
    }
    return traducciones.get(lexema, "")


def main():
    os.makedirs("reportes_html", exist_ok=True)

    input_stream = FileStream("programa.leng")
    lexer = LenguajeLexer(input_stream)

    tokens_lista = []
    token = lexer.nextToken()

    while token.type != Token.EOF:
        tipo = lexer.symbolicNames[token.type] if token.type < len(lexer.symbolicNames) else str(token.type)

        tokens_lista.append({
            "tipo": tipo,
            "lexema": token.text,
            "linea": token.line,
            "columna": token.column,
            "traduccion": traducir_a_c(token.text)
        })

        token = lexer.nextToken()

    html = """
    <html>
    <head><title>Tokens</title></head>
    <body>
    <h1>Reporte de Tokens</h1>
    <table border="1">
    <tr><th>Tipo</th><th>Lexema</th><th>Línea</th><th>Columna</th><th>Traducción C</th></tr>
    """

    for t in tokens_lista:
        html += f"""
        <tr>
            <td>{t['tipo']}</td>
            <td>{t['lexema']}</td>
            <td>{t['linea']}</td>
            <td>{t['columna']}</td>
            <td>{t['traduccion']}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open("reportes_html/reporte_tokens.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Reporte de tokens generado ✔")


if __name__ == "__main__":
    main()
