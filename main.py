"""Example how to use library workspan

Note
----
    To run this program use following syntax:
        python main.py input_file.json 5
"""
import sys

from workspan.settings import (
    MISSING_INPUT_FILE_NAME,
    MISSING_ENTITY_ID_MESSAGE
)

from workspan.graph import Graph
from workspan.clone import EntityCloner
from workspan.counter import Counter


def main(*args):
    """Every program shoud have starting point.
    This is more convention!

    Parameters
    ----------
    args: list
        list of arguments passed by cli
    """
    if len(args) < 2:
        sys.stderr.write(MISSING_INPUT_FILE_NAME)
        exit(1)
    if len(args) < 3:
        sys.stderr.write(MISSING_ENTITY_ID_MESSAGE)
        exit(2)
    input_file = args[1]
    entity_id = args[2]
    # initialize graph
    graph = Graph()
    # load file
    graph.load_from_file(input_file)
    # create counter (INT)
    counter = Counter(graph.get_last_id())
    # create entity cloner instance
    entity_id = (type(counter.value))(entity_id)
    cloner = EntityCloner(graph.find_entity_by_id(entity_id), counter)
    cloned_entity = cloner.clone()
    # add cloned entity to graph
    graph.add_entity(cloned_entity)
    # save results
    graph.save_to_file("result.json")


if __name__ == "__main__":
    main(*sys.argv)
