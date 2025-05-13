# Use mamba and environment.yml to create the environment hydrosat if it is not already created
# !/bin/bash
# Usage: ./setup.sh

# Run setup.py
echo "Running setup.py..."
python setup.py

# Setup kernerl for jupyter
echo "Setting up kernel for jupyter..."
python -m ipykernel install --user --name=hydrosat
# TO remove the kernel, run:
# jupyter kernelspec uninstall hydrosat


