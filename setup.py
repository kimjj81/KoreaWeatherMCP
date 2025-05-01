from setuptools import setup, find_packages

setup(
    name='korea-weather-mcp',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.103.1',
        'uvicorn>=0.22.0',
        'httpx>=0.25.0',
        'python-dotenv>=1.0.0',
        'mcp>=0.2.0'
    ],
    python_requires='>=3.8',
    author='Korea Weather MCP',
    description='기상청 중기예보 조회 MCP 서버',
) 