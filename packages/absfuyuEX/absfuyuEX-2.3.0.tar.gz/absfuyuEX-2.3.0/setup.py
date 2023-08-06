"""
SETUP FILE
----------
"""

import setuptools


setuptools.setup(
    name="absfuyuEX",
    keywords="utilities",
    install_requires=[
        "absfuyu[extra]>=1.2",
        "opencv-python","scikit-learn",
        "click"
    ],
    package_data={"": ["pkg_data/*"]},
)


# TO BUILD:
# python -m build
# python setup.py sdist bdist_wheel

# TO UPLOAD:
# twine upload dist/*