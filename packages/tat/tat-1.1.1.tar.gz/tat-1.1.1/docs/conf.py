# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys
import os
import io
import re
import hashlib
from pbr.git import _iter_log_oneline, _iter_changelog, _run_git_command

sys.path.insert(0, os.path.abspath(os.path.join('..', 'src')))

# -- Project information -----------------------------------------------------

project = 'Tomography Analysis Tool'
copyright = '2021, Hugo Haldi'
author = 'Hugo Haldi'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'myst_parser'
]

myst_enable_extensions = [
    'colon_fence'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_material'

html_theme_options = {
    'base_url': 'https://github.com/ShinoYasx/tat/',
    'repo_url': 'https://github.com/ShinoYasx/tat/',
    'repo_name': 'Tomography Analysis Tool',
    # 'google_analytics_account': 'UA-XXXXX',
    'html_minify': True,
    'css_minify': True,
    'nav_title': 'Tomography Analysis Tool',
    'logo_icon': '&#xe869',
    'globaltoc_depth': 2
}

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


def sha256_file(file):
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        sha256.update(f.read())
    return sha256


def generate_changelog(*args, **kwargs):
    changelog = _iter_log_oneline(git_dir=os.path.join('..', '.git'))
    if changelog:
        changelog = _iter_changelog(changelog)
    if not changelog:
        return

    new_changelog = 'changelog.rst'

    new_content = bytearray()
    for _, content in changelog:
        new_content += content.encode('utf-8')

    if os.path.isfile(new_changelog) and hashlib.sha256(new_content).digest() == sha256_file(new_changelog).digest():
        return

    with io.open(new_changelog, "wb") as changelog_file:
        changelog_file.write(new_content)


def generate_authors(*args, **kwargs):
    old_authors = 'AUTHORS.in'
    new_authors = 'authors.md'
    if os.path.isfile(new_authors) and not os.access(new_authors, os.W_OK):
        # If there's already an AUTHORS file and it's not writable, just use it
        return

    ignore_emails = '((jenkins|zuul)@review|infra@lists|jenkins@openstack)'
    git_dir = os.path.join('..', '.git')
    authors = []

    # don't include jenkins email address in AUTHORS file
    git_log_cmd = ['log', '--format=%aN <%aE>']
    authors += _run_git_command(git_log_cmd, git_dir).split('\n')
    authors = [a for a in authors if not re.search(ignore_emails, a)]

    # get all co-authors from commit messages
    co_authors_out = _run_git_command('log', git_dir)
    co_authors = re.findall('Co-authored-by:.+', co_authors_out,
                            re.MULTILINE)
    co_authors = [signed.split(":", 1)[1].strip()
                  for signed in co_authors if signed]

    authors += co_authors
    authors = sorted(set(authors))

    new_authors_str = bytearray()

    if os.path.exists(old_authors):
        with open(old_authors, "rb") as old_authors_fh:
            new_authors_str += old_authors_fh.read()
    new_authors_str += (os.linesep.join(authors) + os.linesep).encode('utf-8')

    if os.path.isfile(new_authors) and hashlib.sha256(new_authors_str).digest() == sha256_file(new_authors).digest():
        return

    with open(new_authors, 'wb') as f:
        f.write(new_authors_str)


def on_builder_inited(*args, **kwargs):
    generate_changelog()
    # generate_authors()


def setup(app):
    app.connect('builder-inited', on_builder_inited)
