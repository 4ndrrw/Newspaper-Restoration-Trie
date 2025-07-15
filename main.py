import os
import sys
from trie import PrefixTrie
from text_restorer import TextRestorer

class Application:
  def __init__(self):
    # Initialize the trie and text restorer
    self.trie = PrefixTrie()
    self.restorer = TextRestorer(self.trie)
    self.current_trie_file = None
    self.running = True
  
  def clear_screen(self):
    # Clear the terminal screen for better UI
    os.system('cls' if os.name == 'nt' else 'clear')
  
  def display_header(self):
    # Display the application header/banner
    self.clear_screen()
    print("*******************************************************")
    print("* ST1507 DSAA: Predictive Text Editor (using tries)   *")
    print("* -------------------------------------------------- *")
    print("* - Done by: [Your Name1](ID1) & [Your Name2](ID2)   *")
    print("* - Class [Your Class]                                *")
    print("*******************************************************")
  
  def display_main_menu(self):
    # Show the main menu options
    self.display_header()
    print("\nMain Menu\n")
    print("1. Construct/Edit Trie")
    print("2. Predict/Restore Text")
    print("3. Extra Feature One")
    print("4. Extra Feature Two")
    print("5. Extra Feature Three")
    print("6. Extra Feature Four")
    print("7. Exit")
  
  def trie_edit_menu(self):
    # Menu for constructing and editing the trie
    while True:
      self.display_header()
      print("\nConstruct/Edit Trie Commands:")
      print("'+word' - Add a keyword")
      print("-word' - Delete a keyword")
      print("?word' - Find a keyword")
      print("# - Display Trie")
      print("@ - Write Trie to file")
      print("~ - Read keywords from file")
      print("= - Write keywords to file")
      print("! - Print instructions")
      print("\ - Exit to main menu")
      
      command = input("\n> ").strip()
      
      if not command:
        continue
        
      cmd = command[0]
      arg = command[1:].strip()
      
      if cmd == '+':
        # Add a word to the trie
        self.trie.insert(arg.lower())
        print(f"Added '{arg}' to trie")
      elif cmd == '-':
        # Delete a word from the trie
        if self.trie.delete(arg.lower()):
          print(f"Deleted '{arg}' from trie")
        else:
          print(f"'{arg}' not found in trie")
      elif cmd == '?':
        # Search for a word in the trie
        if self.trie.search(arg.lower()):
          print(f"'{arg}' is present in trie")
        else:
          print(f"'{arg}' is not present in trie")
      elif cmd == '#':
        # Visualize the trie structure
        print("\nTrie Structure:")
        self.trie.visualize()
      elif cmd == '@':
        # Save the trie structure to a file (to be implemented)
        self._save_trie_to_file()
      elif cmd == '~':
        # Load keywords from a file
        self._load_keywords_from_file()
      elif cmd == '=':
        # Export keywords to a file
        self._export_keywords_to_file()
      elif cmd == '!':
        # Print instructions (just redisplay)
        continue
      elif cmd == '\\':
        # Exit to main menu
        return
      else:
        print("Invalid command")
      
      input("\nPress Enter to continue...")
  
  def text_restore_menu(self):
    # Menu for text prediction/restoration
    while True:
      self.display_header()
      print("\nPredict/Restore Text Commands:")
      print("~ - Load keywords from file")
      print("# - Display Trie")
      print("$pattern - List matching keywords")
      print("?pattern - Restore word (best match)")
      print("& - Restore text (all matches)")
      print("@ - Restore text (best matches)")
      print("! - Print instructions")
      print("\ - Exit to main menu")
      
      command = input("\n> ").strip()
      
      if not command:
        continue
        
      cmd = command[0]
      arg = command[1:].strip()
      
      if cmd == '~':
        # Load keywords from a file
        self._load_keywords_from_file()
      elif cmd == '#':
        # Visualize the trie structure
        print("\nTrie Structure:")
        self.trie.visualize()
      elif cmd == '$':
        # List all matching keywords for a pattern
        matches = self.trie.find_matches(arg.lower())
        if matches:
          print("\nMatching words:")
          for word, freq in matches:
            print(f"- {word} (frequency: {freq})")
        else:
          print("No matches found")
      elif cmd == '?':
        # Restore a single word (best match)
        restored = self.restorer.restore_word(arg, 'best')
        print(f"\nRestored word: {restored}")
      elif cmd == '&':
        # Restore text file using all matches
        self._restore_text_file('all')
      elif cmd == '@':
        # Restore text file using best matches
        self._restore_text_file('best')
      elif cmd == '!':
        # Print instructions (just redisplay)
        continue
      elif cmd == '\\':
        # Exit to main menu
        return
      else:
        print("Invalid command")
      
      input("\nPress Enter to continue...")
  
  def _load_keywords_from_file(self):
    # Load keywords from a file and insert into trie
    filename = input("Enter filename to load: ").strip()
    try:
      with open(filename, 'r') as f:
        for line in f:
          word = line.strip()
          if word:
            self.trie.insert(word.lower())
      print(f"Loaded keywords from {filename}")
      self.current_trie_file = filename
    except Exception as e:
      print(f"Error loading file: {e}")
  
  def _export_keywords_to_file(self):
    # Export all keywords and their frequencies to a file
    filename = input("Enter output filename: ").strip()
    try:
      with open(filename, 'w') as f:
        for word, freq in self.trie.get_all_words():
          f.write(f"{word},{freq}\n")
      print(f"Exported {self.trie.total_words} keywords to {filename}")
    except Exception as e:
      print(f"Error exporting file: {e}")
  
  def _save_trie_to_file(self):
    # Implement serialization of the trie structure
    pass
  
  def _restore_text_file(self, mode):
    # Restore text from a file using the trie and save output
    input_file = input("Enter input text file: ").strip()
    output_file = input("Enter output file: ").strip()
    
    try:
      with open(input_file, 'r') as f:
        content = f.read()
      
      restored = self.restorer.restore_text(content, mode)
      
      with open(output_file, 'w') as f:
        f.write(restored)
      
      print(f"Text restored using {mode} matches and saved to {output_file}")
    except Exception as e:
      print(f"Error processing files: {e}")
  
  def run(self):
    # Main application loop
    while self.running:
      self.display_main_menu()
      choice = input("\nEnter choice: ").strip()
      
      if choice == '1':
        self.trie_edit_menu()
      elif choice == '2':
        self.text_restore_menu()
      elif choice == '7':
        self.running = False
        print("Exiting application. Goodbye!")
      else:
        print("Invalid choice. Please try again.")
      input("\nPress Enter to continue...")

if __name__ == "__main__":
  # Entry point for the application
  app = Application()
  app.run()