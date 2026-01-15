import os
from typing import Optional

from PyQt5.QtWidgets import QDialog, QHBoxLayout
from qgis.gui import QgsEditorWidgetWrapper, QgsGui
from qgis.PyQt import uic


class MainDialog(QDialog):
    """
    Main dialog for the Attribute Assignment plugin.
    """

    UI_PATH = os.path.join(os.path.dirname(__file__), "main.ui")

    def __init__(self) -> None:
        """
        Initializes the main dialog by loading the UI components
        and setting up signal connections.
        """
        super().__init__()
        self.ui = uic.loadUi(self.UI_PATH, self)
        self.mMapLayerComboBox.layerChanged.connect(self.mFieldComboBox.setLayer)
        self.mFieldComboBox.fieldChanged.connect(self.on_field_changed)
        self.value_layout = QHBoxLayout()
        self.value_layout.setContentsMargins(0, 0, 0, 0)
        self.mValuePlaceholder.setLayout(self.value_layout)
        self.wrapper: Optional[QgsEditorWidgetWrapper] = None
        self.widget = None

    def on_field_changed(self, field_name: str) -> None:
        """
        Handles the field change event.

        Creates an appropriate editor widget for the selected field type.

        Args:
            field_name (str): The name of the selected field.
        """
        reg = QgsGui.editorWidgetRegistry()

        if self.widget:
            self.value_layout.removeWidget(self.widget)
            self.widget.deleteLater()
            self.widget = None

        if field_name:
            layer = self.mMapLayerComboBox.currentLayer()
            if layer:
                field_index = layer.fields().indexFromName(field_name)
                self.wrapper = reg.create(
                    layer, field_index, None, self.mValuePlaceholder
                )
                self.widget = self.wrapper.widget()
                self.value_layout.addWidget(self.widget)
        else:
            self.wrapper = None
