import setuptools

setuptools.setup(
   name='wagtail_colour_picker_enoki',
   version='0.1.4',
   author='Enoki-Studio',
   author_email='theo@enoki-studio.com',
   packages=['wagtail_colour_picker_enoki'],
   url='http://pypi.python.org/pypi/wagtail_colour_picker_enoki/',
   license='LICENSE.txt',
   description='WagtailColorPickerByEnoki',
   long_description='fix bugs',
   long_description_content_type = 'text/markdown',
   install_requires=[
       "Wagtail >= 2.12.2",
       "Django >= 2.2.13",
       "pytest",
   ],
    keywords=['wagtail', 'draftjs', 'colour', 'picker', 'accent', 'design'],
)