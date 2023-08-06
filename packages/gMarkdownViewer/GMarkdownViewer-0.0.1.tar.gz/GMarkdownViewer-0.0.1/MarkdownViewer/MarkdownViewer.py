#!/usr/bin/env python3
"""
Author: Ben Knisley [benknisley@gmail.com]
Created: 11 February, 2022

A simple Markdown viewer application.

A Markdown viewer application build using PythonGTK and Webkit.
"""
## Import Python STD Modules
import os
import sys
import textwrap
import pathlib
import urllib
import webbrowser

## Import depend modules
import markdown as md

## Import GUI modules
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, Gdk, Gio, GObject
from gi.repository import WebKit2


class MarkdownViewerApplication(Gtk.Application):
    """  
    """
    def __init__(self):
        """
        """
        ## Set ID and flags, initialize Gtk Application parent.
        app_id = "apps.com.benknisley.MarkdownView"
        flags = Gio.ApplicationFlags.FLAGS_NONE
        Gtk.Application.__init__(self, application_id=app_id, flags=flags)

        ## Initialize the MainWindow instance
        self.window = MainWindow()

        ## Connect activate signal with on_activate slot
        self.connect("activate", self.on_activate)

        ## Show all widgets
        self.window.show_all()

    def on_activate(self, caller):
        """
        """
        self.add_window(self.window)


class MainWindow(Gtk.Window):
    """ 
    The main window of the Markdown viewer application. 

    Contains the Markdown widget, and handles drag and drop operations.
    """
    def __init__(self):
        """ Defines window properties, & adds child widgets. """
        ## Initialize parents: Gtk.Window & Gtk.GObject
        Gtk.Window.__init__(self)
        GObject.GObject.__init__(self)

        ## Set window properties
        self.set_title("MarkDown Viewer")
        self.resize(800, 1000)
        self.set_border_width(0)
        
        ## Enable drag & drop of URIs
        self.drag_dest_set(
            Gtk.DestDefaults.MOTION | 
            Gtk.DestDefaults.HIGHLIGHT | 
            Gtk.DestDefaults.DROP, 
            [Gtk.TargetEntry.new("text/uri-list", 0, 80)], 
            Gdk.DragAction.COPY
        )

        ## Connect drag_data_received signal with d&d slot
        self.connect('drag_data_received', self.on_drag_data_received)


        # Setup a vertical layout box to manage windows top-level layout
        self.layout = Gtk.VBox()
        self.add(self.layout)

        ## Create a MarkdownViewWidget, and add it to windows layout
        self.markdown_view = MarkdownViewWidget()
        self.layout.pack_start(self.markdown_view, True, True, 0)
        
        ## Connect 
        self.markdown_view.connect("markdown-file-loaded", self.markdown_loaded_handler)

        ## Generate a uri from the current directory path
        base_uri = os.path.join(pathlib.Path(os.getcwd()).as_uri(),'')

        ## Find place holder markdown file path
        place_holder_md_path = os.path.join(
            os.path.dirname(__file__), 
            'place_holder.md'
        )

        ## Load place holder markdown
        with open(place_holder_md_path) as f:
            self.markdown_view.set_markdown(f.read(), base_uri)

    def on_drag_data_received(self, caller, context, x, y, selection, target_type, timestamp):
        """ Drag and drop received slot """
        ## Get URIs byte string from selection
        selection_data = selection.get_data().decode("utf-8")

        ## Split into list of individual uri strings
        uri_list = selection_data.split('\r\n')
        uri_list = [uri for uri in uri_list if uri]
        
        ## Get first uri only !! NOTE: Find a way to disable muti-d&d
        uri = uri_list[0]

        ## Convert uri to path
        path = urllib.parse.urlparse(urllib.parse.unquote(uri)).path

        ## Send file to markdown widget
        self.markdown_view.read_file(path)

    def markdown_loaded_handler(self, caller, file_name):
        """ """
        self.set_title(f"{file_name} - Markdown Viewer")


