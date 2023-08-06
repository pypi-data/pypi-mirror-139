|Latest release| |PyPI| |CI status| |Test coverage| |All Contributors|

BioSimulators-pyNeuroML
=======================

BioSimulators-compliant command-line interfaces and Docker images for
the
`jNeuroML <https://github.com/NeuroML/jNeuroML>`__/`pyNeuroML <https://github.com/NeuroML/pyNeuroML>`__,
`NEURON <https://neuron.yale.edu/>`__,
`NetPyNe <http://netpyne.org/>`__, and simulation programs.

These command-line interfaces and Docker images enable users to use
jNeuroML/pyNeuroML, NEURON, and NetPyNe to execute `COMBINE/OMEX
archives <https://combinearchive.org/>`__ that describe one or more
simulation experiments (in `SED-ML format <https://sed-ml.org>`__) of
one or more models (in
`NeuroML <https://neuroml.org/>`__/`LEMS <https://lems.github.io/LEMS/>`__
format).

A list of the algorithms and algorithm parameters supported by
jNeuroML/pyNeuroML, NEURON, and NetPyNe is available at
`BioSimulators <https://biosimulators.org/simulators/pyneuroml>`__.

A simple web application and web service for using jNeuroML/pyNeuroML,
NEURON, and NetPyNe to execute COMBINE/OMEX archives is also available
at `runBioSimulations <https://run.biosimulations.org>`__.

Installation
------------

Install Python package
~~~~~~~~~~~~~~~~~~~~~~

1. Install Java
2. Install this package
   ::

      pip install biosimulators-pyneuroml

3. To install support for NetPyNe, install NEURON and install this
   package with the ``netpyne`` option:
   ::

      pip install biosimulators-pyneuroml

4. To install support for NEURON, install NEURON and install this
   package with the ``neuron`` option:
   ::

      pip install biosimulators-pyneuroml

Install Docker image
~~~~~~~~~~~~~~~~~~~~

This package provides three Docker images:

::

   docker pull ghcr.io/biosimulators/netpyne
   docker pull ghcr.io/biosimulators/neuron
   docker pull ghcr.io/biosimulators/pyneuroml

Usage
-----

Local usage
~~~~~~~~~~~

This package provides three command-line applications, each with the
interface illustrated below.

-  ``biosimulators-neuron``
-  ``biosimulators-netpyne``
-  ``biosimulators-pyneuroml``

::

   usage: biosimulators-pyneuroml [-h] [-d] [-q] -i ARCHIVE [-o OUT_DIR] [-v]

   BioSimulators-compliant command-line interface to the pyNeuroML <https://github.com/NeuroML/pyNeuroML> simulation program.

   optional arguments:
     -h, --help            show this help message and exit
     -d, --debug           full application debug mode
     -q, --quiet           suppress all console output
     -i ARCHIVE, --archive ARCHIVE
                           Path to OMEX file which contains one or more SED-ML-
                           encoded simulation experiments
     -o OUT_DIR, --out-dir OUT_DIR
                           Directory to save outputs
     -v, --version         show program's version number and exit

Usage through Docker containers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The entrypoints to the Docker images support the same command-line
interface described above.

For example, the following command could be used to use the Docker image
to execute the COMBINE/OMEX archive ``./modeling-study.omex`` and save
its outputs to ``./``.

::

   docker run \
     --tty \
     --rm \
     --mount type=bind,source="$(pwd)",target=/root/in,readonly \
     --mount type=bind,source="$(pwd)",target=/root/out \
     ghcr.io/biosimulators/pyneuroml:latest \
       -i /root/in/modeling-study.omex \
       -o /root/out

Documentation
-------------

Documentation is available at
https://docs.biosimulators.org/Biosimulators_pyNeuroML/.

License
-------

This package is released under the `MIT <LICENSE>`__.

Development team
----------------

This package was developed by the `Karr Lab <https://www.karrlab.org>`__
at the Icahn School of Medicine at Mount Sinai and the `Center for
Reproducible Biomedical Modeling <https://reproduciblebiomodels.org/>`__
with assistance from the contributors listed `here <CONTRIBUTORS.md>`__.

Questions and comments
----------------------

Please contact the `BioSimulators
Team <mailto:info@biosimulators.org>`__ with any questions or comments.

.. |Latest release| image:: https://img.shields.io/github/v/tag/biosimulators/Biosimulators_pyNeuroML
   :target: https://github.com/biosimulations/Biosimulators_pyNeuroML/releases
.. |PyPI| image:: https://img.shields.io/pypi/v/biosimulators_pyneuroml
   :target: https://pypi.org/project/biosimulators_pyneuroml/
.. |CI status| image:: https://github.com/biosimulators/Biosimulators_pyNeuroML/workflows/Continuous%20integration/badge.svg
   :target: https://github.com/biosimulators/Biosimulators_pyNeuroML/actions?query=workflow%3A%22Continuous+integration%22
.. |Test coverage| image:: https://codecov.io/gh/biosimulators/Biosimulators_pyNeuroML/branch/dev/graph/badge.svg
   :target: https://codecov.io/gh/biosimulators/Biosimulators_pyNeuroML
.. |All Contributors| image:: https://img.shields.io/github/all-contributors/biosimulators/Biosimulators_pyNeuroML/HEAD
   :target: #contributors-
