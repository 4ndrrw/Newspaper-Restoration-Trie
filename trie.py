class TrieNode:
  def __init__(self):
    # Each node has a dictionary of children, a flag for end of word,
    # a frequency counter, and a prefix counter for advanced features
    self.children = {}
    self.is_end = False
    self.frequency = 0
    self.prefix_count = 0  # For advanced features

class PrefixTrie:
  def __init__(self):
    # The trie starts with a root node and tracks total words inserted
    self.root = TrieNode()
    self.total_words = 0

  def insert(self, word):
    # Insert a word into the trie, updating prefix counts and frequency
    node = self.root
    for char in word:
      if char not in node.children:
        node.children[char] = TrieNode()
      node = node.children[char]
      node.prefix_count += 1
    node.is_end = True
    node.frequency += 1
    self.total_words += 1

  def search(self, word):
    # Check if a word exists in the trie
    node = self._get_node(word)
    return node.is_end if node else False

  def _get_node(self, word):
    # Helper to traverse the trie and return the node for a word/prefix
    node = self.root
    for char in word:
      if char not in node.children:
        return None
      node = node.children[char]
    return node

  def delete(self, word):
    # Delete a word from the trie, cleaning up unnecessary nodes
    nodes = []
    node = self.root
    for char in word:
      if char not in node.children:
        return False
      nodes.append((node, char))
      node = node.children[char]
    
    if not node.is_end:
      return False
      
    node.is_end = False
    self.total_words -= 1
    
    # Clean up nodes that are no longer needed
    for i in range(len(nodes)-1, -1, -1):
      parent, char = nodes[i]
      child = parent.children[char]
      if not child.is_end and len(child.children) == 0:
        del parent.children[char]
      else:
        break
    return True

  def get_all_words(self):
    # Return all words stored in the trie with their frequencies
    words = []
    self._dfs_collect(self.root, "", words)
    return words

  def _dfs_collect(self, node, prefix, words):
    # Helper for DFS traversal to collect words and their frequencies
    if node.is_end:
      words.append((prefix, node.frequency))
    for char, child in node.children.items():
      self._dfs_collect(child, prefix + char, words)

  def find_matches(self, pattern):
    # Find all words matching a pattern (supports '*' as wildcard)
    matches = []
    self._dfs_pattern_search(self.root, pattern, 0, "", matches)
    # Sort by frequency descending, then alphabetically
    return sorted(matches, key=lambda x: (-x[1], x[0]))

  def _dfs_pattern_search(self, node, pattern, index, current, matches):
    # Helper for DFS pattern search with wildcard support
    if index == len(pattern):
      if node.is_end:
        matches.append((current, node.frequency))
      return
    
    char = pattern[index]
    if char == '*':
      # Wildcard: try all children
      for child_char, child_node in node.children.items():
        self._dfs_pattern_search(child_node, pattern, index+1, current+child_char, matches)
    elif char in node.children:
      # Match specific character
      self._dfs_pattern_search(node.children[char], pattern, index+1, current+char, matches)

  def visualize(self, node=None, prefix="", last=True):
    # Print a visual representation of the trie structure
    if node is None:
      node = self.root
      
    marker = "└── " if last else "├── "
    end_marker = "*" if node.is_end else ""
    freq_str = f" (freq: {node.frequency})" if node.is_end else ""
    print(prefix + marker + end_marker + freq_str)
    
    prefix += "    " if last else "│   "
    children = list(node.children.items())
    
    for i, (char, child) in enumerate(children):
      last_child = i == len(children) - 1
      print(prefix + "│")
      print(prefix + "└── " + char + " → ", end="")
      self.visualize(child, prefix, last_child)