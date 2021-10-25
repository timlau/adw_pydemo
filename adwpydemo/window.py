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


@Gtk.Template(resource_path=f'{Constants.PATHID}/ui/mainwindow.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    main_content = Gtk.Template.Child()
    app_menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Adw.ApplicationWindow.__init__(self, **kwargs)
        self.style_manager = Adw.StyleManager().get_default()
        # print(dir(self.style_manager))
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
        self.btn_flap.set_tooltip_text("Show/Hide Sidebar")
        self.headerbar.pack_start(self.btn_flap)
        # Light/dark switcher
        btn = Gtk.Button()
        btn.props.icon_name = 'weather-clear-symbolic'
        btn.set_tooltip_text('Switch Light/Dark theme')
        btn.connect('clicked', self.on_color_switch)
        self.headerbar.pack_start(btn)
        # setup menu actions
        self.create_action('new', self.menu_handler)
        self.create_action('about', self.menu_handler)
        self.create_action('quit', self.menu_handler)
        self.headerbar.pack_end(self.btn_menu)
        self.main_content.append(self.headerbar)
        self.flap = Adw.Flap()
        self.stack = Gtk.Stack()
        self.page1 = self.add_page(
            'page1', 'ViewStack', self.add_viewswitcher())
        self.page2 = self.add_page('page2', 'Leaflet', self.add_leaflet())
        self.page3 = self.add_page('page3', 'Preferences', self.add_listbox())
        # self.page4 = self.add_page('page4', 'Page 4')
        self.stack_switch = Gtk.StackSidebar()
        self.stack_switch.set_stack(self.stack)
        self.flap.set_content(self.stack)
        self.flap.set_separator(Gtk.Separator())
        self.flap.set_flap(self.stack_switch)
        self.main_content.append(self.flap)

    def add_page(self, name, title, widget=None):
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
        for num in ['1', '2', '3']:
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            title = f'Page {num}'
            name = f'page{num}'
            box.append(Gtk.Separator())
            lbl = get_label_top('<b>⇧ This is a ViewSwitcher</b>')
            box.append(lbl)
            lbl = get_label(f'This is a ViewStack page  ({num})')
            box.append(lbl)
            lbl = get_label_bottom('<b>This is a ViewSwitcherBar ⇩</b>')
            box.append(lbl)
            page = view_stack.add_named(box, name)
            page.set_title(title)
            page.set_icon_name('media-record-symbolic')
        main_box.append(view_switch)
        main_box.append(view_stack)
        view_switchbar = Adw.ViewSwitcherBar()
        view_switchbar.set_stack(view_stack)
        view_switchbar.set_reveal(True)
        main_box.append(view_switchbar)
        return main_box

    def add_leaflet(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        set_margin(box,10)
        btn = Gtk.Button()
        btn.set_icon_name('media-seek-forward-symbolic')
        btn.props.halign = Gtk.Align.START
        btn.props.valign = Gtk.Align.START
        btn.props.vexpand = False
        btn.props.hexpand = False
        btn.connect('clicked', self.on_leaflet_forward)
        box.append(btn)
        
        btn = Gtk.Button()
        btn.set_icon_name('media-seek-backward-symbolic')
        btn.props.halign = Gtk.Align.END
        btn.props.valign = Gtk.Align.START
        btn.props.vexpand = False
        btn.props.hexpand = True
        btn.connect('clicked', self.on_leaflet_back)
        box.append(btn)
        main_box.append(box)
        main_box.append(Gtk.Separator())
        self.leaflet = Adw.Leaflet()
        btn = Gtk.Button()
        btn.set_label("This is an Left/Start Button")
        btn.props.halign = Gtk.Align.START
        btn.props.valign = Gtk.Align.START
        btn.props.vexpand = True
        btn.props.hexpand = True
        set_margin(btn,10)
        self.leaflet.append(btn)
        btn = Gtk.Button()
        btn.set_label("This is a Right/End Button")
        btn.props.halign = Gtk.Align.END
        btn.props.valign = Gtk.Align.END
        btn.props.vexpand = True
        btn.props.hexpand = True
        set_margin(btn,10)
        self.leaflet.append(btn)
        main_box.append(self.leaflet)
        return main_box

    def add_listbox(self):
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
            row.set_subtitle("This is an action, named {title}")
            row.set_icon_name('find-location-symbolic')
            switch = Gtk.Switch()
            switch.props.halign = Gtk.Align.CENTER
            switch.props.valign = Gtk.Align.CENTER
            switch.props.hexpand = False
            switch.props.vexpand = False
            switch.set_active(x % 2 == 0)
            row.add_suffix(switch)
            group.add(row)
        return page
    
    def on_color_switch(self, widget):
        if self.style_manager.get_dark():
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
    
    def on_leaflet_forward(self, widget):
        if self.leaflet.get_folded():
            self.leaflet.navigate(Adw.NavigationDirection.FORWARD)
        
    def on_leaflet_back(self, widget):
        if self.leaflet.get_folded():
            self.leaflet.navigate(Adw.NavigationDirection.BACK)

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
