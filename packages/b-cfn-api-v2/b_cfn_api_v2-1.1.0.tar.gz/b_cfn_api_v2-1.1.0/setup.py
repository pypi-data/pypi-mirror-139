from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_cfn_api_v2',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'b_cfn_api_v2_test'
    ]),
    description=(
        'Convenient wrapper around CfnApi.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'b_cfn_custom_userpool_authorizer>=0.1.1,<1.0.0',
        'b_cfn_custom_api_key_authorizer>=1.1.0,<2.0.0',

        'aws_cdk.aws_apigatewayv2>=1.90.0,<1.145.0',
        'aws_cdk.aws_lambda>=1.90.0,<1.145.0',
        'aws-cdk.assets>=1.90.0,<1.145.0',
        'aws-cdk.aws-ec2>=1.90.0,<1.145.0',
        'aws-cdk.core>=1.90.0,<1.145.0',
        'aws-cdk.custom-resources>=1.90.0,<1.145.0',
        'aws-cdk.cloud-assembly-schema>=1.90.0,<1.145.0',
        'aws-cdk.region-info>=1.90.0,<1.145.0',
        'aws-cdk.aws-cognito>=1.90.0,<1.145.0',
        'aws-cdk.aws_cloudfront>=1.90.0,<1.145.0',
        'aws-cdk.aws_cloudfront_origins>=1.90.0,<1.145.0',
        'aws-cdk.cloud-assembly-schema>=1.90.0,<1.145.0',
        'aws-cdk.region-info>=1.90.0,<1.145.0',
    ],
    keywords='AWS API Gateway',
    url='https://github.com/biomapas/B.CfnApiV2.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
