
import libdiggrpy as dg


class Messages:

    def __init__(self):
        self.t = 0
        self.last_msg_t = 0

    def m(self, s, bold = None):
        self.last_msg_t = self.t
        dg.render_message(s, bool(bold))

    def show_all(self):
        dg.render_draw_messages_window()

