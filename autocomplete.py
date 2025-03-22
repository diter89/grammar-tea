#!/usr/bin/env python
from rich import print
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Float, FloatContainer, HSplit, Window
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.html import HtmlLexer
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Frame, TextArea


class PenyelesaiOtomatis:
    """
    Class untuk menangani penyelesaian otomatis.
    """
    def __init__(self, kata_kunci, meta_dict=None):
        self.kata_kunci = kata_kunci
        self.meta_dict = meta_dict or {}
        self.completer = FuzzyWordCompleter(self.kata_kunci, meta_dict=self.meta_dict)

    def get_completer(self):
        return self.completer


class AplikasiPrompt:
    def __init__(self, completer=None, lexer=PythonLexer):
        # Inisialisasi penyelesaian otomatis
        self.penyelesai_otomatis = completer.get_completer() if completer else None

        # Lexer (default menggunakan PythonLexer jika tidak disediakan)
        self.lexer = PygmentsLexer(lexer)

        # Riwayat input untuk autosuggest
        self.riwayat_input = []

        # Area teks
        self.area_teks = TextArea(
            lexer=self.lexer,
            prompt="» ",
            completer=self.penyelesai_otomatis,
            complete_while_typing=True,
            focus_on_click=True,
            auto_suggest=AutoSuggestFromHistory(),
        )

        # Konten utama
        self.konten_utama = FloatContainer(
            content=HSplit(
                [
                    Frame(self.area_teks, height=3, style="fg:#0a7e89 bold"),
                ],
            ),
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=16, scroll_offset=2),
                )
            ],
        )

        # Pengikatan tombol
        self.pengikatan_tombol = KeyBindings()

        @self.pengikatan_tombol.add("enter")
        def _tekan_enter(event):
            # Simpan teks yang dimasukkan ke riwayat
            teks_input = self.area_teks.text
            if teks_input.strip():  # Jangan simpan input kosong
                self.riwayat_input.append(teks_input)
            # Kosongkan buffer setelah Enter
            self.area_teks.buffer.reset()
            # Update history untuk AutoSuggestFromHistory
            self.area_teks.buffer.history.append_string(teks_input)
            # Keluar dari aplikasi dan kembalikan teks
            event.app.exit(result=teks_input)

        @self.pengikatan_tombol.add('c-q')
        def _keluar(event):
            event.app.exit(1)

        # Gaya
        self.gaya = Style.from_dict(
            {
                "completion.menu": "#0a0a0a",
                "scrollbar.background": "bg:#0a7e98 bold",
                "completion-menu.completion": "bg:#0a0a0a fg:#aaaaaa bold",
                "completion-menu.completion fuzzymatch.outside": "#aaaaaa underline",
                "completion-menu.completion fuzzymatch.inside": "fg:#9ece6a bold",
                "completion-menu.completion fuzzymatch.inside.character": "underline bold",
                "completion-menu.completion.current fuzzymatch.outside": "fg:#9ece6a underline",
                "completion-menu.completion.current fuzzymatch.inside": "fg:#f7768e bold",
                "completion-menu.meta.completion": "bg:#0a0a0a fg:#aaaaaa bold",
                "completion-menu.meta.completion.current": "bg:#888888",
            },
        )

        # Aplikasi
        self.aplikasi = Application(
            layout=Layout(self.konten_utama, focused_element=self.area_teks),
            key_bindings=self.pengikatan_tombol,
            style=self.gaya,
            full_screen=False
        )

    def jalankan(self):
        """
        Menjalankan aplikasi dan mengembalikan teks yang dimasukkan.
        """
        return self.aplikasi.run()


if __name__ == "__main__":
    # Daftar kata kunci dan meta data untuk penyelesaian otomatis
    kata_kunci = [
        "impor",
        "dari",
        "menggunakan_headers : -: 0",
        "peretas",
    ]
    meta_dict = {
        "peretas": HTML("│ 📦 <ansired>Peretas ini ....</ansired> peretas handal ...."),
        'impor': HTML("│ 📦 <ansiblue>Paket impor ini ...</ansiblue>"),
        "dari": HTML("│ 📦 <ansired>dari regex... </ansired>"),
        "menggunakan_headers : -: 0": "│ tertutup ...",
    }

    # Buat instance PenyelesaiOtomatis
    penyelesai_otomatis = PenyelesaiOtomatis(kata_kunci, meta_dict)

    # Pilih lexer: PythonLexer atau HtmlLexer
    lexer_pilihan = HtmlLexer  # Ganti dengan PythonLexer jika ingin menggunakan PythonLexer

    lexer = PythonLexer

    # Buat instance AplikasiPrompt dengan penyelesaian otomatis dan lexer pilihan
    app = AplikasiPrompt(completer=penyelesai_otomatis, lexer=lexer)

    while True:
        hasil = app.jalankan()  # Menjalankan aplikasi dan mendapatkan input
        if hasil == 1:  # Jika pengguna menekan Ctrl+Q
            print("Keluar dari aplikasi.")
            break
        print(f"Teks yang dimasukkan: {hasil}")
