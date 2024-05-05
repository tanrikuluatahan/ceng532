.. include:: substitutions.rst

|byzantine|
=========================================



Background and Related Work
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Bracha-Toueg algorithm is foundational in Byzantine fault tolerance, allowing a system to reach consensus through a structured series of message exchanges, even when some participants act maliciously. It's designed to work in environments where up to one-third of the participants can be Byzantine.

The Lamport-Shostak-Pease algorithm, another cornerstone in this field, introduces the concept of Byzantine Generals' Problem, illustrating the challenges of achieving reliable consensus. This algorithm demonstrates how a system can reach agreement even when some participants are deliberately trying to undermine the process, provided that more than two-thirds of the participants are honest.

Distributed Algorithm: |byzantine| 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. An example distributed algorithm for broadcasting on an undirected graph is presented in  :ref:`Algorithm <Bracha-Toueg Byzantine Consensus Algorithm>`.

.. _Bracha-Toueg Byzantine Consensus Algorithm:

.. I reinterpreted the Original Bracha-Toueg Byzantine Consensus Algorithm 
.. with the help of the ChatGPT4. Prompt was copying the algorithm from the 
.. Wan Fokkink's book to the GPT, asking GPT to reinterpret it.
.. code-block:: RST
    :linenos:
    :caption: Bracha-Toueg Byzantine Consensus Algorithm



    procedure BrachaTouegByzantineConsensus(value)
        round := 1
        decided := false
        est := value                            // initial estimate of the value

        while not decided do

                                                //FIRST PHASE: Send initial value or 
                                                //current estimate to all

            send (est, round) to all

                                                // SECOND PHASE: Wait to receive 
                                                //messages from more than 2/3 of 
                                                //the processes

            values := receive_values_from_majority(round)

            if exists_common_value(values) then
                est := common_value(values)
            else
                est := default_value
            end if

                                                // Send the estimate to all after 
                                                //validation
            send (est, round) to all

                                                // THIRD PHASE: Wait to receive 
                                                //messages from more than 2/3 of 
                                                //the processes

            final_values := receive_values_from_majority(round)

            if count_same_value(final_values, est) > (2/3 * N) then
                                                // If the same value received from
                                                //more than 2/3 of the processes 
                                                //decide on est
                send (decide, est) to all
                decided := true
            end if

            round := round + 1
        end while

        return est
    end procedure

.. _Lamport-Shostak-Pease Authentication Algorithm:
.. I reinterpreted the Original Lamport-Shostak Pease Authentication Algorithm 
.. with the help of the ChatGPT4. Prompt was copying the algorithm from the 
.. Wan Fokkink's book to the GPT, asking GPT to reinterpret it.
.. code-block:: RST
    :linenos:
    :caption: Lamport-Shostak-Pease Authentication Algorithm

    procedure ByzantineGeneral(process_id, initial_value)
        return ByzantineAgreement(process_id, initial_value, 0)

    procedure ByzantineAgreement(process_id, value, level)
        if level >= M then
                                                // Base case: if maximum allowed faulty 
                                                //level is reached, return the value
            return value
        end if

                                                // FIRST PHASE: Send value to every process
        send value to all processes

                                                // SECOND PHASE: Receive values from all processes
        values := receive values from all processes

                                                // Prepare an array to store the majority 
                                                //value at the next level for each process
        next_level_values := []

        for each pid in processes do
            if pid is not process_id then
                                                // Recursive call to perform Byzantine
                                                //agreement for each value received
                next_level_values[pid] := ByzantineAgreement(pid, values[pid], level + 1)
            else
                next_level_values[pid] := value
            end if
        end for

                                                // THIRD PHASE: Determine the majority 
                                                //value among the received values
        majority_value := find_majority(next_level_values)

        return majority_value
    end procedure

    procedure find_majority(values)
                                                // Counts occurrences of each value 
                                                //and returns the one with the majority
        count_map := {}
        for each value in values do
            count_map[value] := count_map[value] + 1
        end for

        majority_value := key with max value in count_map
        return majority_value
    end procedure


.. Do not forget to explain the algorithm line by line in the text.

Example
~~~~~~~~

For the Bracha-Toueg Byzantine Consensus's, lets assume in a distributed system with four processes—Process A, B, C, and D, where D acts Byzantine—each process initiates with a value, aiming for consensus. A, B, and C start with true, while D, unpredictably, may start with false. During the first round, all processes broadcast their values; A, B, and C send true, but D, exploiting its Byzantine nature, sends conflicting values to disrupt consensus. In the collection phase, the non-Byzantine processes identify true as the majority value, despite D's attempts. They then broadcast true in a decision attempt. In the second round, they reaffirm true as the majority value, reaching a consensus, even as D continues its disruptive actions. This process illustrates the Bracha-Toueg Byzantine Consensus Algorithm's effectiveness, achieving consensus on true despite the presence of a Byzantine actor in the system.






For the Lamport-Shostak-Pease Authentication, lets assuma in a distributed system with four processes—Generals A, B, C, and D, where D acts as a traitor—the Lamport-Shostak-Pease algorithm aims for a unanimous decision among the loyal generals (A, B, and C) despite D’s misinformation. General A starts by proposing an action, say "attack," which is then communicated to all generals. Each general forwards what they received to the others, leading to a complex web of messages, including deceitful ones from D, such as sending "attack" to some and "retreat" to others. Through multiple rounds of communication, each general gathers these messages, applying majority rules to filter out inconsistencies and potential deceit. Despite D’s attempts to mislead, the consistent application of majority voting in each round enables the loyal generals to converge on a common decision, in this case, "attack." This illustrates the algorithm's ability to achieve consensus and coordinated action in the face of Byzantine behavior, ensuring the system’s integrity and decision-making resilience.


