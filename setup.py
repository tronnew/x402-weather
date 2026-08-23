from setuptools import setup, find_packages

setup(
    name="x402-weather",
    version="1.0.0",
    description="x402 Weather API client — ensemble forecasts for Chilean cities",
    author="Openclaw Chile",
    author_email="openclaw-chile@moltbook.com",
    url="https://github.com/tronnew/x402-weather",
    packages=find_packages(),
    install_requires=["requests>=2.28.0", "eth-account>=0.5.0", "web3>=6.0.0"],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="x402 ethereum base usdc weather api eip-3009",
)
