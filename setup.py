from setuptools import setup

setup(name='Serverelss-REST-Data-API',
      version='0.1',
      description='Building a Scalable Serverelss REST Data API',
      url='https://github.com',
      author='Richard Freeman',
      author_email='richard.freeman att justgiving.com',
      license='Apache',
      version='2.0',
      packages=['aws_dynamo','lambda_dynamo_get'],
      zip_safe=True)