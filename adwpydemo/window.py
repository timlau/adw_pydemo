from gi.repository import Gtk, Gio, Adw, GLib

from adwpydemo.const import Constants
from adwpydemo.functions import get_action_row


@Gtk.Template(resource_path=f'{Constants.PATHID}/ui/main.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    main_content = Gtk.Template.Child()
    flap = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    stack_switch = Gtk.Template.Child()
    # Page1 widgets
    page1_box = Gtk.Template.Child()
    page1_switch = Gtk.Template.Child()
    page1_content = Gtk.Template.Child()
    # Page2 widgets
    page2_box = Gtk.Template.Child()
    page2_leaflet = Gtk.Template.Child()
    # Page3 widgets
    page3_box = Gtk.Template.Child()
    page3_pref_grp1 = Gtk.Template.Child()
    page3_pref_grp2 = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Adw.ApplicationWindow.__init__(self, **kwargs)
        self.style_manager = Adw.StyleManager().get_default()

        # # setup menu actions
        self.create_action('new', self.menu_handler)
        self.create_action('about', self.menu_handler)
        self.create_action('quit', self.menu_handler)
        self.add_page3()
        self.css_provider = self.load_css()
        self.add_custom_styling(self.main_content)

    def add_page3(self):
        for x in range(5):
            row = get_action_row(x+1)
            self.page3_pref_grp1.add(row)
        for x in range(5):
            row = get_action_row(x+1)
            self.page3_pref_grp2.add(row)

    @Gtk.Template.Callback()
    def on_color_switch(self, *args):
        if self.style_manager.get_dark():
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    @Gtk.Template.Callback()
    def on_leaflet_forward(self, widget):
        if self.page2_leaflet.get_folded():
            self.page2_leaflet.navigate(Adw.NavigationDirection.FORWARD)

    @Gtk.Template.Callback()
    def on_leaflet_back(self, widget):
        if self.page2_leaflet.get_folded():
            self.page2_leaflet.navigate(Adw.NavigationDirection.BACK)

    @Gtk.Template.Callback()
    def on_flap_toggled(self, widget):
        self.flap.set_reveal_flap(not self.flap.get_reveal_flap())

    def on_button_clicked(self, widget):
        label = widget.get_label()
        print(f'Button {label} Pressed')

    def menu_handler(self, action, state):
        """ Callback for  menu actions"""
        name = action.get_name()
        print(f'active : {name}')

    def load_css(self):
        """create a provider for custom styling"""
        css_provider = Gtk.CssProvider()
        css_path = f'{Constants.PATHID}/ui/main.ui'
        try:
            css_provider.load_from_resource(resource_path=css_path)
        except GLib.Error as e:
            print(f"Error loading CSS : {e} ")
            return None
        print(f'loading custom styling from resource: {css_path}')
        return css_provider

    def _add_widget_styling(self, widget):
        if self.css_provider:
            print(f'Adding style to : {widget.props.css_name}')
            context = widget.get_style_context()
            context.add_provider(
                self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def add_custom_styling(self, widget):
        self._add_widget_styling(widget)
        # iterate children recursive
        for child in widget:
            self.add_custom_styling(child)

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
