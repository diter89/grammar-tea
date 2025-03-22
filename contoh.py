#!/usr/bin/env python
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from custom_lexer import CustomLexer


def main():
    # Buat instance PromptSession dengan lexer kustom
    session = PromptSession(
        lexer=PygmentsLexer(CustomLexer), 
    )

    print("Selamat datang di aplikasi dengan lexer kustom!")
    print("Ketik Ctrl+D atau 'exit' untuk keluar.")

    while True:
        try:
            # Dapatkan input dari pengguna
            text = session.prompt("» ")
            if text.strip().lower() in ("exit", "quit"):
                print("Keluar dari aplikasi.")
                break
            print(f"Anda mengetik: {text}")
        except EOFError:
            # Tangani Ctrl+D
            print("\nKeluar dari aplikasi.")
            break

if __name__ == "__main__":
    main()
