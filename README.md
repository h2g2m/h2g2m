# h2g2m 
 
## install venv

    mkdir temp
    cd temp
    wget "http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz"
    tar xvfz virtualenv-1.10.1.tar.gz
    cd ..
    python temp\virtualenv-1.10.1\virtualenv.py py_env
    rm -rf temp


## install app

    ./py_env/bin/easy_install "https://pypi.python.org/packages/source/Y/Yapps2/yapps2-2.1.1-17.1.tar.gz#md5=0651dda9fd07f2c15a8b5e25e0d5eadd"
    ./py_env/bin/python setup.py develop
    ./py_env/bin/populate_h2g2m development.ini
    ./py_env/bin/pserve development.ini


## generate parser

    py_env/Scripts/python.exe parser/yapps2.py parser/h2g2mTeX.g parser/h2g2mTeX.py
    cp parser/h2g2mTeX.py h2g2m/lib/textextmode.py
    py_env/Scripts/python.exe parser/h2g2mTex.py tex parser/test.tex
    py_env/Scripts/python.exe parser/h2g2mTex.py tex parser/test2.tex 
