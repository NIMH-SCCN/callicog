# WIP:

Done:
- try uninstalling wxPython OS dependencies and reinstalling
- read pypa github issue, some users reporting similar install problems; [popular replies][pye2] [suggest][pye1] it could be due to Python being built without all recommended dependency libraries installed
- install all python deps and rebuild

To-do:
- try uninstalling and reinstalling wxPython OS dependencies
- try installing all Python dependencies recommended by pyenv
- try rebuilding Python 3.11.8 (the version wxPython build at first appeared to succeed with) with deps installed
- re-try [building wxPython][wxp1]

Failing that:
- read wxPython forums
- try uninstalling libwebkit2gtk and install libwebkitgtk from an archive package repository
- try installing PsychoPy using conda
- try fresh reinstall of Debian
- post question to PsychoPy forums


## Checklist

- apt	install pyenv
- apt	install Python build dependencies
- pyenv	build Python 3.11.8
    - !!! NEEDS --enable-shared !!!
- apt	install wxPython build dependencies
- pyenv	set local python
- pyenv	create virtualenv
- pyenv	activate virtualenv
- pip	install


# Install Python version with pyenv:

## ATTENTION!!
You *MUST* first install Python dependencies!!! Pyenv will appear to successfully build Python without error or warning (unless run at verbosity level `-vv`). Some package installations downstream then fail with an error that is difficult to trace!

```
# Install Python build dependencies, see:
#
#   https://github.com/pyenv/pyenv/wiki#suggested-build-environment
#
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

## ATTENTION, critical instruction (2 of 2)

Python MUST be built with the `--enable-shared` argument for wxPython:

```sh
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.11.8
```

# Install wxPython

Follow wxPython [build instructions][wxp1].

## Install wxPython dependencies

See dependencies listed on [wxWidgets GitHub README][wxp3]:

> On Ubuntu the following development packages and their dependencies should be installed in order to build Phoenix. Other debian-like distros will probably also have these or similarly named packages available, or newer versions of Ubuntu might have evolved somewhat and require changes from this list. Extrapolate other package names accordingly for other linux distributions or other unixes.
> 
>     dpkg-dev
>     build-essential
>     python3-dev
>     freeglut3-dev
>     libgl1-mesa-dev
>     libglu1-mesa-dev
>     libgstreamer-plugins-base1.0-dev
>     libgtk-3-dev
>     libjpeg-dev
>     libnotify-dev
>     libpng-dev
>     libsdl2-dev
>     libsm-dev
>     libtiff-dev
>     libwebkit2gtk-4.0-dev
>     libxtst-dev
> 
> If you are building for GTK2 then you'll also need these packages and their dependencies:
> 
>     libgtk2.0-dev
>     libwebkitgtk-dev
> 
> If You use a custom built python in a non standard location, You need to compile python with the --enable-shared option.


```sh
sudo apt install dpkg-dev build-essential python3-dev freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev \
libgstreamer-plugins-base1.0-dev libgtk-3-dev libjpeg-dev libnotify-dev libpng-dev libsdl2-dev libsm-dev libtiff-dev \
libwebkit2gtk-4.0-dev libxtst-dev libgtk2.0-dev libwebkit2gtk-4.0-dev
```

------------------------

# Install CalliCog deps:
```
pip install --upgrade Pillow && \
pip install pyserial numpy && \
pip install matplotlib && \
pip install pyqt5==5.14 && \
pip install psychopy --no-deps && \
pip install pyyaml requests freetype-py pandas python-bidi pyglet \
json-tricks scipy packaging future imageio && \
pip install -U pip && \
pip install -U six wheel setuptools
```


# links
http://test.wxpython.org/pages/downloads/index.html


### Python MUST

> ### How to build CPython with `--enable-shared`
> 
> Some of 3rd party tool like [PyInstaller](https://github.com/pyinstaller/pyinstaller) might require CPython installation built with `--enable-shared`. You can build CPython with shared library as follows.
> 
> ```sh
> $ env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.5.0
> ```
> 
> Since pyenv (precisely, python-build) will build CPython with configuring RPATH, you don't have to set `LD_LIBRARY_PATH` to specify library path on GNU/Linux.
> 
> ### How to build CPython for maximum performance
> 
> Building CPython with `--enable-optimizations` will result in a faster interpreter at the cost of significantly longer build times.
> Most notably, this enables PGO (profile guided optimization). While your mileage may vary, it is common for performance improvement from this to be in the ballpark of 30%.
> ```sh
> env PYTHON_CONFIGURE_OPTS='--enable-optimizations --with-lto' PYTHON_CFLAGS='-march=native -mtune=native' pyenv install 3.6.0
> ```
> 
> You can also customize the task used for profile guided optimization by setting the `PROFILE_TASK` environment variable, for instance, `PROFILE_TASK='-m test.regrtest --pgo -j0'` will run much faster than the default task.


env PYTHON_CONFIGURE_OPTS='--enable-shared --enable-optimizations --with-lto' PYTHON_CFLAGS='-march=native -mtune=native' pyenv install 3.10.14


-----


[wxp1]: https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip
    "Building wxPython wheel for Linux with Pip"
[wxp2]: http://test.wxpython.org/pages/downloads/index.html
    "Installing wxPython for Linux (didn't work for me)"
[wxp3]: https://github.com/wxWidgets/Phoenix/blob/master/README.rst
    "wxWidgets Linux build dependencies"
[pye1]: https://github.com/pypa/packaging-problems/issues/573#issuecomment-1040587425
    "pypa: 'setuptools not available in build environment' helpful reply 1"
[pye2]: https://github.com/pypa/packaging-problems/issues/573#issuecomment-1057825325
    "pypa: 'setuptools not available in build environment' helpful reply 2"



-----

Trying with system python
```sh
sudo apt install python3-venv
```

Abortive attempt with pyenv
```sh
sccn@ccpc04:~$ pyenv uninstall 3.11.8
pyenv: remove /home/sccn/.pyenv/versions/3.11.8? [y|N] y
pyenv-virtualenv: remove /home/sccn/.pyenv/versions/3.11.8/envs/callicog? (y/N) y
pyenv: 3.11.8 uninstalled
sccn@ccpc04:~$ env PYTHON_CONFIGURE_OPTS='--enable-shared' pyenv install 3.11.8
Installing Python-3.11.8...
Installed Python-3.11.8 to /home/sccn/.pyenv/versions/3.11.8
sccn@ccpc04:~$ which python
/home/sccn/.pyenv/shims/python
sccn@ccpc04:~$ pyenv local 3.11.8
sccn@ccpc04:~$ python --version
Python 3.11.8
sccn@ccpc04:~$ which python3
/home/sccn/.pyenv/shims/python3
sccn@ccpc04:~$ python3 --version
Python 3.11.8
sccn@ccpc04:~$ pyenv virtualenv callicog
sccn@ccpc04:~$ pyenv activate callicog
```
