from setuptools import setup  
requirements = ["Pygame==2.1.1","keyboard","pygame_widgets","colorama"]
setup(name='GRPgraph',
       version='15.5.122c',
       description='small and compact graphick distributions',
       packages=['GRPgraph'],       
       author_email='pvana621@gmail.com', 
       install_requires=requirements,      
       zip_safe=False)