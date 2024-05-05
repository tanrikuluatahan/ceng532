.. include:: substitutions.rst

Introduction
============


.. If you would like to get a good grade for your project, you have to write a good report.  Your project will be assessed mostly based on the report. Examiners are not mind-readers, and cannot give credit for work which you have done but not included in the report [York2017]_.

.. Here is the Stanford InfoLab's patented five-point structure for Introductions. Unless there's a good argument against it, the Introduction should consist of five paragraphs answering the following five questions:

.. - What is the problem?
.. - Why is it interesting and important? What do you gain when you solve the problem, and what do you miss if you do not solve it?
.. - Why is it hard? (e.g., why do naive approaches fail?)
.. - Why hasn't it been solved before? What's wrong with previous proposed solutions? How does yours differ?
.. - What are the key components of your approach and results including any specific limitations.

.. Then have a penultimate paragraph or subsection: "Contributions". It should list the major contributions in bullet form, mentioning in which sections they can be found. This material doubles as an outline of the rest of the paper, saving space and eliminating redundancy.

.. .. [York2017]  York University. (2017) How to write a project report.



.. .. admonition:: EXAMPLE 



..    In the realm of snapshot algorithms for distributed systems, the fundamental problem lies in capturing a consistent global state without interrupting the ongoing execution of processes and avoiding excessive overhead. The challenges involve managing concurrency, ensuring accurate message ordering, providing fault tolerance to handle process failures, optimizing efficiency to minimize computational and communication overhead, and maintaining scalability as the system expands. Successfully addressing these challenges is crucial for designing snapshot algorithms that accurately reflect the distributed system's dynamic state while preserving efficiency and resilience.,
    
..    Snapshot algorithms are both interesting and important due to their pivotal role in understanding, managing, and troubleshooting distributed systems. Solving the problem of capturing consistent global states in a distributed environment offers several significant benefits. Firstly, it provides invaluable insights into the system's behavior, facilitating tasks such as debugging, performance analysis, and identifying issues like deadlocks or message race conditions. Moreover, snapshot algorithms enable efficient recovery from failures by providing checkpoints that allow systems to resume operation from a known, consistent state. Additionally, they aid in ensuring system correctness by verifying properties like termination or the absence of deadlock. Without solving this problem, distributed systems would lack the capability to effectively diagnose and resolve issues, leading to increased downtime, inefficiencies, and potentially catastrophic failures. The absence of snapshot algorithms would hinder the development, deployment, and management of robust and reliable distributed systems, limiting their usability and scalability in modern computing environments. Thus, addressing this problem is critical for advancing the field of distributed systems and maximizing the reliability and efficiency of distributed computing infrastructures.

..    Capturing consistent global states in distributed systems poses significant challenges due to their decentralized, asynchronous nature. Naive approaches often fail due to complexities such as concurrency, message ordering, synchronization, fault tolerance, and scalability. Concurrency and ordering issues may lead to inconsistent snapshots, while synchronization difficulties hinder performance. Inadequate fault tolerance can result in incomplete or incorrect snapshots, jeopardizing system recovery and fault diagnosis. Additionally, inefficient approaches may impose excessive overhead, impacting system performance. Overcoming these challenges requires sophisticated algorithms that balance correctness, efficiency, fault tolerance, and scalability, navigating the inherent trade-offs of distributed systems to capture accurate global states without disrupting system operation.

..    The persistent challenge of capturing consistent global states in distributed systems, particularly within the context of the Chandy-Lamport Algorithm, arises from the algorithm's inherent complexities and the dynamic nature of distributed environments. While the Chandy-Lamport Algorithm offers a promising approach by utilizing marker propagation to capture snapshots without halting the system's execution, its implementation faces obstacles such as concurrency management, ensuring accurate message ordering, and handling fault tolerance. Previous attempts at solving these challenges with the Chandy-Lamport Algorithm may have been hindered by their complexity, limited scalability, or inability to adapt to changing system conditions. Thus, achieving a comprehensive resolution within the Chandy-Lamport framework requires addressing these concerns through innovative approaches that optimize for correctness, efficiency, fault tolerance, and scalability while considering the evolving requirements of distributed systems.
    
