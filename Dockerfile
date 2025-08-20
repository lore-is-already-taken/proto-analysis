# Use the official Jupyter scipy-notebook image.
# It includes JupyterLab, Python, numpy, pandas, and matplotlib.
FROM jupyter/scipy-notebook:latest

# Install the Python Language Server with all optional plugins.
# This enables features like code completion, linting, and formatting.
RUN pip install --no-cache-dir 'python-lsp-server[all]'
RUN pip install --no-cache-dir 'tabulate'
