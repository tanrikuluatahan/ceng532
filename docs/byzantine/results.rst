.. include:: substitutions.rst

Implementation, Results and Discussion
======================================

Implementation and Methodology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The implementation of the Byzantine consensus algorithms, namely the Bracha-Toueg and Lamport-Shostak-Pease algorithms, is fundamental to demonstrating their practical utility and validating the theoretical constructs. This section describes the methodology and technical specifics of the implementation, adhering to the principles of reproducibility which underpin the scientific method.

**Methodology**

To ensure that the results are verifiable and the experiments reproducible, a detailed account of the methodologies employed is provided:

- **Simulation Environment**: The algorithms were implemented within a simulated network environment using the AdHocComputing Framework V2. This environment allowed the simulation of various network conditions and Byzantine faults.
- **Node Configuration**: Each node in the network was configured to either follow the protocol honestly or exhibit Byzantine behavior as per the experiment's design. Nodes were implemented using Python, with cryptographic operations handled via the PyCryptoDome library for authenticity.
- **Data Collection**: Data on message transmission, consensus achievement, and algorithm termination were automatically logged by the simulation environment for subsequent analysis.

**Equipment and Materials**

The following tools and technologies were used:

- **Computational Resources**: Simulations were run on virtual machines to handle multiple simulation instances simultaneously.
- **Software Tools**: The entire simulation was orchestrated using Python 3.10, with dependencies on libraries such as PyCryptoDome for cryptographic functionality and NumPy for data handling and analysis.

**Procedure**

- **Network Setup**: A network of virtual nodes was programmatically created, with each node assigned a unique role (general, lieutenant) and behavior (Byzantine or non-Byzantine).
- **Experiment Execution**: Experiments were conducted by initiating the consensus protocol with predetermined values and observing the system's ability to reach a consensus despite the presence of Byzantine faults.
- **Data Handling**: Raw data from the simulations were processed using statistical software to calculate the frequency and conditions of consensus achievement.


Results
~~~~~~~~

Present your AHCv2 run results, plot figures.

**Results**

The implementation of the Bracha-Toueg and Lamport-Shostak-Pease algorithms demonstrated a high degree of resilience to Byzantine faults. Specific results included:

- **Consensus Accuracy**: Both algorithms consistently achieved consensus among non-faulty nodes across various test scenarios involving different numbers and configurations of Byzantine nodes.
- **Performance Metrics**: The time to reach consensus and the number of messages exchanged were measured, providing insights into the efficiency of each algorithm under stress.


This is probably the most variable part of any research paper, and depends upon the results and aims of the experiment. For quantitative research, it is a presentation of the numerical results and data, whereas for qualitative research it should be a broader discussion of trends, without going into too much detail. For research generating a lot of results, then it is better to include tables or graphs of the analyzed data and leave the raw data in the appendix, so that a researcher can follow up and check your calculations. A commentary is essential to linking the results together, rather than displaying isolated and unconnected charts, figures and findings. It can be quite difficulty to find a good balance between the results and the discussion section, because some findings, especially in a quantitative or descriptive experiment, will fall into a grey area. As long as you not repeat yourself to often, then there should be no major problem. It is best to try to find a middle course, where you give a general overview of the data and then expand upon it in the discussion - you should try to keep your own opinions and interpretations out of the results section, saving that for the discussion [Shuttleworth2016]_.





.. list-table:: Byzantine Auth
   :widths: 25 25 25 25 25
   :header-rows: 1

   * - Node Count
     - Decision
     - Byzantine Count
     - General is byzantine(T/F)
     - Result(1's and 0's Count)
   * - 5, column 1
     - 
     - 5//3 = 1
     - True
     - 5 ACCEPT
   * - 5, column 1
     - 
     - 5//3 = 1
     - False
     - 5 ACCEPT
   * - 8, column 1
     - 
     - 8//3 = 2
     - True
     - ACCEPT
   * - 8, column 1
     - 
     - 8//3 = 2
     - False
     - ACCEPT
   * - 10, column 1
     - 
     - 10//3 = 3
     - True
     - Cannot sync
   * - 10, column 1
     - 0
     - 10//3 = 3
     - False
     - Cannot sync
   * - 12, column 1
     - 
     - 12//3 = 4
     - True
     - Cannot init
   * - 12, column 1
     - 0
     - 12//3 = 4
     - False
     - Cannot init

.. list-table:: Byzantine Consensus
   :widths: 25 25 25 25 25
   :header-rows: 1

   * - Node Count
     - Decision
     - Byzantine Count
     - Result(1's and 0's Count)
   * - 5, column 1
     - 
     - 5//3 = 1
     - 0:5, 1:0
   * - 8, column 1
     - 
     - 8//3 = 2
     - 0:0, 1:8
   * - 10, column 1
     - 
     - 10//3 = 3
     - 0:1, 1:9
   * - 12, column 1
     - 
     - 12//3 = 4
     - 0:11, 1:0 , None:1
   * - 12, column 1
     - 
     - 12//3 = 4
     - AFTER 12 IT GETS UNRELIABLE


Discussion
~~~~~~~~~~

The results confirm the robustness of the Byzantine fault tolerance mechanisms provided by both algorithms. However, the Lamport-Shostak-Pease algorithm showed a higher computational overhead due to its reliance on cryptographic verification, which was more resource-intensive than the message redundancy approach used by the Bracha-Toueg algorithm.

These findings suggest that while both algorithms are effective for ensuring consensus in the presence of Byzantine faults, the choice between them should consider the network's size, the expected number of Byzantine nodes, and the available computational resources.




.. [Shuttleworth2016] M. Shuttleworth. (2016) Writing methodology. `Online <https://explorable.com/writing-methodology>`_.