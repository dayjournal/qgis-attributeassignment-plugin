import os
from typing import Callable, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QWidget

from .ui.main.main import MainDialog
from .utils.click_handler import MapClickHandler


class AttributeAssignment:
    """
    Manages the plugin interface within the QGIS environment,
    including toolbar actions and dialog display.
    """

    PLUGIN_NAME = "Attribute Assignment"

    def __init__(self, iface) -> None:
        """
        Initializes the plugin interface.

        Args:
            iface: Reference to the QGIS interface.
        """
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.main_window = iface.mainWindow()
        self.plugin_directory = os.path.dirname(__file__)
        self.actions = []
        self.toolbar = iface.addToolBar(self.PLUGIN_NAME)
        self.toolbar.setObjectName(self.PLUGIN_NAME)
        self.dialog = MainDialog()
        self.dialog.hide()
        self.click_handler: Optional[MapClickHandler] = None

    def add_action(
        self,
        icon_path: str,
        text: str,
        callback: Callable,
        enabled_flag: bool = True,
        add_to_menu: bool = True,
        add_to_toolbar: bool = True,
        status_tip: Optional[str] = None,
        whats_this: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ) -> QAction:
        """
        Adds an action to the plugin menu and toolbar.

        Args:
            icon_path (str): Path to the action icon.
            text (str): Display text for the action.
            callback (Callable): Function to call when action is triggered.
            enabled_flag (bool): Whether the action is enabled by default.
            add_to_menu (bool): Whether to add the action to the menu.
            add_to_toolbar (bool): Whether to add the action to the toolbar.
            status_tip (Optional[str]): Text shown in status bar on hover.
            whats_this (Optional[str]): Extended description of the action.
            parent (Optional[QWidget]): Parent widget for the action.

        Returns:
            QAction: The created action.
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_menu:
            self.iface.addPluginToMenu(self.PLUGIN_NAME, action)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        self.actions.append(action)
        return action

    def initGui(self) -> None:
        """
        Initializes the GUI components.
        """
        icon_path = os.path.join(self.plugin_directory, "ui", "icon.png")
        self.add_action(
            icon_path=icon_path,
            text=self.PLUGIN_NAME,
            callback=self.run,
            parent=self.main_window,
        )

    def unload(self) -> None:
        """
        Cleans up the plugin interface by removing actions and toolbar.
        """
        for action in self.actions:
            self.iface.removePluginMenu(self.PLUGIN_NAME, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self) -> None:
        """
        Runs the plugin. Shows the dialog and activates the map click tool.
        """
        self.dialog.setWindowFlags(Qt.WindowStaysOnTopHint)  # type: ignore
        self.dialog.show()
        current_layer = self.iface.layerTreeView().currentLayer()
        self.dialog.mMapLayerComboBox.setLayer(current_layer)
        self.click_handler = MapClickHandler(
            self.iface,
            self.canvas,
            self.dialog,
        )
        self.canvas.setMapTool(self.click_handler)
