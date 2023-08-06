---
title: TAT Documentation
summary: Tomography Analysis Tool Documentation
authors:
    - Hugo Haldi
date: 2021-05-12
---

# Welcome to TAT

Welcome to the documentation of the TAT GUI. TAT (for Tomography Analysis Tool) is a graphical interface letting you generate clusters for tomography images using the k-means method and manipulate clusters.

## Getting started

If you are a user, you can follow the [installation guide](user-guide/installation.md) and see the [user manual](user-guide/manual.md).

### Quick start

TAT needs Python >= 3.8 and 3.8.1 on Windows.

TAT is available in PyPI, thus you can install it with `pip` :

```shell
pip install tat
```

And then you can run the application as a Python module :

```shell
python -m tat
```

Or directly as a program if Python scripts are in path :

```shell
tat
```

And if you are using Windows, you can start the executable file created in the start menu under the name of `tat`.

```{toctree}
:caption: User Guide
:hidden:
Installation <user-guide/installation>
Interface manual <user-guide/manual>
```

```{toctree}
:caption: Developper Guide
:hidden:
References <dev-guide/references>
```

```{toctree}
:caption: About
:hidden:
license
Release Notes <changelog>
```
