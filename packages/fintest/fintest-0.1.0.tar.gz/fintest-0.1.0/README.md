# fintest

**F**unctional and **In**tegration **Test**ing toolkit for Python.

Aim of this toolkit is to make it easier to write integration and functional tests in python using the pytes testing library. It makes use of pytest fixtures to setup pre-test environments.

## Core Concepts

### Components

Components can be thought of the main programs/APIs/microservices that need to communicate together. These components can have their own config specifying things like database connection parameters, endpoints, location (url, ip, etc) for actual component instances running somewhere that can be used for testing.


### Tests

The tests themself are normal pytest based tests that utilize component fixtures to specify which components should be "made available" for the current test.


