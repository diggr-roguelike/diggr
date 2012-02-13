
import libdiggrpy as dg


class Messages:

    def m(self, s, bold = None):
        dg.render_message(s, bool(bold))

    def show_all(self):
        dg.render_draw_messages_window()

