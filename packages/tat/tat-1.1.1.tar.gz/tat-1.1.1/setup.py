from typing import List, Tuple

import setuptools

data_files: List[Tuple[str, List[str]]] = []

setuptools.setup(
    setup_requires=['pbr'],
    pbr=True,
    data_files=data_files
)
