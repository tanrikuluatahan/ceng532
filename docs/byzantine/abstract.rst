.. include:: substitutions.rst
========
Abstract
========

.. Investigating Byzantine fault tolerance in systems where many parts work together without a central timing mechanism is a tough challenge. It involves creating rules for agreement that stay strong even when some parts fail in unpredictable ways. This is crucial for keeping the system working smoothly, making sure all parts can agree, and staying strong against these failures. These rules are key to keeping the system safe and working well, even when facing tough conditions. The important work of Bracha and Toueg on these rules for agreement and message sharing helps tackle these challenges. They set up a way to handle faults that keeps the system working well and able to grow. Their work is very important for understanding how to reach agreement in systems where the behavior of parts is not certain. In our paper, we look closely at Bracha and Toueg’s methods, checking how they are built and how they work today. We examine how these methods can handle different kinds of failures, how they affect how well the system works, and how relevant they are to today's technology. Through detailed study and tests, we reveal how efficient and resilient these methods are, and what they mean for modern systems that work together. Our results show the lasting importance of Bracha and Toueg’s work, explaining its value both in theory and in practice for systems that need to be fault-tolerant. Our study confirms the basic importance of their methods and shows new directions for making systems more robust and effective when facing Byzantine failures.

.. Write your abstract here.

.. An abstract summarizes, in one paragraph (usually), the major aspects of the entire paper/report in the following prescribed sequence [Anderson2016]:

.. - the question(s) you investigated (or purpose), (from Introduction)
.. - state the purpose very clearly in the first or second sentence.
.. - the experimental design and methods used; clearly express the basic design of the study; name or briefly describe the basic methodology used without going into excessive detail-be sure to indicate the key techniques used.
.. - the major findings including key quantitative results, or trends; report those results which answer the questions you were asking; identify trends, relative change or differences, etc.
.. - a brief summary of your interpretations and conclusions; clearly state the implications of the answers your results gave you.


.. The length of your Abstract should be kept to about 200-300 words maximum. Limit your statements concerning each segment of the paper (i.e. purpose, methods, results, etc.) to two or three sentences. The Abstract helps readers decide whether they want to read the rest of the paper, or it may be the only part they can obtain via electronic literature searches or in published abstracts. Therefore, enough key information (e.g., summary results, observations, trends, etc.) must be included to make the Abstract useful to someone who may to reference your work~\cite{Anderson2016}.

.. How do you know when you have enough information in your Abstract? A simple rule-of-thumb is to imagine that you are another researcher doing an study similar to the one you are reporting. If your Abstract was the only part of the paper you could access, would you be happy with the information presented there?

.. The Abstract is ONLY text. Use the active voice when possible, but much of it may require passive constructions. Write your Abstract using concise, but complete, sentences, and get to the point quickly. The Abstract SHOULD NOT contain~\cite{Anderson2016}:

.. -  lengthy background information,
.. -  references to other literature,
.. -  elliptical (i.e., ending with ...) or incomplete sentences,
.. -  abbreviations or (mathematical) terms that may be confusing to readers,
.. -  any sort of illustration, figure, or table, or references to them.



.. .. admonition:: EXAMPLE 

In the study of distributed systems, achieving consensus in the presence of Byzantine faults remains a fundamental challenge. This report delves into the mechanisms and performance of two prominent Byzantine fault tolerance algorithms: the Bracha-Toueg Byzantine consensus algorithm and the Lamport-Shostak-Pease authentication algorithm. Utilizing the AdHocComputing Library for simulation and testing, this research aims to explore their effectiveness in different network conditions and fault scenarios.

The Bracha-Toueg algorithm operates under the assumption of partial synchrony and provides fault tolerance by using additional rounds of communication to confirm the consistency of the messages received by non-faulty nodes. This algorithm ensures safety by preventing nodes from deciding prematurely based on potentially faulty or inconsistent messages. The resilience of the algorithm is tested by simulating scenarios with varying numbers of Byzantine nodes to assess its fault tolerance limit and the impact on consensus latency.

Conversely, the Lamport-Shostak-Pease algorithm leverages cryptographic methods to authenticate messages among processes, ensuring that a receiver can verify the origin of a message reliably. This approach is particularly powerful in thwarting the Byzantine generals problem by preventing forged message attacks. The algorithm's strength lies in its use of digital signatures to validate the sequence of messages transmitted between nodes, thus ensuring the integrity of the decision-making process.

Our comparative analysis focuses on the algorithms' operational overhead, the complexity of implementation, and their scalability in larger networks. Results indicate that while the Bracha-Toueg algorithm excels in environments where tighter control over message timing is possible, the Lamport-Shostak-Pease algorithm is superior in networks where securing message integrity and origin is paramount.

This report confirms that both algorithms provide robust solutions to Byzantine faults but highlight the importance of choosing the appropriate algorithm based on specific network requirements and threat models. These findings contribute to the broader understanding of distributed systems security, offering valuable insights for researchers and practitioners aiming to enhance the reliability and integrity of distributed protocols.

