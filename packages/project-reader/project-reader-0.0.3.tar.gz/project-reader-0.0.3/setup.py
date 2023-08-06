import setuptools


with open('README.rst', 'r', encoding='utf-8') as f:
    main_description = f.read()

setuptools.setup(
    name='project-reader',
    version='0.0.3',
    author='Muremwa',
    author_email='danmburu254@gmail.com',
    url='https://github.com/muremwa/Project-Reader',
    description='Read and analyse the files in your projects.',
    long_description=main_description,
    long_description_content_type='text/x-rst',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
