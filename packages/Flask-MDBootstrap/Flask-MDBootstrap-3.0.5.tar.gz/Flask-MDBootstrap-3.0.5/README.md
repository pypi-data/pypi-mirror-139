# Flask-MDBootstrap


Flask-MDBootstrap packages [MDB](https://mdbootstrap.com/) into an extension that mostly consists
of a blueprint named 'mdbootstrap'. It can also create links to serve MATERIAL DESIGN FOR BOOTSTRAP
from a CDN and works with no boilerplate code in your application.

## Installation

Installation using pip:

    pip install Flask-MDBootstrap
    

## Compatibility

This package is compatible Python versions 2.7, 3.4, 3.5 and 3.6.

## Usage

Here is an example:

    from flask_mdbootstrap import MDBootstrap
    
    [...]
    
    MDBootstrap(app)

This makes some new templates available, containing blank pages that include all
bootstrap resources, and have predefined blocks where you can put your content.
    


