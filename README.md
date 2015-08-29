# h2g2m
[![Travis-CI](https://travis-ci.org/h2g2m/h2g2m.svg?branch=master)](https://travis-ci.org/h2g2m/h2g2m)
[![Coverage Status](https://coveralls.io/repos/h2g2m/h2g2m/badge.svg?branch=master&service=github)](https://coveralls.io/github/h2g2m/h2g2m?branch=master)
 
## install venv

    mkdir temp
    cd temp
    wget "http://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.0.tar.gz"
    tar xvfz virtualenv-13.1.0.tar.gz
    cd ..
    python temp\virtualenv-13.1.0\virtualenv.py venv
    rm -rf temp


## install app

    venv\Scripts\easy_install.exe "https://pypi.python.org/packages/source/Y/Yapps2/yapps2-2.1.1-17.1.tar.gz#md5=0651dda9fd07f2c15a8b5e25e0d5eadd"
    venv\Scripts\python.exe setup.py develop
    venv\Scripts\populate_h2g2m.exe development.ini
    venv\Scripts\pserve.exe development.ini

## generate parser

    venv/Scripts/python.exe parser/yapps2.py parser/h2g2mTeX.g parser/h2g2mTeX.py
    cp parser/h2g2mTeX.py h2g2m/lib/textextmode.py
    venv/Scripts/python.exe parser/h2g2mTex.py tex parser/test.tex
    venv/Scripts/python.exe parser/h2g2mTex.py tex parser/test2.tex 
