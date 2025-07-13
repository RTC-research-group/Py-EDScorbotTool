API reference for C/C++ Runtime
==================================

.. doxygenclass:: EDScorbot
    :private-members:
    :members:
    

.. doxygenclass:: EDScorbotJoint
    :members:

Scripts
=======


Home routine
------------

.. doxygenfile:: home.cpp

Read Joints and publish
------------------------

.. doxygenfile:: read_joints.cpp

Reset home position 
-------------------
.. note:: 
    Don't confuse 'Home routine' with 'Reset home position'. The former sets the real position of the robot to its designated home/default position, there are hardware checks to ensure this.
    The latter just resets the controller's internal logic in order to tell it that the position the joints are in right at the moment of the call is their home position, so the controller will match the reference 0 to that position
.. doxygenfile:: reset_all.cpp

Send Home
---------
.. doxygenfile:: send_0.cpp

Move a joint
---------------------------
.. doxygenfile:: sendRefJx.cpp

..
        alpsfjapdfj THIS IS A COMMENT