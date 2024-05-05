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

# Define the events and states
# Maybe other events come in v2
class EventType(Enum):
    """
    Defines the types of events that can occur in the Byzantine consensus algorithm.
    """
    VOTE = "VOTE"
    ECHO = "ECHO"
    DECIDE = "DECIDE"
    INIT = "INIT"

class State(Enum):
    """
    Represents the state of a Byzantine consensus node.
    """
    UNDECIDED = "UNDECIDED"
    DECIDED = "DECIDED"

# Base event data structure
class Event:
    """
    Base class for event data structure in Byzantine consensus process.

    :param event_type: The type of the event.
    :param source: The source node of the event.
    :param vote: The vote (if applicable) associated with the event.
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


    """
        Main execution loop of the node, processing incoming events until timeout.
        But it is going to be changed.
        """
    def run(self):
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
    ###

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
        Handles the INIT event. Typically used to start the voting process or acknowledge the initialization of other nodes.
        """
        with global_lock:
            if event.source != self:
                print(f"{self.name} acknowledges the initialization of {event.source.name}.")
            self.broadcast_vote()

    def on_vote(self, event):
        """
        Handles a VOTE event, either by echoing the vote or sending randomized votes if Byzantine.

        :param event: The event containing the vote to handle.
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

    # '''
    #  implement also a function that when a node receives a message from other nodes,
    #  it should echo that message in a broadcast manner and wait for the n("all nodes")/2
    #  confirmation echoes ,which tells the current node whether the same message
    #  had arrived from the same source to other different nodes, then process that message
    # '''

    def on_echo(self, event):
        global byzantine_count
        """
        Handles an ECHO event, counting votes and deciding if a majority is reached.

        :param event: The event containing the echo to handle.
        """
        if self.state == State.DECIDED:
            return

        # Count the echoes come from other nodes and decide if there is a majority
        with global_lock:
            self.echo_counts[event.vote] += 1
            for vote, count in self.echo_counts.items():
                if count > (len(self.nodes.keys()) + byzantine_count) / 2:
                    # print(self.nodes.values())
                    # print(self.name)
                    # print(vote,count)
                    self.decide(vote)

    def on_decide(self, event):
        """
        Handles a DECIDE event, finalizing the decision.

        :param event: The event containing the decision to finalize.
        """

        # if self.state == State.DECIDED:
        #     return
        #print(f"RET: {event.source.name}")
        #print(f'Event source name: {event.source.name} decided on value {event.vote}')
        #self.decide(event.vote)

    def decide(self, vote):
        """
        Finalizes the decision for this node based on received votes.

        :param vote: The majority vote that leads to a decision.
        """
        self.state = State.DECIDED
        self.decided_value = vote
        self.broadcast(EventType.DECIDE, vote=vote)
        print(f'{self.name} decided on value {self.decided_value}')
        return

    def broadcast_vote(self):
        """
        Broadcasts the node's vote to other processes.
        """
        global node_count
        if global_inited_count != node_count:
            sleep(0.05)
        
        if not self.is_byzantine:
            self.broadcast(EventType.VOTE, vote=self.vote)

    def broadcast(self, event_type, vote):
        """
        Broadcasts an event to all other nodes except itself.

        :param event_type: The type of the event to broadcast.
        :param vote: The vote to include in the event, if applicable.
        """
        for component in  self.nodes.values():
            if component.name != self.name:
                event = Event(event_type, self, vote=vote)
                component.queue.put(event)

def setup_simulation():
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
