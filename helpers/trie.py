import random

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

  def insert(self, word, count=1):
    # Insert a word into the trie, updating prefix counts and frequency
    node = self.root
    for char in word:
      if char not in node.children:
        node.children[char] = TrieNode()
      node = node.children[char]
      node.prefix_count += count
    node.is_end = True
    node.frequency += count
    self.total_words += count

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

    if not matches:
        return []

    # Sort all matches by frequency descending, then alphabetically
    matches.sort(key=lambda x: (-x[1], x[0]))

    # Get max frequency *after sorting*
    max_freq = matches[0][1]

    # Split into top matches (same freq) and others
    top_matches = [pair for pair in matches if pair[1] == max_freq]
    other_matches = [pair for pair in matches if pair[1] < max_freq]

    # Shuffle only top matches to vary order
    random.shuffle(top_matches)

    # Return combined list
    return top_matches + other_matches

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

  def visualize(self, node=None, prefix=""):
    # Print a visual representation of the trie structure in bracket format
    if node is None:
      node = self.root
      print("[")
      self._print_trie_recursive(node, "", 1)
      print("]")
    else:
      self._print_trie_recursive(node, prefix, 1)
  
  def _print_trie_recursive(self, node, prefix, depth):
    # Recursive helper for printing trie structure
    for char, child in node.children.items():
      new_prefix = prefix + char
      indent = "." * depth
      
      if child.is_end and len(child.children) == 0:
        # If this is a complete word with no children, show it with the > marker
        print(f"{indent}>{new_prefix}({child.frequency})*")
      else:
        # If it has children, show it as a bracket (even if it's also a complete word)
        if child.is_end:
          print(f"{indent}[{new_prefix}({child.frequency})*")
        else:
          print(f"{indent}[{new_prefix}")
        
        # Recursively print children
        self._print_trie_recursive(child, new_prefix, depth + 1)
        
        # Close bracket
        print(f"{indent}]")