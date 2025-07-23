import pickle

class FileIO:
    @staticmethod
    def load_keywords(filename, trie_processor):
        try:
            with open(filename, 'r') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        trie_processor.add_word(word)
            return f"Loaded keywords from {filename}"
        except Exception as e:
            return f"Error loading file: {e}"

    @staticmethod
    def export_keywords(filename, words):
        try:
            with open(filename, 'w') as f:
                for word, freq in words:
                    f.write(f"{word},{freq}\n")
            return f"Exported {len(words)} keywords to {filename}"
        except Exception as e:
            return f"Error exporting file: {e}"

    @staticmethod
    def restore_text_file(input_file, output_file, content):
        try:
            with open(output_file, 'w') as f:
                f.write(content)
            return f"Text saved to {output_file}"
        except Exception as e:
            return f"Error saving file: {e}"