class MarkdownViewWidget(WebKit2.WebView, GObject.GObject):
    """
    A widget to display Markdown.

    Creates a widget to view Markdown by subclassing the Webkit WebView class. 
    Restricts some basic browser functions, and adds methods to implement 
    Markdown viewer.
    """ 
    ## Define signals widget can emit
    __gsignals__ = {
        "markdown-file-loaded": (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (str,)),
    }

    def __init__(self):
        """
        Initializes a MarkdownViewWidget object. A widget to display Markdown.

        Parameters:
            None
        
        Returns:
            None
        """
        WebKit2.WebView.__init__(self)
        GObject.GObject.__init__(self)

        ## Connect navigation policy to slot, to intercept external requests
        self.connect("decide-policy", self.navigation_hander)
        self.connect("context-menu", self.context_menu_handler)
        
        ## Disable drag & drop as it is handled by parent window
        self.drag_dest_unset()

        ## Define css for Markdown view
        self.page_css_js = """
            <style>
                body{
                    background-color:#343434;
                    color: white;
                    font-size: 18pt;
                    margin-left: 10%;
                    margin-right: 10%;
                    padding-bottom: 2em;
                    word-break: break-all;
                }
            </style>
            <script>
                // Disable drag & drop from webkit
                document.addEventListener("dragstart", function(evt) { evt.preventDefault(); });
            </script>
        """

        ## Find path for external HighlightJS file
        highlight_js_path = os.path.join(
            os.path.dirname(__file__), 
            'highlight_js.html')

        ## Load HighlightJS css & js data
        with open(highlight_js_path) as f:
            self.highlight_js = f.read()
        
    def _set_html(self, body_html, base_uri):
        """
        Sets the html to be displayed by the widget.

        ParametersL
            body_html (str): The source html to be displayed by the widget.

            base_uri (str): The uri of the directory where the resources are 
                stored.
            
        Returns:
            None
        """
        ## Generate html for full html document
        full_html = textwrap.dedent(f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <base href="{base_uri}">
                {self.page_css_js}
                {self.highlight_js}
            </head>
            <body>
                {body_html}
            </body>
        </html>
        """)

        ## Load the html into WebView
        self.load_html(full_html, base_uri=base_uri)

    def set_markdown(self, markdown_text, base_uri):
        """
        Set the Markdown displayed by the widget.

        Parameters:
            markdown_text (str): The source of the markdown to display.

            base_uri (str): The uri of the directory where the resources are 
                stored.
        
        Returns:
            None
        """
        ## Generate html from given markdown string, and call set_html
        body_html = md.markdown(markdown_text)
        self._set_html(body_html, base_uri)

    def read_file(self, file_path):
        """
        Opens and displays contents of a Markdown file.

        Parameters:
            file_path (str): The path to the Markdown file to open.
        
        Returns:
            None
        """
        ## Extract file name and base uri from path
        file_name = os.path.basename(file_path)
        base_dir = os.path.dirname(os.path.abspath(file_path))
        base_uri = os.path.join(pathlib.Path(base_dir).as_uri(),'')

        ## Read file and display markdown
        with open(file_path, 'r') as md_file:
            self.set_markdown(md_file.read(), base_uri)
        
        ## Emit file name via markdown-file-loaded signal to listeners
        self.emit("markdown-file-loaded", file_name)

    def navigation_hander(self, caller, policy_decision, decision_type):
        """
        Slot to manage Webkit decide-policy signals. 

        Intercepts navigation requests, opens them in web browser if they are 
        http links, and in self of they are local markdown files.
        """
        ## Get nav URI
        uri = policy_decision.get_request().get_uri()

        ## Get navigation scheme
        nav_scheme = urllib.parse.urlparse(uri).scheme

        ## If nav scheme is http(s)
        if nav_scheme in ('http', 'https'):
            ## Open in external browser
            webbrowser.open(uri, new = 0, autoraise = True)
            
            ## Deny webkit navigation request
            policy_decision.ignore()

        elif nav_scheme == 'file':
            ## Get file extention
            ext = os.path.splitext(urllib.parse.urlparse(uri).path)[1]

            ## If Markdown file, open in self
            if ext == '.md':
                ## Extract path from uri
                path = urllib.parse.urlparse(urllib.parse.unquote(uri)).path

                ## Load new Markdown file
                self.read_file(path)

                ## Deny webkit navigation request
                policy_decision.ignore()

    def context_menu_handler(self, caller, context_menu, event, hit_test):
        """
        """
        ## Loop through each item in the context menu
        for item in context_menu.get_items():
            ## If menu item is anything but copy text, remove it
            if item.get_action().get_label() != "_Copy":
                context_menu.remove(item)


def main(markdown_file=None):
    """
    Create & runs a Markdown Viewer Application instance and can pass a file 
    path to it.

    Parameters:
        Optional:
            markdown_file (str): Path to Markdown file to open.
    
    Returns:
        None
    """
    ## Create an application instance
    app = MarkdownViewerApplication()

    ## Open files with markdown_view widget, if path is given
    if markdown_file:
        app.window.markdown_view.read_file(markdown_file)

    ## Run GTK application loop
    app.run()


## Run main function, if file ran as an executable
if __name__ == "__main__":
    ## Parse cmd args
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        main(file_path)
    else:
        main()
  