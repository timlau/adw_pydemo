from gi.repository import Gtk, Gio, Adw, GLib

from adwpydemo.const import Constants
from adwpydemo.functions import get_label, get_label_bottom, get_label_top, set_margin


@Gtk.Template(resource_path=f'{Constants.PATHID}/ui/main.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    main_content = Gtk.Template.Child()
    flap = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    stack_switch = Gtk.Template.Child()
    page1_box  = Gtk.Template.Child()
    page1_switch  = Gtk.Template.Child()
    page1_content  = Gtk.Template.Child()
    page2_box  = Gtk.Template.Child()
    page3_box  = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Adw.ApplicationWindow.__init__(self, **kwargs)
        self.style_manager = Adw.StyleManager().get_default()

        # # setup menu actions
        self.create_action('new', self.menu_handler)
        self.create_action('about', self.menu_handler)
        self.create_action('quit', self.menu_handler)
        self.add_page1()
        self.add_page2()
        self.add_page3()

    def add_page1(self):
        self.page1_switch.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        for num in ['1', '2', '3']:
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            title = f'Page {num}'
            name = f'page{num}'
            box.append(Gtk.Separator())
            lbl = get_label_top('<b>⇧ This is a ViewSwitcher</b>')
            set_margin(lbl, 5)
            box.append(lbl)
            lbl = get_label(f'This is a ViewStack page  ({num})')
            box.append(lbl)
            lbl = get_label_bottom('<b>This is a ViewSwitcherBar ⇩</b>')
            set_margin(lbl, 5)
            box.append(lbl)
            page = self.page1_content.add_named(box, name)
            page.set_title(title)
            page.set_icon_name('media-record-symbolic')

    def add_page2(self):
        self.page2_box.append(Gtk.Separator())
        self.leaflet = Adw.Leaflet()
        btn = Gtk.Button()
        btn.set_label("This is an Left/Start Button")
        btn.props.halign = Gtk.Align.START
        btn.props.valign = Gtk.Align.START
        btn.props.vexpand = True
        btn.props.hexpand = True
        set_margin(btn, 10)
        self.leaflet.append(btn)
        btn = Gtk.Button()
        btn.set_label("This is a Right/End Button")
        btn.props.halign = Gtk.Align.END
        btn.props.valign = Gtk.Align.END
        btn.props.vexpand = True
        btn.props.hexpand = True
        set_margin(btn, 10)
        self.leaflet.append(btn)
        self.page2_box.append(self.leaflet)
        return self.page2_box

    def add_page3(self):
        page = Adw.PreferencesPage()
        page.set_title('This is an PreferencePage')
        group = Adw.PreferencesGroup()
        group.set_title('This is an PreferenceGroup')
        group.set_description("It contains a number of ActionRow's")
        page.add(group)
        for x in range(10):
            title = f'Action {x+1}'
            row = Adw.ActionRow()
            row.set_title(title)
            row.set_subtitle(f"This is an action, named {title}")
            row.set_icon_name('find-location-symbolic')
            switch = Gtk.Switch()
            switch.props.halign = Gtk.Align.CENTER
            switch.props.valign = Gtk.Align.CENTER
            switch.props.hexpand = False
            switch.props.vexpand = False
            switch.set_active(x % 2 == 0)
            row.add_suffix(switch)
            group.add(row)
        self.page3_box.append(page)

    @Gtk.Template.Callback()
    def on_color_switch(self, *args):
        if self.style_manager.get_dark():
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    @Gtk.Template.Callback()
    def on_leaflet_forward(self, widget):
        if self.leaflet.get_folded():
            self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    @Gtk.Template.Callback()
    def on_leaflet_back(self, widget):
        if self.leaflet.get_folded():
            self.leaflet.navigate(Adw.NavigationDirection.BACK)

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
        css_provider = None
        css_provider = Gtk.CssProvider()
        css_path = 'data/main.css'
        try:
            css_provider.load_from_resource(resource_path=css_path)
        except GLib.Error as e:
            print(f"Error loading CSS : {e} ")
            return None
        print(f'loading custom styling from resource: {css_path}')
        return css_provider

    def _add_widget_styling(self, widget):
        if self.css_provider:
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
