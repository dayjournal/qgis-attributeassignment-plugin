from typing import Any, Optional

from qgis.core import (
    QgsCoordinateTransform,
    QgsFeatureRequest,
    QgsMapLayer,
    QgsProject,
    QgsRectangle,
)
from qgis.gui import QgsMapCanvas, QgsMapMouseEvent, QgsMapTool
from qgis.PyQt.QtWidgets import QMessageBox

from ..ui.main.main import MainDialog


class MapClickHandler(QgsMapTool):
    """
    Handles map click events for assigning attribute values to features.

    This tool allows users to click on features in the map canvas
    and assign a specified value to a selected field.
    """

    CLICK_TOLERANCE = 0.00001

    def __init__(
        self,
        iface: Any,
        canvas: QgsMapCanvas,
        dialog: MainDialog,
    ) -> None:
        """
        Initializes the MapClickHandler.

        Args:
            iface: Reference to the QGIS interface.
            canvas (QgsMapCanvas): The map canvas to handle clicks on.
            dialog (MainDialog): The main dialog containing layer/field selection.
        """
        super().__init__(canvas)
        self.iface = iface
        self.canvas = canvas
        self.dialog = dialog

    def canvasPressEvent(self, event: QgsMapMouseEvent) -> None:
        """
        Handles mouse press events on the map canvas.

        When a user clicks on the map, this method:
        1. Validates the selected layer is a vector layer
        2. Transforms the click coordinates to the layer's CRS
        3. Finds features at the click location
        4. Assigns the specified value to the selected field

        Args:
            event (QgsMapMouseEvent): The mouse event containing click information.
        """
        layer = self.dialog.mMapLayerComboBox.currentLayer()
        field_name = self.dialog.mFieldComboBox.currentText()
        value = self.get_value()

        if not self.validate_layer(layer):
            return

        feature_id, field_index = self.find_feature_at_point(
            layer, event.mapPoint(), field_name
        )

        if feature_id is not None:
            layer.startEditing()
            layer.changeAttributeValue(feature_id, field_index, value)
            layer.triggerRepaint()
        else:
            QMessageBox.warning(None, "Error", "No feature found at this location.")

    def get_value(self) -> Optional[Any]:
        """
        Gets the current value from the editor widget.

        Returns:
            Optional[Any]: The value from the widget, or None if no wrapper exists.
        """
        if self.dialog.wrapper is not None:
            return self.dialog.wrapper.value()
        return None

    def validate_layer(self, layer: Any) -> bool:
        """
        Validates that the layer is a vector layer.

        Args:
            layer: The layer to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not layer or layer.type() != QgsMapLayer.VectorLayer:
            QMessageBox.warning(None, "Error", "This is not a vector layer.")
            return False
        return True

    def find_feature_at_point(
        self,
        layer: Any,
        map_point: Any,
        field_name: str,
    ) -> tuple[Optional[int], Optional[int]]:
        """
        Finds a feature at the specified map point.

        Args:
            layer: The vector layer to search.
            map_point: The point in map coordinates.
            field_name (str): The name of the field to get the index for.

        Returns:
            tuple[Optional[int], Optional[int]]: A tuple of (feature_id, field_index),
                or (None, None) if no feature found.
        """
        # Transform coordinates to layer CRS
        layer_crs = layer.crs()
        dest_crs = self.canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(dest_crs, layer_crs, QgsProject.instance())
        transformed_point = transform.transform(map_point)

        # Create search rectangle
        rect = QgsRectangle(
            transformed_point.x() - self.CLICK_TOLERANCE,
            transformed_point.y() - self.CLICK_TOLERANCE,
            transformed_point.x() + self.CLICK_TOLERANCE,
            transformed_point.y() + self.CLICK_TOLERANCE,
        )

        # Find features
        request = QgsFeatureRequest().setFilterRect(rect)
        feature_id = None
        field_index = None

        for feature in layer.getFeatures(request):
            field_index = feature.fieldNameIndex(field_name)
            feature_id = feature.id()

        return feature_id, field_index
