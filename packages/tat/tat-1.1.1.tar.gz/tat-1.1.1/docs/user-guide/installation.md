# Installation of TAT

## Via pip

### Requirements

During this section, we will assume that you have Python installed. If it is not the case, you can install it by downloading it on the [official Python website](https://www.python.org/downloads/) or using your distribution package manager if you are on Linux. Python 3.8 or superior is required.

### Installation

In a command prompt, write the following command to install the `tat` package add all its dependencies using the `pip` tool :

```shell
pip install tat
```

:::{note}
If you are using windows, it may happends that `pip` is not in your path. So you will need to add `python -m pip` to install the package, e.g.
    ```shell
    python -m pip install tat
    ```
:::

## Via sources

### Getting the sources

As this project is open source, you can directly download the sources on the [Git repo](https://github.com/ShinoYasx/tat). You can either download the sources as a zip on the website [https://github.com/ShinoYasx/tat](https://github.com/ShinoYasx/tat), or use [Git](https://git-scm.com) :

```shell
git clone https://github.com/ShinoYasx/tat tat
cd tat/
```

### Installing from sources

Once you download the sources, there will be an executable than you can run in the project root, called `setup.py`. Run this file will install TAT in your current python environment :

```shell
python setup.py install
```

## Executing the application

### Via the command line interface

TAT is a module and has a startup script, so you can run it with the following command :

```shell
python -m tat
```

Or if the Python scripts are in your path :

```shell
tat
```

### Via a desktop environment

#### Windows

If you are on windows, an executable file should be available in the start menu, to find it simply type `tat` in the search bar. Click `tat.exe` to open the application.

#### Linux

If you are on Linux, there will be no default desktop executable. You can however download [this file](https://github.com/ShinoYasx/tat/blob/master/data/ch.unige.tat.desktop) and put it into `~/.local/share/applications`, or with a one-liner bash command :

```shell
curl --create-dirs -O --output-dir ~/.local/share/applications/ https://raw.githubusercontent.com/ShinoYasx/tat/master/data/ch.unige.tat.desktop
```