..    The Chandy-Lamport Algorithm is a key method for capturing consistent global snapshots in distributed systems, comprising the initiation of marker propagation, recording of local states by processes upon marker reception, and subsequent snapshot reconstruction. It allows for the capture of snapshots without halting system execution, facilitating concurrent operations and serving various purposes like debugging and failure recovery. However, the algorithm exhibits limitations including increased message overhead due to marker propagation, challenges in managing concurrency which may affect snapshot accuracy, potential difficulties in handling faults during snapshot collection, and scalability concerns as system size grows. Despite these limitations, the Chandy-Lamport Algorithm remains foundational in distributed systems, driving further research in snapshot capture techniques. DETAILS OF Lai-Yang Algorithm.

..    Our primary contributions consist of the following:
    
..    - Implementation of both the Chandy-Lamport Algorithm and the Lai-Yang Algorithm on the AHCv2 platform. The implementation specifics are detailed in Section XX.
    - Examination of the performance of these algorithms across diverse topologies and usage scenarios. Results from these investigations are outlined in Section XXX.
    - Comprehensive comparison and contrast of the algorithms based on criteria such as accuracy, overhead, complexity, and fault tolerance. Key insights derived from these comparisons are elaborated upon in Section XXXX.
    
Introduction to Byzantine Fault Tolerance

In the area of distributed systems, which are networks of computers working together, ensuring that the system can be trusted and is secure is very important. This is where Byzantine fault tolerance (BFT) comes in. BFT helps these systems reach an agreement or consensus, even when some parts fail in unexpected or harmful ways. These failures are called Byzantine faults. They can make parts of the system act in strange or destructive ways, which makes keeping the system consistent and ensuring smooth communication between its parts very challenging.

BFT is crucial for making sure that a distributed system can keep working properly, even if some parts are faulty or acting oddly. The main idea behind BFT is to create rules or protocols that help all parts of the system agree on something, despite the presence of faults. This is very important in areas like banking and finance, where safety and trust are top priorities, and also in technologies like blockchains, where agreement among all parts is essential.

The concept of BFT was first introduced in a famous paper called “The Byzantine Generals Problem,” written by Leslie Lamport, Robert Shostak, and Marshall Pease. This paper describes a situation where army generals have to come up with a joint plan of action but face the risk of betrayal from some of their own. This story is used to show the difficulty of reaching a reliable agreement in a system where some parts might not be trustworthy. The challenge is to design a system that can still reach a unanimous decision, even when faced with such difficulties.

Following this groundwork, Bracha and Toueg made significant advances in the field with their work on how to achieve consensus and coordinate messages in systems without needing a strict timetable. They provided a way to understand and manage the unpredictable nature of Byzantine faults in a system that can grow and adapt to changing needs.

In our paper, we explore the complex area of Byzantine fault tolerance, influenced by the work of Lamport, Shostak, Pease, Bracha, and Toueg. We look at how these protocols are designed and how they operate. We carefully review how well they can handle different Byzantine fault situations and what effect they have on the system's overall performance and ability to grow. We aim to give a detailed and complete picture of these protocols, showing their strengths and weaknesses, and their importance in today's tech world.

Our study confirms the lasting importance of Bracha and Toueg’s work, as well as the groundbreaking contributions of Lamport, Shostak, and Pease, to the area of systems that can tolerate Byzantine faults. We examine how their ideas can be applied to current distributed systems and point out where more research and development could lead to better solutions. Our work not only recognizes the historical importance of their contributions but also looks forward to new ways to make distributed systems more robust and efficient in dealing with Byzantine faults.

In summary, our paper adds to the field of Byzantine fault tolerance by:

Taking a close look at the protocols for handling Byzantine faults developed by Bracha and Toueg, and relating them to the earlier work of Lamport, Shostak, and Pease.
Testing these protocols in different situations to see how they perform and understanding what this means for the system's dependability and ability to handle growth.
Comparing older and newer solutions for Byzantine fault tolerance to spot important trends, challenges, and opportunities for improvement in this crucial field of distributed computing.