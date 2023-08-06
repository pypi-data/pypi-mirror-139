*******
Scripts
*******

.. warning:: All execution examples are not meant to be copy&pasted! Cobbler instances are very custom and each command
             needs to be adjusted to your environment.

migrate-data-v2-to-v3.py
########################

Description
===========

This script tries to convert your old Cobbler 2.x.x data to Cobbler 3.x.x data. It won't make backups and can't rollback
the changes it did.

Execution examples
==================

.. code-block:: shell

   python3 migrate-data-v2-to-v3.py

Author
======

`Orion Poplawski <https://github.com/opoplawski>`_

settings-migration-v1-to-v2.sh
##############################

Description
===========

This script will try to replace your old ``modules.conf`` file (< 3.0.1) to a new one (>= 3.0.1).

Execution examples
==================

.. code-block:: shell

   ./settings-migration-v1-to-v2.sh -h
   ./settings-migration-v1-to-v2.sh -r -f /etc/cobbler/modules.conf
   ./settings-migration-v1-to-v2.sh -n -f /etc/cobbler/modules.conf
   ./settings-migration-v1-to-v2.sh -s -f /etc/cobbler/modules.conf

Author
======

`Enno Gotthold <https://github.com/SchoolGuy>`_
