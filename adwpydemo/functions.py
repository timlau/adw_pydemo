from gi.repository import Gtk, Adw

def get_action_row(num):
    title = f'Action {num}'
    row = Adw.ActionRow()
    row.set_title(title)
    row.set_subtitle(f"This is an action")
    row.set_icon_name('find-location-symbolic')
    switch = Gtk.Switch()
    switch.props.halign = Gtk.Align.CENTER
    switch.props.valign = Gtk.Align.CENTER
    switch.props.hexpand = False
    switch.props.vexpand = False
    switch.set_active(num % 2 == 0)
    row.add_suffix(switch)
    return row
