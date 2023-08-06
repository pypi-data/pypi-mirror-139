==========
mosaik-fmi
==========

This mosaik-fmi adapter allows to couple FMUs, which are based on the FMI standard (https://fmi-standard.org) with mosaik.

Installation
============

* mosaik-fmi is based on the FMI++ library, which can be found at https://fmipp.sourceforge.io/
* The FMI++ python interface is used, which can be found at https://github.com/AIT-IES/py-fmipp. See this page also for details about installation and requirements of the python interface.

Test
====

The tests for Co-Simulation and ModelExchange in test_fmuAdapter.py don't work together yet and have to be called separately
(by commenting out the respective other one in @pytest.mark.parametrize("fmi_type,fmu_dir").

The FMU for the test is based on https://github.com/qtronic/fmusdk.

Getting help
============

If you need help, please visit the `mosaik-users mailing list`__ .

__ https://mosaik.offis.de/mailinglist