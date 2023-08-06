from setuptools import setup, find_packages
setup(
 name='fillnull',
 version='0.0.1',
 description='fillnull helps to automate the process of filling all null values in a dataframe by predicting their value using your algorithm of choice,',
 url='https://github.com/sire-ambrose/fillnull', 
 author='Sire Ambrose',
 author_email='ikpeleambroseobinna@gmail.com',
 classifiers=[
   'Operating System :: OS Independent',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3',
   'Programming Language :: Python :: 3.5',
   'Programming Language :: Python :: 3.6',
   'Programming Language :: Python :: 3.7',
   'Programming Language :: Python :: 3.8',
 ],
 keywords=['null', 'nan', 'null values', 'nan values', 'pandas fill'],
 packages=find_packages()
)