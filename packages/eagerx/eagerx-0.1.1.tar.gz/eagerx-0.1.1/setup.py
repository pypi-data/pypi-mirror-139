# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eagerx',
 'eagerx.bridges',
 'eagerx.bridges.openai_gym',
 'eagerx.bridges.test',
 'eagerx.converters',
 'eagerx.core',
 'eagerx.enginestates',
 'eagerx.nodes',
 'eagerx.utils',
 'eagerx.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Rx>=3.2.0,<4.0.0',
 'defusedxml>=0.7.1,<0.8.0',
 'gym>=0.20.0,<0.21.0',
 'netifaces>=0.11.0,<0.12.0',
 'networkx>=2.5.1,<3.0.0',
 'opencv-python>=4.3.0.36,<5.0.0.0',
 'psutil>=5.9.0,<6.0.0',
 'rospkg>=1.3.0,<2.0.0',
 'scikit-image>=0.17.2,<0.18.0',
 'tabulate>=0.8.9,<0.9.0',
 'termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'eagerx',
    'version': '0.1.1',
    'description': 'Engine Angostic Gym Environments for Robotics',
    'long_description': '******\nEAGERx\n******\n**Streamlining the transfer of simulated robot learning to the real-world.**\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: codestyle\n\n.. image:: https://readthedocs.org/projects/mushroomrl/badge/?version=latest\n   :target: https://eagerx.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/eager-dev/eagerx/actions/workflows/ci.yml/badge.svg?branch=master\n   :target: https://github.com/MushroomRL/mushroom-rl/actions/workflows/continuous_integration.yml\n   :alt: Continuous Integration\n\n.. image:: https://api.codeclimate.com/v1/badges/3146dce3dd4c3537834c/maintainability\n   :target: https://codeclimate.com/github/eager-dev/eagerx/maintainability\n   :alt: Maintainability\n\n.. image:: https://api.codeclimate.com/v1/badges/3146dce3dd4c3537834c/test_coverage\n   :target: https://codeclimate.com/github/eager-dev/eagerx/test_coverage\n   :alt: Test Coverage\n\n\n\n.. contents:: Table of Contents\n    :depth: 2\n\n\nWhat is EAGERx\n==============\nEAGERx enables users to easily define new tasks, switch from one sensor to another,\nand switch from simulation to reality with a single line of code by being invariant to the physics engine.\nEAGERx explicitly addresses the differences in learning between simulation and reality,\nwith essential features for roboticists such as a safety layer, signal delay simulation, and controller switching for resets.\nA single RL pipeline that works with both the simulated and real robots eliminates the chance for mismatches between the simulation and reality implementation.\nThe defined task follows the OpenAI Gym interface, so one can plug in algorithms from established RL libraries\n(e.g., `Stable-baselines3 <https://github.com/DLR-RM/stable-baselines3>`_ ) to solve the task afterward, again minimizing implementation errors.\n\n`Full documentation and tutorials available here <https://eagerx.readthedocs.io/en/latest/>`_.\n\n..\n    TODO: ADD code example with gifs?\n    Example\n    =================\n\nInstallation\n============\n\nYou can do a minimal installation of ``EAGERx`` with:\n\n.. code:: shell\n\n    pip3 install eagerx\n\nEAGERx depends on a minimal ROS installation. Fortunately, you **can** use eagerx anywhere as you would any python package,\nso it does **not** impose a ROS package structure on your project.\nSee `here <ROS_>`_ for installation instructions.\n\nExtras: GUI\n---------------------\n\nTo install the whole set of features, you will need additional packages.\nYou can install everything by running:\n\n.. code:: shell\n\n    pip3 install eagerx-gui\n\n..\n  TODO: Add example and gif of GUI\n\nExtras: training visualization\n---------------------\n\nFor training visualization, either a ``desktop`` or ``desktop-full`` ROS installation is required.\nSee `here <ROS_>`_ for installation instructions.\n\n..\n  TODO: add example and gif of visualization.\n\nDependencies\n============\nBelow you find instructions for installing dependencies required for EAGERx.\n\nROS\n---------------------\n\nSee the `ROS Installation Options <https://eagerx.readthedocs.io/en/latest/>`_, or do the following.\nBy replacing ``<DISTRO>`` with the supported ROS distributions (``noetic``, ``melodic``),\nand ``<PACKAGE>`` with the installation type (``ros-base``, ``desktop``, ``desktop-full``),\na minimal ros installation can be installed with:\n\n.. code:: shell\n\n    sudo sh -c \'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list\'\n    sudo apt install curl # if you haven\'t already installed curl\n    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -\n    sudo apt update\n    sudo apt install ros-<DISTRO>-<PACKAGE>\n    sudo apt-get install ros-<DISTRO>-cv-bridge\n\nMake sure to source ``/opt/ros/<DISTRO>/setup.bash`` in the environment where you intend to ``eagerx`` in.\nIt can be convenient to automatically source this script every time a new shell is launched.\nThese commands will do that for you if you:\n\n.. code:: shell\n\n      echo "source /opt/ros/<DISTRO>/setup.bash" >> ~/.bashrc\n      source ~/.bashrc\n\nIn case you make use of a virtual environment, move to the directory containing the ``.venv`` and\nadd ``source /opt/ros/<DISTRO>/setup.bash`` to the activation script before activating the environment with\nthis line:\n\n.. code:: shell\n\n      echo "source /opt/ros/<DISTRO>/setup.bash" >> .venv/bin/activate\n\nCite EAGERx\n===============\nIf you are using EAGERx for your scientific publications, please cite:\n\n.. code:: bibtex\n\n    @article{eagerx,\n        author  = {van der Heijden, Bas and Luijkx, Jelle, and Ferranti, Laura and Kober, jens and Babuska, Robert},\n        title = {EAGER: Engine Agnostic Gym Environment for Robotics},\n        year = {2022},\n        publisher = {GitHub},\n        journal = {GitHub repository},\n        howpublished = {\\url{https://github.com/eager-dev/eagerx}}\n    }\n\nMaintainers\n=================\nEAGERx is currently maintained by Bas van der Heijden (`@bheijden <https://github.com/bheijden>`_) and Jelle Luijkx (`@jelledouwe <https://github.com/jelledouwe>`_).\n\nHow to contact us\n=================\nFor any question, drop an e-mail at d.s.vanderheijden@tudelft.nl.\n\nAcknowledgements\n=================\nEAGERx is funded by the `OpenDR <https://opendr.eu/>`_ Horizon 2020 project.',
    'author': 'Bas van der Heijden',
    'author_email': 'd.s.vanderheijden@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eager-dev/eagerx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
