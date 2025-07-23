from processors.trie_processor import TrieProcessor
import re

class TextProcessor:
    def __init__(self, trie_processor):
        self.trie = trie_processor
        self.restoration_history = []

    def restore_word(self, word, mode='best'):
        if '*' not in word:
            return word
        
        matches = self.trie.find_matches(word)
        if not matches:
            return word
        
        if mode == 'best':
            return f"<{matches[0][0]}>"
        else:
            options = [f"[{match[0]}]" for match in matches]
            return f"{word} {' '.join(options)}"

    def restore_text(self, text, mode='best'):
        tokens = re.findall(r"\w+'\w+|\w+|\W+", text)
        restored_tokens = []
        
        for token in tokens:
            if '*' in token:
                restored = self.restore_word(token, mode)
                self.restoration_history.append((token, restored))
                restored_tokens.append(restored)
            else:
                restored_tokens.append(token)
        
        return ''.join(restored_tokens)