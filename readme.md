# Image Punch Chart

This app shows photographers a punch chart of when they took pictures during a gig. It helps to analyze shooting breaks or identify lost or forgotten sd cards.

## Usage

Mac users download and open the .app file in the dist directory

## Build

The app is build with py2app out of a virtual environment. It needs a `setup.py` file generated with `py2applet --make-setup punch-chart.py`. A good explanation can be found [here](https://www.metachris.com/2015/11/create-standalone-mac-os-x-applications-with-python-and-py2app/). These are the build steps:
1. `virtualenv venv` (if not done yet: `pip install virtualenv`)
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`
4. Only needed if previously built: `rm -rf build dist`
5. `python setup.py py2app`

## During development

it is easier and quicker to not always build the app during development but rather use aliases. Therefore py2app has an alias mode. Run these commands to build the app in alias mode.

    rm -rf build dist
    python setup.py py2app -A