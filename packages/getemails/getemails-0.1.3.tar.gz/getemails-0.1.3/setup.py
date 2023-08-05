from setuptools import setup

setup(
    name='getemails',
    version='0.1.3',    
    description='Python module for generating random emails',
    long_description="""<b>Python module for generating random emails and names and surnames</b>
    Initially import: <br>
    from genemails import GET_EMAIL<br>
    To generate one random email:<br>
        email=GET_EMAIL.generate_email()<br>
    To generate many emails use:<br>
        manyemails=GET_EMAIL.generate_emails(15) #It will return string separated by comma<br>
    To get random 1st or surname name:<br>
        fisrtname=GET_EMAIL.get_firstname()<br>
        surname=GET_EMAIL.get_sndname()<br>
    """,
    long_description_content_type='text/markdown',
    
    url='https://github.com/hendalf332/genemails',
    author='Hendalf332',
    author_email='ludvih177xe@tutanota.com',
    license='GPL',
    packages=['genemails'],
    install_requires=['colorama>=0.4.4',                   
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',        
    ],
)
