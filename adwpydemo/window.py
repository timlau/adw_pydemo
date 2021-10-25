from gi.repository import Gtk, Gio, Adw, GLib

from adwpydemo.const import Constants

@Gtk.Template(resource_path=f'{Constants.PATHID}/ui/mainwindow.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'    
    
    main_content = Gtk.Template.Child()
    app_menu = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
         Adw.ApplicationWindow.__init__(self, **kwargs)
         # Setup Headerbar
         self.headerbar = Gtk.HeaderBar()
         self.btn_menu = Gtk.MenuButton()
         self.btn_menu.props.icon_name = 'open-menu-symbolic'
         self.btn_menu.set_menu_model(self.app_menu)
         title = Gtk.Label()
         title.set_text('Libadwaita Python Demo')
         self.headerbar.set_title_widget(title)
         self.headerbar.pack_end(self.btn_menu)
         self.main_content.append(self.headerbar)

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