Correctness
~~~~~~~~~~~
// TODO IN LATER STAGES ^.^
Present Correctness, safety, liveness and fairness proofs.


Complexity 
~~~~~~~~~~

Present theoretic complexity results in terms of number of messages and computational complexity.








.. .. admonition:: EXAMPLE 

..    Snapshot algorithms are fundamental tools in distributed systems, enabling the capture of consistent global states during system execution. These snapshots provide insights into the system's behavior, facilitating various tasks such as debugging, recovery from failures, and monitoring for properties like deadlock or termination. In this section, we delve into snapshot algorithms, focusing on two prominent ones: the Chandy-Lamport algorithm and the Lai-Yang algorithm. We will present the principles behind these algorithms, their implementation details, and compare their strengths and weaknesses.

..    **Chandy-Lamport Snapshot Algorithm:**

..    The Chandy-Lamport [Lamport1985]_ , proposed by Leslie Lamport and K. Mani Chandy, aims to capture a consistent global state of a distributed system without halting its execution. It operates by injecting markers into the communication channels between processes, which propagate throughout the system, collecting local states as they traverse. Upon reaching all processes, these markers signify the completion of a global snapshot. This algorithm requires FIFO channels. There are no failures and all messages arrive intact and only once. Any process may initiate the snapshot algorithm. The snapshot algorithm does not interfere with the normal execution of the processes. Each process in the system records its local state and the state of its incoming channels.

..    1. **Marker Propagation:** When a process initiates a snapshot, it sends markers along its outgoing communication channels.
    2. **Recording Local States:** Each process records its local state upon receiving a marker and continues forwarding it.
    3. **Snapshot Construction:** When a process receives markers from all incoming channels, it captures its local state along with the incoming messages as a part of the global snapshot.
    4. **Termination Detection:** The algorithm ensures that all markers have traversed the system, indicating the completion of the snapshot.


    .. _ChandyLamportSnapshotAlgorithm:

    .. code-block:: RST
        :linenos:
        :caption: Chandy-Lamport Snapshot Algorithm [Fokking2013]_.
                
        bool recordedp, markerp[c] for all incoming channels c of p; 
        mess-queue statep[c] for all incoming channels c of p;

        If p wants to initiate a snapshot 
            perform procedure TakeSnapshotp;

        If p receives a basic message m through an incoming channel c0
        if recordedp = true and markerp[c0] = false then 
            statep[c0] ← append(statep[c0],m);
        end if

        If p receives ⟨marker⟩ through an incoming channel c0
            perform procedure TakeSnapshotp;
            markerp[c0] ← true;
            if markerp[c] = true for all incoming channels c of p then
                terminate; 
            end if

        Procedure TakeSnapshotp
        if recordedp = false then
            recordedp ← true;
            send ⟨marker⟩ into each outgoing channel of p; 
            take a local snapshot of the state of p;
        end if


    **Example**

    DRAW FIGURES REPRESENTING THE EXAMPLE AND EXPLAIN USING THE FIGURE. Imagine a distributed system with three processes, labeled Process A, Process B, and Process C, connected by communication channels. When Process A initiates a snapshot, it sends a marker along its outgoing channel. Upon receiving the marker, Process B marks its local state and forwards the marker to Process C. Similarly, Process C marks its state upon receiving the marker. As the marker propagates back through the channels, each process records the messages it sends or receives after marking its state. Finally, once the marker returns to Process A, it collects the markers and recorded states from all processes to construct a consistent global snapshot of the distributed system. This example demonstrates how the Chandy-Lamport algorithm captures a snapshot without halting the system's execution, facilitating analysis and debugging in distributed environments.


    **Correctness:**
    
    *Termination (liveness)*: As each process initiates a snapshot and sends at most one marker message, the snapshot algorithm activity terminates within a finite timeframe. If process p has taken a snapshot by this point, and q is a neighbor of p, then q has also taken a snapshot. This is because the marker message sent by p has been received by q, prompting q to take a snapshot if it hadn't already done so. Since at least one process initiated the algorithm, at least one process has taken a snapshot; moreover, the network's connectivity ensures that all processes have taken a snapshot [Tel2001]_.

    *Correctness*: We need to demonstrate that the resulting snapshot is feasible, meaning that each post-shot (basic) message is received during a post-shot event. Consider a post-shot message, denoted as m, sent from process p to process q. Before transmitting m, process p captured a local snapshot and dispatched a marker message to all its neighbors, including q. As the channels are FIFO (first-in-first-out), q received this marker message before receiving m. As per the algorithm's protocol, q took its snapshot upon receiving this marker message or earlier. Consequently, the receipt of m by q constitutes a post-shot event [Tel2001]_.

    **Complexity:**

    1. **Time Complexity**  The Chandy-Lamport  takes at most O(D) time units to complete where D is ...
    2. **Message Complexity:** The Chandy-Lamport  requires 2|E| control messages.


    **Lai-Yang Snapshot Algorithm:**

    The Lai-Yang algorithm also captures a consistent global snapshot of a distributed system. Lai and Yang proposed a modification of Chandy-Lamport's algorithm for distributed snapshot on a network of processes where the channels need not be FIFO. ALGORTHM, FURTHER DETAILS

.. .. [Fokking2013] Wan Fokkink, Distributed Algorithms An Intuitive Approach, The MIT Press Cambridge, Massachusetts London, England, 2013
.. .. [Tel2001] Gerard Tel, Introduction to Distributed Algorithms, CAMBRIDGE UNIVERSITY PRESS, 2001
.. .. [Lamport1985] Leslie Lamport, K. Mani Chandy: Distributed Snapshots: Determining Global States of a Distributed System. In: ACM Transactions on Computer Systems 3. Nr. 1, Februar 1985.