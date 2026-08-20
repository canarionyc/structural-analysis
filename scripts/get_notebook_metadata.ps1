python -c "import json; f=open('notebooks/ipympl_testing.ipynb'); d=json.load(f); f.close(); print(d)"
python -c "import matplotlib; print(matplotlib.get_backend())"
rem location of the matplotlib configuration file.
python -c "import matplotlib; print(matplotlib.matplotlib_fname())"

Select-String "backend" C:\dev\matplotlibrc

python -c "import ipympl; print(ipympl.__version__)"