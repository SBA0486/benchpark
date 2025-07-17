#!/bin/bash

export BM="saxpy"
export SYS="riken-fugaku"
export WSDIR="$(pwd)/wkspace"

if [ -e "$(find ${WSDIR}/spack/opt/spack/linux-rhel8-a64fx/gcc-8.5.0/python-venv-1.0*/bin -name 'virtualenv')" ]; then
    echo "Python installed."
    exit
fi
if [ -e "$(find ${WSDIR}/spack/opt/spack/linux-rhel8-a64fx/clang-18.1.8/python-venv-1.0-*/bin -name 'python')" ]; then
    echo "Python installed."
    exit
fi

sed -i -e 's"python3.11"python3"g' bin/benchpark
# Get Python version
python_version=$(python3 --version 2>&1)
# Extract major and minor versions
major_version=$(echo "$python_version" | grep -oP 'Python \K[0-9]+' | head -n 1)
minor_version=$(echo "$python_version" | grep -oP 'Python [0-9]+\.\K[0-9]+' | head -n 1)

# Check if Python is 3.8 or newer, else install python 3.10.16
if [[ "$major_version" -ge 3 ]]; then
    if [[ "$major_version" -eq 3 && "$minor_version" -lt 8 ]]; then
        echo "Python version is older than 3.8. Installing python 3.10.16"
        
        # Python install with benchpark's spack
	sed -i -e 's"python3"python3.11"g' bin/benchpark

        . setup-env.sh

        if [ -e "$(find ${WSDIR}/spack/opt/spack/linux-rhel8-a64fx/*/python-venv-1.0*/bin -name 'virtualenv')" ]; then
            echo "Python installed."
        else
            benchpark system init --dest=${SYS}-pytest ${SYS} cluster=rccs_cloud > py_install.log 2>&1
            benchpark experiment init --dest=${BM}-pytest ${BM} +openmp >> py_install.log 2>&1
            benchpark setup ${BM}-pytest ${SYS}-pytest ${WSDIR} >> py_install.log 2>&1
            . ${WSDIR}/setup.sh

            mkdir ${WSDIR}/spack/etc/spack/linux
	    cp ${SYS}-pytest/auxiliary_software_files/packages.yaml ${WSDIR}/spack/etc/spack/linux/

            echo ""
	    echo "Setup finished, installing python" >> py_install.log 2>&1

	    spack install python@3.10.16%gcc >> py_install.log 2>&1
            spack load python

	    echo ""
	    echo "Installing py-pip" >> py_install.log 2>&1

            spack install py-pip%gcc ^python@3.10.16%gcc >> py_install.log 2>&1
            spack load py-pip
            echo ""
            echo "Installing requirements" >> py_install.log 2>&1
	    pip install -r requirements.txt >> py_install.log 2>&1

            rm -r ${SYS}-pytest
            rm -r ${BM}-pytest
	    rm ${WSDIR}/spack/etc/spack/linux/packages.yaml
            sed -i -e 's"python3.11"python3"g' bin/benchpark
            
        fi

     #   python_dir="$(dirname "$(find ${WSDIR}/spack/opt/spack/linux-rhel8-a64fx/gcc-8.5.0/python-venv-1.0*/bin -name 'virtualenv')")"
     #   echo "${python_dir}"
     #   export PATH=${python_dir}:$PATH

    else
        echo "Python version is 3.8 or newer."
    fi
fi
