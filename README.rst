################################
pl-chris_test
################################


Abstract
********

Chris Hackathon test app

Run
***

Using ``docker run``
====================

Assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``

.. code-block:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing   \
            fnndsc/pl-chris_test chris_test.py            \
            /incoming /outgoing

This will ...

Make sure that the host ``$(pwd)/out`` directory is world writable!







