from gi.repository import Gtk


def get_label(text):
    lbl = Gtk.Label()
    lbl.set_text(text)
    lbl.props.halign = Gtk.Align.CENTER
    lbl.props.valign = Gtk.Align.CENTER
    lbl.props.hexpand = True
    lbl.props.vexpand = True
    return lbl


def get_label_top(text):
    lbl = Gtk.Label()
    lbl.set_markup(text)
    lbl.props.halign = Gtk.Align.START
    lbl.props.valign = Gtk.Align.START
    lbl.props.hexpand = True
    lbl.props.vexpand = False
    return lbl


def get_label_bottom(text):
    lbl = Gtk.Label()
    lbl.set_markup(text)
    lbl.props.halign = Gtk.Align.END
    lbl.props.valign = Gtk.Align.END
    lbl.props.hexpand = True
    lbl.props.vexpand = False
    return lbl

def set_margin(widget, value):
    widget.props.margin_top = 10
    widget.props.margin_bottom = 10
    widget.props.margin_start = 10
    widget.props.margin_end = 10

