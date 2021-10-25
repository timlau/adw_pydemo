from gi.repository import Gtk, Gio, Adw, GLib

from adwpydemo.const import Constants


def get_label(text):
    lbl = Gtk.Label()
    lbl.set_text(text)
    lbl.props.halign = Gtk.Align.CENTER
    lbl.props.valign = Gtk.Align.CENTER
    lbl.props.hexpand = True
    lbl.props.vexpand = True
    return lbl

@Gtk.Template(resource_path=f'{Constants.PATHID}/ui/mainwindow.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    main_content = Gtk.Template.Child()
    app_menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Adw.ApplicationWindow.__init__(self, **kwargs)
        # Setup Headerbar
        self.headerbar = Adw.HeaderBar()
        self.btn_menu = Gtk.MenuButton()
        self.btn_menu.props.icon_name = 'open-menu-symbolic'
        self.btn_menu.set_menu_model(self.app_menu)
        # Flap toggle
        self.btn_flap = Gtk.ToggleButton()
        self.btn_flap.props.icon_name = 'sidebar-show-right-rtl-symbolic'
        self.btn_flap.set_active(True)
        self.btn_flap.connect('toggled', self.on_flap_toggled)
        self.headerbar.pack_start(self.btn_flap)
        # setup menu actions
        self.create_action('new', self.menu_handler)
        self.create_action('about', self.menu_handler)
        self.create_action('quit', self.menu_handler)
        self.headerbar.pack_end(self.btn_menu)
        self.main_content.append(self.headerbar)
        self.flap = Adw.Flap()
        self.stack = Gtk.Stack()
        self.page1 = self.add_page('page1', 'ViewStack', self.add_viewswitcher())
        self.page2 = self.add_page('page2', 'Page 2')
        self.page3 = self.add_page('page3', 'Page 3')
        self.page4 = self.add_page('page4', 'Page 4')
        self.stack_switch = Gtk.StackSidebar()
        self.stack_switch.set_stack(self.stack)
        self.flap.set_content(self.stack)
        self.flap.set_separator(Gtk.Separator())
        self.flap.set_flap(self.stack_switch)
        self.main_content.append(self.flap)
        # self.btn_start = Gtk.Button()
        # self.btn_start.set_label("Hallo World, This is the Start Button")
        # self.btn_start.props.halign = Gtk.Align.START
        # self.btn_start.props.valign = Gtk.Align.START
        # self.btn_start.props.vexpand = True
        # self.btn_start.props.hexpand = True

        # self.leaflet.append(self.btn_start)
        # self.btn_end = Gtk.Button()
        # self.btn_end.set_label("Hallo World, This is the End Button")
        # self.btn_end.props.halign = Gtk.Align.END
        # self.btn_end.props.valign = Gtk.Align.END
        # self.btn_end.props.vexpand = True
        # self.btn_end.props.hexpand = True
        # self.leaflet.append(self.btn_end)


    def add_page(self, name, title, widget = None):
        if not widget:
            widget = Gtk.Box()
            lbl = get_label(title)
            widget.append(lbl)
        page = self.stack.add_named(widget, name)
        page.set_title(title)
        return page
    
    def add_viewswitcher(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        view_stack = Adw.ViewStack()
        view_switch = Adw.ViewSwitcher()
        view_switch.set_stack(view_stack)
        view_switch.set_policy(Adw.ViewSwitcherPolicy.WIDE)
        for num in ['1','2','3']:
            box = Gtk.Box()
            title = f'Page {num}'
            name = f'page{num}'
            lbl = get_label(f'This is a ViewStack page  ({num})')
            box.append(lbl)
            page = view_stack.add_named(box, name)
            page.set_title(title)
            page.set_icon_name('media-record-symbolic')
        main_box.append(view_switch)
        main_box.append(view_stack)
        return main_box
        
        
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
