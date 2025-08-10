from abc import ABC

class BaseProcessor(ABC):
  def __init__(self):
    # Keep a simple protected history store for processors that want it
    self._history = []

  def record(self, entry):
    # Record an event into the processor's history
    self._history.append(entry)

  @property
  def history(self):
    # Read-only view of the history
    return tuple(self._history)