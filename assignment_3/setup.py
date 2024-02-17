from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(r"C:\Users\wenxu\OneDrive\Documents\VS Codes\DD2358\Assignment III\gauss_seidel_ctype.pyx",
                            compiler_directives={"language_level": "3"}))