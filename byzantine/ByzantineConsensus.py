from enum import Enum, auto
from queue import Queue, Empty
from threading import Thread
from time import sleep
import random
from threading import Lock


global_lock = Lock()

byzantine_count = 0
node_count = 0
global_inited_count = 0


class EventType(Enum):
    """
    Enumeration for the types of events that can occur in the Byzantine consensus algorithm.
    """
    VOTE = "VOTE"
    ECHO = "ECHO"
    DECIDE = "DECIDE"
    INIT = "INIT"

class State(Enum):
    """
    Enumeration for possible states of a Byzantine consensus node.
    """
    UNDECIDED = "UNDECIDED"
    DECIDED = "DECIDED"

# Base event data structure
class Event:
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
        #self.echo_votes = []

# ByzantineConsensusNode
class BCNode(Thread):
    ### by default node is not byzantine
    """
    Represents a node in the Byzantine consensus algorithm.

    :param name: The name of the node.
    :param is_byzantine: A flag to indicate if the node is Byzantine (i.e., it can perform malicious actions).
    """
    def __init__(self, name, nodes, is_byzantine=False):
        Thread.__init__(self)
        self.name = name
        self.queue = Queue()
        self.is_byzantine = is_byzantine
        self.state = State.UNDECIDED
        ### randomized voting procedure
        self.vote = random.choice([0, 1])
        self.nodes = nodes
        self.echo_counts = {0: 0, 1: 0}
        self.event_handlers = {
            ####
            EventType.VOTE: self.on_vote,
            EventType.ECHO: self.on_echo,
            EventType.DECIDE: self.on_decide,
            EventType.INIT: self.on_init,
            ####
        }
        self.decided_value = None


    
    def run(self):
        """
        Main execution loop of the node, processing incoming events until timeout.
        """
        with global_lock:
            self.send_init()
        while True:
            try:
                event = self.queue.get(timeout=3)  # Timeout for simulation
                self.handle_event(event)
            except Empty:
                if self.state == State.UNDECIDED:
                    print(f"{self.name} timed out without deciding.")
                break


    def handle_event(self, event):
        """
        Handles an incoming event based on its type.

        :param event: The event to handle.
        """
        if event.event_type == EventType.INIT:
            self.broadcast_vote()
        elif event.event_type == EventType.VOTE:
            self.on_vote(event)
        elif event.event_type == EventType.ECHO:
            self.on_echo(event)
        elif event.event_type == EventType.DECIDE:
            self.on_decide(event)

    def send_init(self):
        """ Broadcasts an INIT event to all nodes including itself to start the voting process. """
        init_event = Event(EventType.INIT, self)
        global global_inited_count
        global_inited_count += 1
        self.broadcast(EventType.INIT, self.vote)


    def on_init(self, event):
        """
        Handles the INIT event, either by starting the voting process or acknowledging other nodes' initialization.

        :param Event event: The event instance.
        """
        with global_lock:
            if event.source != self:
                print(f"{self.name} acknowledges the initialization of {event.source.name}.")
            self.broadcast_vote()

    def on_vote(self, event):
        """
        Handles a VOTE event by either echoing the vote directly or, if Byzantine, potentially altering the vote before echoing.

        :param Event event: The event containing the vote.
        """
        if self.state == State.DECIDED:
            return

        if self.is_byzantine:
            # send different votes to different processes randomly from byzantine node
            for component in self.nodes.values():
                vote = random.choice([0, 1])
                event = Event(EventType.ECHO, self, vote=vote)
                component.queue.put(event)
        else:
            # Echo the current node's vote to other processes
            self.broadcast(EventType.ECHO, vote=event.vote)



    def on_echo(self, event):
        global byzantine_count
        """
        Handles an ECHO event by counting received echoes and deciding if a majority has been reached.

        :param Event event: The event containing the echo.
        """
        if self.state == State.DECIDED:
            return

        # Count the echoes come from other nodes and decide if there is a majority
        with global_lock:
            self.echo_counts[event.vote] += 1
            for vote, count in self.echo_counts.items():
                if count > (len(self.nodes.keys()) + byzantine_count) / 2:
                    self.decide(vote)


    def decide(self, vote):
        """
        Finalizes the decision based on the most common received vote.

        :param int vote: The vote that this node has decided upon.
        """
        self.state = State.DECIDED
        self.decided_value = vote
        self.broadcast(EventType.DECIDE, vote=vote)
        print(f'{self.name} decided on value {self.decided_value}')
        return

    def broadcast_vote(self):
        """
        Broadcasts the node's initial vote to all other nodes.
        """
        global node_count
        if global_inited_count != node_count:
            sleep(0.05)
        
        if not self.is_byzantine:
            self.broadcast(EventType.VOTE, vote=self.vote)

    def broadcast(self, event_type, vote):
        """
        Sends an event to all other nodes.

        :param EventType event_type: The type of the event to broadcast.
        :param int vote: The vote to be included in the broadcast, if applicable.
        """
        for component in  self.nodes.values():
            if component.name != self.name:
                event = Event(event_type, self, vote=vote)
                component.queue.put(event)

def setup_simulation():
    """
    Initializes and starts a network of nodes participating in the Byzantine consensus algorithm.
    """
    global byzantine_count, node_count
    nodes = {name: BCNode(name, None, is_byzantine=(name == 'Node3')) for name in ['Node1', 'Node2', 'Node3', 'Node4','Node5', 'Node6', 'Node7', 'Node8', 'Node9', 'Node10', 'Node11', 'Node12','Node13']}
    nodes['Node4'].is_byzantine = True
    nodes['Node10'].is_byzantine = True
    node_count = len(nodes.keys())
    byzantine_count += 3
    for node in nodes.values():
        node.nodes = nodes  # Set the reference to all nodes for each node
    for node in nodes.values():
        node.start()  # Starting the node thread will trigger its own initialization

if __name__ == '__main__':
    setup_simulation()
