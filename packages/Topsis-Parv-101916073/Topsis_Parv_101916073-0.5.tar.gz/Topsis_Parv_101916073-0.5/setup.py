from distutils.core import setup
setup(
  name = 'Topsis_Parv_101916073',         
  packages = ['Topsis_Parv_101916073'],  
  version = '0.5',      
  license='MIT',        
  description = 'package for implimentation of topsis in python',   
  author = 'Parv Gupta',                   
  author_email = 'parvg555@gmail.com',     
  url = 'https://github.com/parvg555/Topsis_Parv_101916073',   
  download_url = 'https://github.com/parvg555/Topsis_Parv_101916073/archive/refs/tags/stablev0.2.tar.gz',   
  keywords = ['Topsis', 'data science', 'predictive analysis'],   
  install_requires=[           
          'pandas',
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.9',
  ],
)