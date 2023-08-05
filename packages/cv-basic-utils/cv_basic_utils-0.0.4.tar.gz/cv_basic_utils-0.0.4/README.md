# CV BASIC UTILS
A package for reusing functions that repeat during computer vision and machine learning works

[![Tests](https://github.com/jerinka/cv_basic_utils/actions/workflows/main.yml/badge.svg)](https://github.com/jerinka/cv_basic_utils/actions/workflows/main.yml)

[![pypi](https://github.com/jerinka/cv_basic_utils/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jerinka/cv_basic_utils/actions/workflows/python-publish.yml)

# Install from Pypi
```pip install cv_basic_utils```

# Local install
```git clone https://github.com/jerinka/cv_basic_utils```\
```pip3 install -e cv_basic_utils```

# Test and Coverage
```coverage run --source=cv_basic_utils/ -m pytest -v test/ && coverage report -m```\
```coverage html -d coverage_html```

# build
```pip install wheel```\
```python setup.py sdist bdist_wheel```

# testpypi
```pip install twine```\
```twine upload --repository testpypi dist/* ```\
```pip install -i https://test.pypi.org/simple/ cv_basic_utils ```

# pypi
```twine upload dist/*```\
```pip install -U cv_basic_utils```

# Quick usage
```import cv_basic_utils as pk1```\
```pk1.subpackage1.moduleA.fun_a()```


# Reference
[https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56)









