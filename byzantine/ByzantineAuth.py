import threading
import time
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from collections import defaultdict, Counter
import random

global_lock = threading.Lock()
global_node_count = 0
num_nodes = 0

class BANode(threading.Thread):
    """
    Represents a node in a Byzantine fault-tolerant network simulation.

    :param int node_id: Unique identifier for the node.
    :param list nodes: List of all nodes in the network.
    :param int k: Maximum number of communication pulses.
    :param bool is_general: True if the node is the general, otherwise False.
    :param bool is_byzantine: True if the node exhibits Byzantine behavior.
    """
    def __init__(self, node_id, nodes, k, is_general=False, is_byzantine= False):
        threading.Thread.__init__(self)
        self.node_id = node_id
        self.nodes = nodes
        self.k = k
        self.is_general = is_general
        self.is_byzantine = is_byzantine
        self.values_q = defaultdict(list)
        self.key = RSA.generate(2048)
        self.received_signatures = defaultdict(set)
        self.final_decision = None  # Attribute to store the final decision
        self.stop_event = threading.Event()



    def run(self):
        """
        Entry point for thread execution.
        Initializes the broadcast if the node is the general.
        """

        if self.is_general:
            time.sleep(1)  
            if self.is_byzantine:
                self.broadcast_initial_value(random.choice(["ACCEPT","REJECT"]), 0)
            else:
                self.broadcast_initial_value("ACCEPT", 0)
        while not self.stop_event.is_set():
            time.sleep(0.1)  
        

    def sign(self, data):
        """
        Signs data using the node's private RSA key.

        :param str data: The data to sign.
        :return: The digital signature.
        """
        hasher = SHA256.new(data.encode('utf-8'))
        signature = pkcs1_15.new(self.key).sign(hasher)
        return signature

    def verify_signature(self, data, signature, public_key):
        """
        Verifies a digital signature.

        :param str data: The data that was signed.
        :param signature: The signature to verify.
        :param public_key: The public key to use for verification.
        :return: True if the signature is valid, False otherwise.
        """
        hasher = SHA256.new(data.encode('utf-8'))
        try:
            pkcs1_15.new(public_key).verify(hasher, signature)
            return True
        except ValueError:
            return False

    def broadcast_initial_value(self, value, pulse):
        """
        Broadcasts the initial value from the general.

        :param str value: The value to broadcast.
        :param int pulse: The pulse number for this broadcast.
        """
        message = (value, [(self.node_id, self.sign(value))])
        self.broadcast_message(message, pulse , True)

    def broadcast_message(self, message, pulse, is_init = False):
        """
        Broadcasts a message to all other nodes.

        :param tuple message: The message to broadcast.
        :param int pulse: The current pulse number.
        """ 
        global global_node_count
        for node in self.nodes:
            if node.node_id != self.node_id:
                node.receive_message(message, pulse, is_init)
                global_node_count += 1
                    
            #print("\n")
    def receive_message(self, message, pulse, is_init = False):
        """
        Receives a message from another node.

        :param tuple message: The received message.
        :param int pulse: The pulse number when the message was sent.
        """
        value, signature_chain = message
        if self.validate_message(value, signature_chain) and pulse <= self.k:
            # Store the value if valid
            received_value = value if not self.is_byzantine else random.choice(["ACCEPT","REJECT"])
            self.values_q[pulse].append(received_value)
            if pulse < self.k:
                # Propagate the message to the next pulse with added signature

                next_pulse = pulse + 1
                new_signature_chain = signature_chain + [(self.node_id, self.sign(received_value))]
                new_message = (received_value, new_signature_chain)
                self.broadcast_message(new_message,next_pulse)
            elif pulse == (self.k ):

                self.decide()
                self.stop_event.set()  # Signal the run loop to stop


    def validate_message(self, value, signature_chain):
        """
        Validates a message's signature chain.

        :param str value: The message value.
        :param list signature_chain: The chain of (node_id, signature) tuples.
        :return: True if the message is valid, False otherwise.
        """
        # Check all signatures are valid and from distinct nodes

        seen_nodes = set()
        for node_id, signature in signature_chain:
            if node_id in seen_nodes:
                return False  # Prevents the same node from signing multiple times in a single chain
            if not self.verify_signature(value, signature, self.nodes[node_id].key.publickey()):
                return False  # Verification failed
            seen_nodes.add(node_id)
        return True  # All signatures are valid and from distinct nodes


    def decide(self):
        """
        Makes a final decision based on the received values at the last pulse.
        """
        # Retrieve the list of values received in the last pulse (communication round).
        last_pulse_values = self.values_q[self.k]
        decision_count = Counter(last_pulse_values)
        # Check if all values in the last pulse are the same (consensus reached).
        # The 'set' data structure is used to eliminate duplicates; if the set size is 1, all values are the same.

        decision, count = decision_count.most_common(1)[0]
        majority_threshold = (len(self.nodes) - 1) // 2 + 1
        for i in range(len(self.values_q)):
            print(f"{self.values_q[i]}, NODE : {self.node_id}")

        if count >= majority_threshold:  # all must agree
            temp_final_decision = 0
            if count >= majority_threshold:
                temp_final_decision = decision
            else:
                temp_final_decision = decision if not self.is_byzantine else random.choice(["ACCEPT", "REJECT"])
            self.final_decision = temp_final_decision


    def stop(self):
        """
        Stops the node's thread.
        """
        self.stop_event.set()

def setup_network(num_nodes, k, byzantine_nodes):
    nodes = []
    for i in range(num_nodes):
        is_general = (i == 0)
        is_byzantine = (i in byzantine_nodes)
        node = BANode(i, [], k, is_general, is_byzantine)
        nodes.append(node)
    for node in nodes:
        node.nodes = nodes  # Ensuring each node knows about all other nodes
    return nodes

def main():
    global num_nodes
    num_nodes = 4
    k = 1  # Number of pulses
    byzantine_nodes = {1}
    network = setup_network(num_nodes, k, byzantine_nodes)

    for node in network:
        node.start()

    for node in network:
        node.join()
    
    for node in network:
        print(f"Node {node.node_id} final decision: {node.final_decision}")

if __name__ == "__main__":
    main()