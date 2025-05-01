from setuptools import setup, find_packages

setup(
    name='korea-weather-mcp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'requests',
        'python-dotenv',
        'pydantic',
    ],
    author='Korea Weather MCP',
    description='기상청 중기예보 조회 MCP 서버',
) 