from enum import Enum
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto import Random
import collections

class ByzantineAuthMessageType(Enum):
    """
    Enumeration for Byzantine authentication message types.
    """
    VOTE = "VOTE"
    ECHO = "ECHO"
    DECIDE = "DECIDE"

class ByzantineAuthMessage:
    """Represents a message within the Byzantine authentication system.

    :param message_type: The type of message (e.g., VOTE, ECHO, DECIDE)
    :param sender_id: Identifier for the sender of the message
    :param payload: The content of the message
    :param signature: The digital signature of the message (optional)
    """
    def __init__(self, message_type, sender_id, payload, signature=None):
        self.message_type = message_type
        self.sender_id = sender_id
        self.payload = payload
        self.signature = signature

    def __str__(self):
        return f"{self.message_type} from {self.sender_id} with payload {self.payload}"


class BANode:
    """
    A node in the Byzantine authentication system.

    :param process_id: The identifier of the process
    :param is_byzantine: A boolean flag to indicate if the node behaves in a Byzantine manner (default False)
    """
    def __init__(self, process_id, is_byzantine=False):
        self.process_id = process_id
        self.is_byzantine = is_byzantine
        self.keys = RSA.generate(2048)
        self.public_key = self.keys.publickey()
        self.decisions = {}
        self.messages = []

    # take the message hash and sign the hash 
    # with self.keys 
    
    def sign_message(self, message):
        """
        Signs a message using the node's private key.

        :param message: The message to be signed
        :return: The digital signature of the message
        """
        hasher = SHA256.new(str(message).encode('utf-8'))
        return pkcs1_15.new(self.keys).sign(hasher)

    def verify_message(self, message, signature, public_key):
        """
        Verifies a signed message using the provided public key.

        :param message: The message to be verified
        :param signature: The digital signature of the message
        :param public_key: The public key to be used for verification
        :return: True if the verification is successful, otherwise False
        """
        hasher = SHA256.new(str(message).encode('utf-8'))
        try:
            pkcs1_15.new(public_key).verify(hasher, signature)
            return True
        except (ValueError, TypeError):
            return False

    def create_signed_message(self, message_type, payload):
        """
        Creates and signs a message.

        :param message_type: The type of the message
        :param payload: The content of the message
        :return: The signed message object
        """
        message = ByzantineAuthMessage(message_type, self.process_id, payload)
        signature = self.sign_message(message)
        message.signature = signature
        return message

    def receive_message(self, message : ByzantineAuthMessage, sender_public_key):
        # Verify the message signature
        """
        Receives and processes a message from another node.

        :param message: The received message
        :param sender_public_key: The public key of the sender for verification
        """
        if not self.verify_message(message, message.signature, sender_public_key):
            print(f"Process {self.process_id} received an invalid message from {message.sender_id}")
            return
        
        print(f"Process {self.process_id} received a valid message: {message}")
        self.messages.append(message)
        # Handle message based on its type
        if message.message_type == ByzantineAuthMessageType.VOTE:
            self.handle_vote(message)
        elif message.message_type == ByzantineAuthMessageType.ECHO:
            self.handle_echo(message)
        elif message.message_type == ByzantineAuthMessageType.DECIDE:
            self.handle_decision(message)

    def broadcast(self, message : ByzantineAuthMessage, all_processes):
        """
        Broadcasts a message to all other processes except itself.

        :param message: The message to be broadcasted
        :param all_processes: A dictionary of all processes
        """
        for process in all_processes.values():
            if process.process_id != self.process_id:
                process.receive_message(message, self.public_key)

    def handle_vote(self, message : ByzantineAuthMessage):
        """
        Handles the voting message by creating and broadcasting an ECHO message.

        :param message: The received VOTE message
        """
        echo_message = self.create_signed_message(ByzantineAuthMessageType.ECHO, message.payload)
        self.broadcast(echo_message, '''all processess''')

    def handle_echo(self, message : ByzantineAuthMessage):
        """
        Handles an ECHO message by broadcasting it further.

        :param message: The received ECHO message
        """
        # Each process echoes the message to others
        self.broadcast(message, '''all processess''')

    def handle_decision(self, message : ByzantineAuthMessage):
        """
        Handles a DECIDE message based on a consensus mechanism.
        """
        # Decide based on consensus
        self.decide()

    def decide(self):
        """
        Determines the consensus based on the most common decision among received messages and decides accordingly.
        """
        decision_counter = collections.Counter([msg.payload for msg in self.messages])
        decision, count = decision_counter.most_common(1)[0]
        if count >= (len('''all processess''') + 1) // 2:
            self.decisions[self.process_id] = decision
            print(f"Process {self.process_id} decided on: {decision}")
            decision_message = self.create_signed_message(ByzantineAuthMessageType.DECIDE, decision)
            self.broadcast(decision_message, '''all processess''')