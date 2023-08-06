from typing import Optional, Final, List


class LayerData:
    """
    Container for layer data.
    """

    def __init__(self, image_path: Optional[str] = None, array_path: Optional[str] = None, is_merger=False,
                 layer_index: Optional[int] = None, parent_layers: Optional[List[int]] = None):
        """
        Creates a LayerData.

        :type image_path: str, optional
        :type array_path: str, optional
        :param bool is_merger: Tells if the layer a merger of multiple layers or not.
        :param layer_index: Index of the layer if it is not a merger.
        :type layer_index: int, optional
        :param parent_layers: List of the parent layers if the layer is a merger.
        :type parent_layers: list of int, optional
        """
        if is_merger:
            assert parent_layers is not None and layer_index is None
        else:
            assert parent_layers is None and layer_index is not None
        self.image_path: Final[str] = image_path
        self.array_path: Final[str] = array_path
        self.is_merger: Final[bool] = is_merger
        self.parent_layers: Final[Optional[List[int]]] = parent_layers
        self.layer_index: Final[Optional[int]] = layer_index

    def name(self) -> str:
        """
        :return: Name based on the index.
        :rtype: str
        """
        if self.is_merger:
            assert self.parent_layers is not None
            return "m " + self.indices2str(self.parent_layers)
        assert self.layer_index is not None
        return str(self.layer_index)

    @staticmethod
    def indices2str(indices: List[int]) -> str:
        """
        Creates a string from a list of indices, each index separated by a `+`.

        :type indices: list of int
        :rtype: str
        """
        indices_str = ""
        for i in indices:
            indices_str += str(i) if i == indices[0] else f"+{str(i)}"
        return indices_str
