#!/bin/env python

import os
import sys
from typing import List, Tuple


class RstGenerator:
    def __init__(self, package_name) -> None:
        self.package_name = package_name

    def generate_class_rst(self, module_name: str, class_name: str) -> str:
        s = class_name + os.linesep + len(class_name) * '=' + 2 * os.linesep + \
            f'.. autoclass:: {self.package_name}.{module_name}.{class_name}' + \
            os.linesep + '    :members:' + os.linesep + \
            '    :special-members: __init__' + os.linesep
        return s


if __name__ == "__main__":
    modules_classes: List[Tuple[str, str]] = [
        ('checkable_image_entry', 'CheckableImageEntry'),
        ('cluster_editor', 'ClusterEditor'),
        ('cluster_image_entry', 'ClusterImageEntry'),
        ('clustering', 'Tat'),
        ('image_entry', 'ImageEntry'),
        ('layer_data', 'LayerData'),
        ('layer_image_entry', 'LayerImageEntry'),
        ('main_window', 'MainWindow'),
        ('preview_window', 'PreviewWindow'),
        ('progress_window', 'ProgressWindow')
    ]

    generator = RstGenerator('tat')
    for module_name, class_name in modules_classes:
        with open(os.path.join('source', 'dev-guide', 'classes', f'{module_name}.rst'), 'wb') as file:
            file.write(generator.generate_class_rst(
                module_name, class_name).encode('utf-8'))
