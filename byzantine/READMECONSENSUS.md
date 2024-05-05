 # Byzantine Consensus Algorithm Simulation

## Overview

This project simulates a Byzantine fault tolerance algorithm among multiple nodes in a network. The simulation includes nodes that may behave in a Byzantine manner (i.e., nodes that can act maliciously or erratically). The system uses a consensus mechanism to decide on a common value despite the presence of these Byzantine nodes.


## Key Features
- Simulation of Byzantine fault tolerance using event-driven programming.
- Utilization of threading to simulate concurrent node operations.
- Dynamic simulation of Byzantine nodes that may alter or corrupt decision-making processes.
- Utilization of a simple majority voting mechanism to reach consensus.
- Handling of INIT, VOTE, ECHO, and DECIDE events to simulate the communication between nodes.
- Randomized initial voting to simulate diversity in initial states.

## Requirements

- Python 3.x
- `threading` and `queue` libraries for handling multithreading.
- `Crypto` library for handling cryptographic operations like signing and verifying messages.

## Usage

To run the simulation, simply execute the main Python script:

```bash
python ByzantineConsensus.py
```

## Configuration

You can configure the number of nodes, the number of Byzantine nodes, and other parameters directly in the script:

- `num_nodes`: Total number of nodes in the simulation.
- `byzantine_nodes`: A set of indices indicating which nodes should behave in a Byzantine manner.



## Simulation Details

- The script sets up a network of nodes where each node is a thread that:

- Participates in voting on a binary decision (0 or 1).
- Communicates with other nodes to echo votes and decide based on the majority.
- Handles Byzantine behavior where nodes can randomly alter their votes.

Each node processes events such as voting, echoing votes, and making decisions. The simulation tracks the state of each node, from undecided to decided, and outputs the final decision of each node.

## Output
The script will print the final decision of each node after the simulation concludes. It shows whether nodes have reached a consensus or if the presence of Byzantine nodes influenced the outcome differently.

## Extending the Simulation
To extend this simulation, consider implementing:

- Network delays and packet loss.
- Different Byzantine behaviors beyond simple vote alteration.
