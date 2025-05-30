from setuptools import setup, find_packages
import os
import sys # Import sys for warnings

# Function to read the README.md for the long description
def read_readme():
    readme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
    if not os.path.exists(readme_path):
        print(f"Warning: README.md not found at {readme_path}", file=sys.stderr)
        return "" # Return empty string if README.md is not found
    with open(readme_path, encoding='utf-8') as f:
        return f.read()

# Function to read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt')
    if not os.path.exists(requirements_path):
        print(f"Warning: requirements.txt not found at {requirements_path}", file=sys.stderr)
        return [] # Return empty list if requirements.txt is not found
    with open(requirements_path) as f:
        return f.read().splitlines()

setup(
    name='sdat2img-brotli', # ⚡ PyPI package name updated! Use hyphens for PyPI.
    version='1.0.2',      # Your package version number. Increment for new releases!
    author='TNTAPPLE',   # Your name or organization
    author_email='tntapple219@gmail.com', # Your email
    description='A Python tool to decompress .dat.br files and convert Android .dat/.transfer.list into .img disk images.',
    long_description=read_readme(),
    long_description_content_type='text/markdown', # Tell PyPI your long_description is Markdown
    url='https://github.com/tntapple219/sdat2img_brotli_forPyPI', # ⚡ Update GitHub URL if applicable
    packages=find_packages(), # Automatically discover packages. find_packages() will find 'sdat2img_brotli'
    install_requires=read_requirements(), # Read dependencies from requirements.txt
    classifiers=[ # Metadata describing your package for PyPI search
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6', # Minimum Python version required
    entry_points={
        'console_scripts': [
            'sdat2img-brotli=sdat2img_brotli.main:convert_rom_files_function', # ⚡ console_script command updated!
            # The command users will type is 'sdat2img-brotli'.
            # It will execute convert_rom_files_function from sdat2img_brotli/main.py.
        ],
    },
)