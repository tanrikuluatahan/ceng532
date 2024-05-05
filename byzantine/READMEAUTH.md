# Byzantine Authentication Simulation

## Overview
This Python script simulates a network of nodes operating under the Byzantine Fault Tolerance algorithm. It demonstrates how a system can achieve consensus even in the presence of a subset of nodes that may behave maliciously or fail to respond.

## Key Features
- Simulation of a distributed network with nodes that may exhibit Byzantine behavior.
- Implementation of cryptographic signing and verification to ensure message integrity.
- Ability to configure the number of nodes and the number of Byzantine nodes dynamically.
- Use of threading to simulate simultaneous operations of multiple nodes in a network.

## Requirements
To run this simulation, you need Python 3.x with the following packages installed:
- `pycryptodome` for cryptographic operations

You can install the required package using pip:
```bash
pip install pycryptodome
```

## Usage
To run the simulation, simply execute the main Python script:

```bash
python ByzantineAuth.py
```


## Configuration

You can configure the number of nodes, the number of Byzantine nodes, and other parameters directly in the script:

- `num_nodes`: Total number of nodes in the simulation.
- `byzantine_nodes`: A set of indices indicating which nodes should behave in a Byzantine manner.


## Simulation Details
- The simulation initializes a network of nodes where each node is represented as a thread.
- Nodes communicate through a simulated network using message passing, where messages include a value and a digital signature.
- The "general" node broadcasts an initial value, which is then propagated through the network.
- Nodes attempt to reach consensus on the initial value despite the presence of Byzantine nodes which may alter or forge messages.
## Output
- The script outputs the final decision of each node after running the consensus algorithm. If a node reaches a decision, it prints its final decision. Otherwise, it indicates a failure to reach consensus.

### Extending the Simulation
- To extend this simulation:

- Adjust the k value to change the number of communication pulses.
- Implement additional Byzantine behaviors and consensus algorithms.
- Enhance the simulation environment to more complex network conditions and failure modes.