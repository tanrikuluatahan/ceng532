from enum import Enum
from adhoccomputing.Generics import EventTypes, Event
from adhoccomputing.GenericModel import GenericModel, GenericMessageHeader, GenericMessage
import networkx as nx
from time import sleep
from collections import defaultdict, Counter
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import csv
from Crypto.Hash import SHA256
import random

BRIGHT_BLACK = "\033[0;90m"   # Black (Bright)
BRIGHT_RED = "\033[0;91m"     # Red (Bright)
BRIGHT_GREEN = "\033[0;92m"   # Green (Bright)
BRIGHT_YELLOW = "\033[0;93m"  # Yellow (Bright)
BRIGHT_BLUE = "\033[0;94m"    # Blue (Bright)
BRIGHT_MAGENTA = "\033[0;95m" # Magenta (Bright)
BRIGHT_CYAN = "\033[0;96m"    # Cyan (Bright)
BRIGHT_WHITE = "\033[0;97m"   # White (Bright)
# Reset Color
RESET = "\033[0m"  # Reset to default terminal color

def log_message_to_csv(source_node, message, signature_chain, delivered_node, pulse, filename='ByzantineAuth.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([source_node, message, signature_chain ,delivered_node, pulse])


class BANode(GenericModel):
    """
    Initializes a Byzantine Agreement node within a distributed network simulation.

    :param str componentname: The name of the component.
    :param int componentinstancenumber: A unique identifier for this instance of the component.
    :param list nodes: A list of all nodes in the network.
    :param int k: The maximum number of communication rounds or pulses.
    :param bool is_general: Indicates whether this node acts as the general.
    :param bool is_byzantine: Flags whether this node can exhibit Byzantine (faulty) behavior.
    :param context: The environment or context in which the node operates (optional).
    :param configurationparamters: Configuration parameters specific to the node's setup (optional).
    :param int num_worker_threads: The number of worker threads for this node (optional).
    :param nx.Graph topology: The network topology as a graph where nodes are processes and edges represent communication links (optional).

    Attributes:
        node_id (int): An identifier that matches the component instance number, used for addressing the node within the network.
        general_id (int): Identifier of the general node, typically set to 0 by default.
        round_count (int): A counter to track the number of communication rounds that have been executed.
        values_q (defaultdict(list)): A dictionary to store values by rounds, collected from messages.
        is_decided (bool): Flag to check if the node has made a final decision.
        key (RSA key): A generated RSA key for signing and verifying messages.
        received_signatures (defaultdict(set)): Stores signatures received to prevent replay and ensure message integrity.
        final_decision (Any): Stores the final decision made after concluding the agreement process.
    """
    def __init__(self, componentname, componentinstancenumber, nodes, k , is_general, is_byzantine, context=None, configurationparamters=None, num_worker_threads=1, topology: nx.Graph = None):
        
        super().__init__(componentname, componentinstancenumber,context,configurationparamters, num_worker_threads, topology)
        self.node_id = componentinstancenumber
        self.nodes = nodes
        self.k = k
        self.general_id = 0
        self.round_count = 0
        self.is_general = is_general
        self.is_byzantine = is_byzantine
        self.values_q = defaultdict(list)
        self.is_decided = False
        self.key = RSA.generate(2048)
        self.received_signatures = defaultdict(set)
        self.final_decision = None  # Attribute to store the final decision

    def prepare_payload(self, msg_type, destination, payload):
        """
        Prepares a payload for transmission within the network by wrapping it into a generic message structure.

        :param str msg_type: The type of the message, determining how it should be handled by receiving nodes.
        :param int destination: The identifier of the destination node to which the message is being sent.
        :param any payload: The actual data to be sent, which can be of any type that needs to be encapsulated within the message.

        :return: A fully formed GenericMessage object ready for transmission.
        """
        hdr = GenericMessageHeader(msg_type,self.componentinstancenumber,destination)
        msg = GenericMessage(hdr,payload)
        return msg

    def on_message_from_bottom(self, eventobj: Event):
        message = eventobj.eventcontent
        inner_message = message.payload
        hdr = message.header
        self.receive_message(inner_message)
        #COLOR = ''

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
        
    def on_init(self, eventobj: Event):
        """
        Broadcasts the initial value from the general.

        :param str value: The value to broadcast.
        :param int pulse: The pulse number for this broadcast.
        """
        if self.is_general:
            if self.is_byzantine:
                value = random.choice(["ACCEPT","REJECT"])
            else:
                value = "ACCEPT"
            pulse = 0 
            message = (value, pulse ,[(self.node_id, self.sign(value))])
            self.broadcast_message(message, True)
        else:
            pass

    def broadcast_message(self, message, is_init = False):
        """
        Broadcasts a message to all other nodes.

        :param tuple message: The message to broadcast.
        :param int pulse: The current pulse number.
        """ 
       # global global_node_count
        for node in self.nodes:
            if is_init:
                node.general_id = message[2][0][1]
            if node.node_id != self.node_id:
                msg = self.prepare_payload("temp", node.node_id, message )
                # print(f"{BRIGHT_RED}{msg}{RESET}")
                self.send_down(Event(self,EventTypes.MFRT,msg))
                    
    def receive_message(self, message, is_init = False):
        """
        Receives a message from another node.

        :param tuple message: The received message.
        :param int pulse: The pulse number when the message was sent.
        """
        value, pulse,  signature_chain = message
        source_id = signature_chain[-1][0] if signature_chain else "Unknown"
        new_signature_chain = 0
        log_message_to_csv(source_id, value, [i[0] for i in signature_chain], self.node_id, pulse)
        if self.validate_message(value, signature_chain):
            
            # Store the value if valid
            received_value = value
            #
            self.values_q[self.round_count].append(received_value)
            if  self.round_count < self.k - 1:
                # Propagate the message to the next pulse with added signature
                next_pulse = self.round_count 
                self.round_count += 1
                received_value = value if not self.is_byzantine else random.choice(["ACCEPT","REJECT"])
                new_signature_chain = signature_chain + [(self.node_id, self.sign(received_value))]
                new_message = (received_value, next_pulse ,new_signature_chain)
                self.broadcast_message(new_message)
            elif  self.round_count == (self.k - 1):
                #self.round_count += 1
                self.decide()
            if pulse == self.round_count:
                print(f"ROUND COUNT: {self.round_count} of NODE : {self.node_id}\n")
                self.round_count += 1
        else:
            #discard
            # self.round_count += 1
            print("DISCARD")
            pass     


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
                print(f"{BRIGHT_RED}DUPLICATE SIGN{RESET}\n")
                return False  # Prevents the same node from signing multiple times in a single chain
            if not self.verify_signature(value, signature, self.nodes[node_id].key.publickey()):
                print(f"{BRIGHT_RED}VERIFICATION FAILED{RESET}\n")
                return False  # Verification failed
            seen_nodes.add(node_id)
        return True  # All signatures are valid and from distinct nodes


    def decide(self):
        """
        Makes a final decision based on the received values at the last pulse.
        """
        if self.is_decided:
            return
        # Retrieve the list of values received in the last pulse (communication round).
        last_pulse_values = self.values_q[self.round_count]
        decision_count = Counter(last_pulse_values)
        # Check if all values in the last pulse are the same (consensus reached).
        # The 'set' data structure is used to eliminate duplicates; if the set size is 1, all values are the same.

        decision, count = decision_count.most_common(1)[0]
        #majority_threshold = (len(self.nodes) - 1) // 2 + 1
        self.final_decision = decision
        
        try:
            print(f"{BRIGHT_GREEN}NODE {self.componentinstancenumber} decided on {self.final_decision}{RESET}\n")
        except:
            print("HERE FAILED")
        #sleep(0.5)
        self.is_decided = True
            

    