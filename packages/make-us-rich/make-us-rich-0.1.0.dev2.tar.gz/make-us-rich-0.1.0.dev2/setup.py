# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['make_us_rich',
 'make_us_rich.cli',
 'make_us_rich.client',
 'make_us_rich.interface',
 'make_us_rich.pipelines',
 'make_us_rich.pipelines.converting',
 'make_us_rich.pipelines.exporting',
 'make_us_rich.pipelines.fetching',
 'make_us_rich.pipelines.preprocessing',
 'make_us_rich.pipelines.training',
 'make_us_rich.serving',
 'make_us_rich.utils',
 'make_us_rich.worker']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.26,<4.0.0',
 'docker>=5.0.3,<6.0.0',
 'ipython>=7.10,<8.0',
 'isort>=5.0,<6.0',
 'jupyter-client>=5.1',
 'jupyter>=1.0,<2.0',
 'jupyterlab>=3.0,<4.0',
 'kedro-viz==3.16.0',
 'kedro[pandas.CSVDataSet]==0.17.6',
 'minio==7.1.2',
 'onnx==1.10.2',
 'onnxruntime==v1.10.0',
 'pandas>=1.4.0,<2.0.0',
 'prefect==0.15.13',
 'python-binance==v0.7.10',
 'python-dotenv>=0.19.2,<0.20.0',
 'pytorch-lightning==1.5.9',
 'scikit-learn==1.0.2',
 'torch==1.10.0',
 'typer[all]>=0.4.0,<0.5.0',
 'wandb==0.12.9']

entry_points = \
{'console_scripts': ['mkrich = make_us_rich.cli.main:app']}

setup_kwargs = {
    'name': 'make-us-rich',
    'version': '0.1.0.dev2',
    'description': 'Cryptocurrency forecasting 📈 training and serving models made automatic',
    'long_description': '# 🚧 Be carefull this repo is still a work in progress\n\nWhat is already functional?\n- [ ] Prefect Flows - 80%\n- [x] Training pipeline - 100%\n- [x] Serving models - 100%\n- [x] Interface - 100%\n- [ ] CLI - 70%\n- [ ] Documentation - 0%\n\nDev package available on [PyPI](https://pypi.org/project/make-us-rich/).\n\n# Make Us Rich\nDeep Learning applied to cryptocurrency forecasting.\n\nFor more details on how to use this project, please refer to [documentation](https://chainyo.github.io/make-us-rich/).\n\nYou can inspect the training pipeline with the `Kedro Viz` tool, available [here](https://makeusrich-viz.chainyo.tech)\n\n---\n\n## Introduction\n\nWe provide a simple way to train, serve and use cryptocurrency forecasting models on a daily basis.\n\n![Project Architecture](assets/project_architecture.png)\n\nEvery hour `Prefect` flows are launched to train and store models automatically.\nEach flow has 2 variables: `currency` and `compare` to identify which type of data the `fetching data` part\nneeds to get from the `Binance API` to train the model.\n\nFor example, if you want to train a model on the currency `Bitcoin` compared with `US Dollar`: `currency="btc",compare="usdt"`.\n\nYou have to give the symbol for each variable. Find all available symbols on the \n[Binance](https://www.binance.com/en/markets) platform.\n\nOnce the `Kedro` pipeline is launched, everything works smoothly and automatically. \n\nThere is 5 steps for the pipeline to complete:\n- \U0001fa99 Fetching data from Binance API.\n- 🔨 Preprocessing data:\n    - Extract features from fetched data.\n    - Split extracted features.\n    - Scale splitted features.\n    - Create sequences with scaled train features.\n    - Create sequences with scaled test features.\n    - Split train sequences as train and validation sequences.\n- 🏋️ Training model.\n- 🔄 Converting model to ONNX format.\n- 📁 Uploading converted model to object storage service.\n\nAfter the end of the training pipeline, the new model will be available for serving. \nEvery 10 minutes, a `Prefect` flow is launched to update the API with lastest available models for each currency.\n\nThe final step is the crypto dashboard that allows users to see forecasting for their favorite assets.\n\n---\n\n## Prerequisites\n\nThe main project has `poetry` as package manager. If you need to install poetry, check their awesome \n[documentation](https://python-poetry.org/docs/).\n\nYou don\'t need to clone this project to your local machine. You can simply install the `make-us-rich` package with this \ncommand:\n```bash\n$ pip install make-us-rich\n```\n\nIt\'s recommended to have an isolated environment for each component of the project, unless you run everything on the \nsame machine.\n\n\n## CLI Usage\n\nTODO\n',
    'author': 'Thomas Chaigneau',
    'author_email': 't.chaigneau.tc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
