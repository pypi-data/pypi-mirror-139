﻿
***************************************
Raisin: To perform cluster work easily!
***************************************

.. Pour la syntaxe voir: https://deusyss.developpez.com/tutoriels/Python/SphinxDoc/

Project Philosophy
^^^^^^^^^^^^^^^^^^

| The main aim of project\ *raisin*\  is to \ **share physical resources**\  of your laptop with a community.
| In counterpart, you can \ **benefit from the community resources**\ .
| There are 2 sides in this project:

1. Resources usage
------------------

| The \ *raisin*\  API wants to be as close as possible to the 'threading' and 'multiprocessing' python APIs.
| The advantage in using \ *raisin*\  rather than 'threading' or 'multiprocessing' is that the computing power is greatly increased (depending on the number of connected resources).
| Though \ *raisin*\  is based on 'multiprocessing' module - that splits tasks among the resources of a single computer - it also shares the load over the different machines in the network. Everything is automatically and intelligently orchestrated.

\ *raisin*\  wants to be \ **as simple as possible**\ . That’s why the code analysis and the resources management are automated. It also uses a bunch of classes and functions default parameters that are suitable for most usages.

| However, you can tune \ *raisin*\  behavior as you want since all these parameters are \ **fully customizable**\ .
| \ *raisin*\  is a multi-OS module 100% written in python in order to keep installation reliable and simple.

In a future version, \ *raisin*\  will be able to perform automatic parallelization, a little like 'pydron'.

2. Resources sharing
--------------------

| To be able to use community resources, you must give in return!
| That’s why, when \ *raisin*\  is installed as a python package, you have to install the 'application' part.
| The minimum to do is to start a grape server that will be listening to execute the tasks requested by itself or by other users on the network. To do this, run the following command: ``python -m raisin server``

Installation
^^^^^^^^^^^^

| To install the module, you have to go through pypi: ``pip install raisin``.
| Once the module is installed, execute ``python -m raisin install`` to create the configuration file.
| For the uninstallation, it is enough to execute ``python -m raisin uninstall && pip uninstall raisin``.

Basic example
^^^^^^^^^^^^^

.. code:: python

    >>> import raisin
    >>> f = lambda x: x**2 # a costly function
    >>> list(raisin.imap_unordered(f, range(3), context=True))
    [Result(0), Result(1), Result(4)]
    >>>


* See the `documentation <http://raisin-docs.ddns.net/>`_ for more details and examples.
