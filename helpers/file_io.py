class FileIO:
  @staticmethod
  def load_keywords(filename, trie_processor):
    """
    Loads keywords from a file and adds them to the provided trie_processor.
    Clears the trie before loading new keywords.
    Supports both plain text format (one word per line) and CSV format (word,frequency).

    Args:
      filename (str): Path to the file containing keywords.
      trie_processor: An object with add_word(word) and clear_trie() methods.

    Returns:
      str: Status message indicating success or error.
    """
    try:
        # Clear the existing trie before loading new keywords
        trie_processor.clear_trie()

        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Check if line contains CSV format (word,frequency)
                if ',' in line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        word = parts[0].strip()
                        try:
                            frequency = int(parts[1].strip())
                            # Add the word once with its frequency value
                            trie_processor.add_word(word, frequency)
                        except ValueError:
                            # If frequency is invalid, treat the whole line as a word
                            trie_processor.add_word(line)
                    else:
                        # If not valid CSV format, treat whole line as word
                        trie_processor.add_word(line)
                else:
                    # Plain text format, just add the word
                    trie_processor.add_word(line)

        return f"Loaded keywords from {filename}"
    except Exception as e:
        return f"Error loading file: {e}"

  @staticmethod
  def export_keywords(filename, words):
    """
    Exports a list of (word, frequency) tuples to a file in CSV format.

    Args:
      filename (str): Path to the output file.
      words (list): List of (word, frequency) tuples.

    Returns:
      str: Status message indicating success or error.
    """
    try:
      with open(filename, 'w') as f:
        for word, freq in words:
          f.write(f"{word},{freq}\n")  # Write each word and its frequency
      return f"Exported {len(words)} keywords to {filename}"
    except Exception as e:
      return f"Error exporting file: {e}"

  @staticmethod
  def restore_text_file(filename, content):
    """
    Writes the provided content to the output file.

    Args:
      filename (str): Path to the file where content will be saved.
      content (str): The text content to write.

    Returns:
      str: Status message indicating success or error.
    """
    try:
      with open(filename, 'w') as f:
        f.write(content)  # Write the content to the output file
      return f"Text saved to {filename}"
    except Exception as e:
      return f"Error saving file: {e}"

  @staticmethod
  def save_trie(filename, trie_processor):
    """
    Saves the trie structure to a file in the same visual format as display_trie().

    Args:
      filename (str): Path to the file where trie will be saved.
      trie_processor: An object with a trie that has visualize() method.

    Returns:
      str: Status message indicating success or error.
    """
    try:
      import io
      import sys
      
      # Capture the output of the trie visualization
      old_stdout = sys.stdout
      sys.stdout = captured_output = io.StringIO()
      
      # Generate the trie visualization
      if trie_processor.trie.total_words == 0:
        captured_output.write("[]")
      else:
        trie_processor.trie.visualize()
      
      # Restore stdout and get the captured text
      sys.stdout = old_stdout
      trie_text = captured_output.getvalue()
      
      # Write to file
      with open(filename, 'w') as f:
        f.write(trie_text)
      
      return f"Trie saved to {filename}"
    except Exception as e:
      return f"Error saving trie: {e}"
