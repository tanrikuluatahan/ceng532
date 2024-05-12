from enum import Enum
from adhoccomputing.Generics import EventTypes, Event
from adhoccomputing.GenericModel import GenericModel, GenericMessageHeader, GenericMessage
import networkx as nx
import random
import csv

byzantine_count = 4
# Bright Colors
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

def log_message_to_csv(source_node, message, delivered_node, filename='ByzantineConsensus.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([source_node, message, delivered_node])

class ApplicationLayerMessageTypes(Enum):
    """
    Enumeration for the types of events that can occur in the Byzantine consensus algorithm.
    """
    VOTE = "VOTE"
    ECHO = "ECHO"
    DECIDE = "DECIDE"
    INIT = "INIT"

# Base event data structure
class ModEvent:
    """
    Represents an event in the Byzantine consensus process.

    :param EventType event_type: The type of the event.
    :param source: The node that originated the event.
    :param int vote: The vote associated with the event, if applicable.
    """
    def __init__(self, event_type, source, vote=None):
        self.event_type = event_type
        self.source = source
        self.vote = vote

class State(Enum):
    """
    Enumeration for possible states of a Byzantine consensus node.
    """
    UNDECIDED = "UNDECIDED"
    DECIDED = "DECIDED"


class BCNode(GenericModel):
    """
    Initializes a Byzantine Consensus node within a distributed network simulation based on the Byzantine Generals Problem.

    :param str componentname: The name of the component.
    :param int componentinstancenumber: A unique identifier for this instance of the component, used as the node's name.
    :param list nodes: A list of all nodes in the network.
    :param context: The environment or context in which the node operates (optional).
    :param configurationparamters: Configuration parameters specific to the node's setup (optional).
    :param int num_worker_threads: The number of worker threads for this node (optional).
    :param nx.Graph topology: The network topology as a graph where nodes are processes and edges represent communication links (optional).

    Attributes:
        queue (Queue): The queue used for message handling within the node.
        name (int): The identifier of the node, usually matches the component instance number.
        nodes (list): The list of all other nodes in the network this node can communicate with.
        num_of_decided (int): A counter to track how many nodes have decided on a value.
        state (State): The current state of the node, initially set to UNDECIDED.
        vote (int): The initial vote of the node, randomly chosen between predefined options.
        echo_counts (dict): A dictionary to count echoes for each possible vote.
        decide_counts (dict): A dictionary to count decisions for each possible vote.
        is_byzantine (bool): Indicates if the node can perform Byzantine (faulty) actions.
        flag (bool): A general-purpose flag used for various checks and conditions within the node.
        event_handlers (dict): Event handlers mapping event types to corresponding methods.
        decided_value (Any): The final decision made by the node if it reaches a consensus.

    This class represents a node capable of participating in Byzantine fault-tolerant consensus algorithms, handling different types of messages, and deciding on values based on majority rules or received commands.
    """
    def __init__(self, componentname, componentinstancenumber, nodes, context=None, configurationparamters=None, num_worker_threads=1, topology: nx.Graph = None):
        
        super().__init__(componentname, componentinstancenumber,context,configurationparamters, num_worker_threads, topology)

        self.queue = None
        self.name = self.componentinstancenumber
        self.nodes = nodes
        self.num_of_decided = 0
        self.state = State.UNDECIDED
        self.vote = random.choice([0, 1])
        self.echo_counts = {0: 0, 1: 0}
        self.decide_counts = {0: 0, 1: 0}
        self.is_byzantine = False
        self.flag = False
        self.event_handlers = {
            ####
            ApplicationLayerMessageTypes.VOTE: self.on_vote,
            ApplicationLayerMessageTypes.ECHO: self.on_echo,
            ApplicationLayerMessageTypes.DECIDE: self.on_decide,
            ApplicationLayerMessageTypes.INIT: self.on_init,
            ####
        }
        self.decided_value = None

    def on_message_from_bottom(self, eventobj: Event):
        message = eventobj.eventcontent
        modMessage = message.payload
        hdr = message.header
        COLOR = ''
        if modMessage.event_type == ApplicationLayerMessageTypes.INIT:
            COLOR = BRIGHT_GREEN
        elif modMessage.event_type == ApplicationLayerMessageTypes.VOTE:
            COLOR = BRIGHT_YELLOW
        elif modMessage.event_type == ApplicationLayerMessageTypes.ECHO:
            COLOR = BRIGHT_CYAN
        elif modMessage.event_type == ApplicationLayerMessageTypes.DECIDE:
            COLOR = BRIGHT_RED
        #print(f"{COLOR}Message arrived to Node: {self.componentinstancenumber}\n\tMessage:\n\t\tModEvent Type: {modMessage.event_type}\n\t\tSource Node: {modMessage.source.componentinstancenumber}\n\t\tVote: {modMessage.vote}{RESET}\n")
        log_message_to_csv(modMessage.source.name, f'Event Type: {modMessage.event_type} | Vote: {modMessage.vote} ', self.name)
        self.handle_event(modMessage,hdr)

    def handle_event(self, event, hdr):
        """
        Handles an incoming event based on its type.

        :param event: The event to handle.
        """
        if hdr.messagetype == ApplicationLayerMessageTypes.VOTE:
            self.on_vote(event)
        elif hdr.messagetype == ApplicationLayerMessageTypes.ECHO:
            self.on_echo(event)
        elif hdr.messagetype == ApplicationLayerMessageTypes.DECIDE:
            self.on_decide(event)

    def prepare_payload(self, msg_type, destination, payload):
        hdr = GenericMessageHeader(msg_type,self.componentinstancenumber,destination)
        msg = GenericMessage(hdr,payload)
        return msg


    def on_init(self, eventobj: Event):
        """
        Handles the INIT event, either by starting the voting process or acknowledging other nodes' initialization.

        :param Event event: The event instance.
        """
        self.broadcast(ApplicationLayerMessageTypes.VOTE, vote=self.vote)

    def on_vote(self, event):
        """
        Handles a VOTE event by either echoing the vote directly or, if Byzantine, potentially altering the vote before echoing.

        :param Event event: The event containing the vote.
        """
        if self.state == State.DECIDED:
            return

        if self.is_byzantine:
            # send different votes to different processes randomly from byzantine node
            vote = random.choice([0, 1])
            #event = ModEvent(ApplicationLayerMessageTypes.ECHO, self, vote=vote)
            self.broadcast(ApplicationLayerMessageTypes.ECHO, vote=vote)
        else:
            # Echo the current node's vote to other processes
            self.broadcast(ApplicationLayerMessageTypes.ECHO, vote=event.vote)

    def on_echo(self, event):
        """
        Handles an ECHO event by counting received echoes and deciding if a majority has been reached.

        :param Event event: The event containing the echo.
        """
        # Count the echoes come from other nodes and decide if there is a majority

        global byzantine_count
        self.echo_counts[event.vote] += 1
        for vote, count in self.echo_counts.items():
            if count > (len(self.nodes) + byzantine_count) / 2:
                self.decide(vote)

    def on_decide(self, event):
        
        if self.flag:
            return
        self.decide_counts[event.vote] += 1
        self.num_of_decided += 1
        majority_threshold = (len(self.nodes) - 1) // 2 + 1
        if self.num_of_decided >= majority_threshold:
            self.flag = True
            majority_decision = None
            if self.decide_counts[1] > self.decide_counts[0]:
                majority_decision = 1
            elif self.decide_counts[1] < self.decide_counts[0]:
                majority_decision = 0
            elif self.decide_counts[1] == self.decide_counts[0]:
                pass
            print(f'{BRIGHT_WHITE}Node : {self.name} decided on value : {majority_decision}{RESET}\n')
    
    def decide(self, vote):
        """
        Finalizes the decision based on the most common received vote.

        :param int vote: The vote that this node has decided upon.
        """

        if self.state == State.DECIDED:
            return
        self.decided_value = vote
        self.state = State.DECIDED
        self.broadcast(ApplicationLayerMessageTypes.DECIDE, vote=vote)
        return
    
    def broadcast(self, event_type, vote):
        """
        Sends an event to all other nodes.

        :param EventType event_type: The type of the event to broadcast.
        :param int vote: The vote to be included in the broadcast, if applicable.
        """

        for component in self.nodes:
            if component.name != self.name:
                if self.is_byzantine:
                    vote = random.choice([0, 1])
                event = ModEvent(event_type, self, vote=vote)
                msg = self.prepare_payload(event_type, component.name,event )
                self.send_down(Event(self,EventTypes.MFRT,msg))