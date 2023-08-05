from browser import document
from pyfyre.globals import Globals

def runApp(app, mount="app-mount"):
    """This is the main entry point of your app. You must call this
    with an argument object that inherits [UsesState] or just a simple widget.

    Parameters
    ----------
    app : UsesState (Positional)
        This is what the app will render.
    mount : str
        Where the app will mount on the index.html. This is a provided
        id of a `div` element.
    """

    body = document.getElementById(mount)
    body.innerHTML = ""
    body.appendChild(app.dom())

    Globals.__PARENT__ = app