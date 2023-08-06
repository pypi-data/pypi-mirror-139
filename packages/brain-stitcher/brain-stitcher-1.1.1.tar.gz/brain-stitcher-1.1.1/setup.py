from setuptools import setup, find_packages

##python3 setup.py sdist bdist_wheel
##twine upload dist/*
VERSION = '1.1.1'
DESCRIPTION = 'Stitcher - mesh builder'
LONG_DESCRIPTION = ''' Stitcher package is a 3D mesh builder

It was developed by metaBIO lab member Heitor Gessner as part of his master thesis.
The main usage is for recreating brain models from rare species, i.e., especies with low number of spiciements.

    It provides 3 classes:
        - Points()
        - Perimeters()
        - Surface()

    Each Periemeter is a collection of Points. Each Surface is a collection of Perimeters.
    For the points in points, it is expected to have a 3D coordinate reference for each point that delimits a plane contour.
    The contours are made by manual or automatic segmentation, in the case of brains. This can be done in softwares such as ImageJ, Horos or Osirix - and than exported as a json file.

Version 1.1:
    -New super resolution method using Fourier Transform
    -Fixed fix_intersection() method from Perimeter() to properly handle rare parallel lines case
    -Example on how to use will come on version 1.2 with some results

'''
setup(
        name="brain-stitcher",
        version=VERSION,
        author="Heitor Gessner",
        author_email="<lab.metabio@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        python_requires='>=3.0, <4',
        install_requires=["numpy"],
        keywords=['mesh', 'Sticher'],
        classifiers= [
            'Development Status :: 4 - Beta',
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix"
        ],
        project_urls={
        'Source':'https://github.com/labmetabio/Stitcher'
    }
)
