from processors.trie_processor import TrieProcessor
import re
import random

class TextProcessor:
  def __init__(self, trie_processor):
    # Store the trie processor instance for word restoration
    self.trie = trie_processor
    # Keep a history of restoration attempts (original, restored)
    self.restoration_history = []

  def restore_word(self, word, mode='best'):
    # If the word does not contain a wildcard, return as is
    if '*' not in word:
        return word

    # Find possible matches for the word with wildcards
    matches = self.trie.find_matches(word)
    if not matches:
        # If no matches found, return the original word
        return word

    if mode == 'best':
        # Return the best match (random among highest freq)
        max_freq = matches[0][1]
        top_matches = [w for w, f in matches if f == max_freq]
        return random.choice(top_matches)
    else:
        # Return all matches as ['opt1','opt2',...] format
        options = [f"'{match[0]}'" for match in matches]
        return f"[{','.join(options)}]"

  def restore_text(self, text, mode='best'):
    # Tokenize words including wildcards, apostrophes, and punctuation
    tokens = re.findall(r"[a-zA-Z0-9*']+|[^\w\s]|\n", text)
    restored_tokens = []

    for token in tokens:
        if '*' in token:
            # Restore words with wildcards and record the restoration
            restored = self.restore_word(token, mode)
            self.restoration_history.append((token, restored))
            if mode == 'best':
                # Wrap the best match with < >
                restored_tokens.append(f"<{restored}>")
            else:
                # Use the bracketed list format as returned by restore_word
                restored_tokens.append(restored)
        else:
            # Keep tokens without wildcards unchanged
            restored_tokens.append(token)

    # Reconstruct the text from the restored tokens
    restored_text = ""
    for i, token in enumerate(restored_tokens):
        if token == '\n':
            restored_text += token
        elif i > 0 and restored_tokens[i - 1] != '\n' and not re.match(r"[.,!?;:\)\]\}]", token):
            restored_text += " " + token
        else:
            restored_text += token
    return restored_text
