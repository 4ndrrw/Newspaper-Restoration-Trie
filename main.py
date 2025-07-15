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
    print("*****************************************************************")
    print("* ST1507 DSAA: Predictive Text Editor (Using Tries)             *")
    print("*---------------------------------------------------------------*")
    print("*                                                               *")
    print("* - Done by: Andrew Pang (2423708) & Nyi Nyi Zaw (2423472)      *")
    print("* - Class DAAA/2A/04                                            *")
    print("*                                                               *")
    print("*****************************************************************")

  def display_main_menu(self):
    # Show the main menu options
    self.display_header()
    print("\n\nPlease select your choice ('1', '2', '3', '4', '5', '6', '7'):")
    print("    1. Construct/Edit Trie")
    print("    2. Predict/Restore Text")
    print("    -----------------------------------------------------------")
    print("    3. Extra Feature One (Andrew Pang)")
    print("    4. Extra Feature Two (Andrew Pang)")
    print("    -----------------------------------------------------------")
    print("    5. Extra Feature One (Nyi Nyi Zaw)")
    print("    6. Extra Feature Two (Nyi Nyi Zaw)")
    print("    -----------------------------------------------------------")
    print("    7. Exit")

  def trie_edit_menu(self):
    # Menu for constructing and editing the trie
    while True:
      self.display_header()
      self._print_trie_edit_instructions()
      command = input("\n> ").strip()
      if not command:
        continue
      cmd = command[0]
      arg = command[1:].strip()
      if self._handle_trie_edit_command(cmd, arg):
        return
      input("\nPress Enter to continue...")

  def _print_trie_edit_instructions(self):
    print("\nConstruct/Edit Trie Commands:")
    print("'+word' - Add a keyword")
    print("-word' - Delete a keyword")
    print("?word' - Find a keyword")
    print("# - Display Trie")
    print("@ - Write Trie to file")
    print("~ - Read keywords from file")
    print("= - Write keywords to file")
    print("! - Print instructions")
    print("\\ - Exit to main menu")

  def _handle_trie_edit_command(self, cmd, arg):
    command_methods = {
      '+': self._cmd_add_word,
      '-': self._cmd_delete_word,
      '?': self._cmd_find_word,
      '#': self._cmd_display_trie,
      '@': self._save_trie_to_file,
      '~': self._load_keywords_from_file,
      '=': self._export_keywords_to_file,
      '!': self._cmd_print_instructions,
      '\\': self._cmd_exit_menu
    }
    if cmd in command_methods:
      return command_methods[cmd](arg)
    else:
      print("Invalid command")
      return False

  def _cmd_add_word(self, arg):
    self.trie.insert(arg.lower())
    print(f"Added '{arg}' to trie")
    return False

  def _cmd_delete_word(self, arg):
    if self.trie.delete(arg.lower()):
      print(f"Deleted '{arg}' from trie")
    else:
      print(f"'{arg}' not found in trie")
    return False

  def _cmd_find_word(self, arg):
    if self.trie.search(arg.lower()):
      print(f"'{arg}' is present in trie")
    else:
      print(f"'{arg}' is not present in trie")
    return False

  def _cmd_display_trie(self, arg):
    print("\nTrie Structure:")
    self.trie.visualize()
    return False

  def _cmd_print_instructions(self, arg):
    # Print instructions (just redisplay)
    return False

  def _cmd_exit_menu(self, arg):
    # Exit to main menu
    return True
  
  def text_restore_menu(self):
    # Menu for text prediction/restoration
    while True:
      self.display_header()
      self._print_text_restore_instructions()
      command = input("\n> ").strip()
      if not command:
        continue
      if self._handle_text_restore_command(command):
        return
      input("\nPress Enter to continue...")

  def _print_text_restore_instructions(self):
    print("\nPredict/Restore Text Commands:")
    print("~ - Load keywords from file")
    print("# - Display Trie")
    print("$pattern - List matching keywords")
    print("?pattern - Restore word (best match)")
    print("& - Restore text (all matches)")
    print("@ - Restore text (best matches)")
    print("! - Print instructions")
    print("\\ - Exit to main menu")

  def _handle_text_restore_command(self, command):
    cmd = command[0]
    arg = command[1:].strip()
    if cmd == '~':
      self._load_keywords_from_file()
    elif cmd == '#':
      print("\nTrie Structure:")
      self.trie.visualize()
    elif cmd == '$':
      matches = self.trie.find_matches(arg.lower())
      if matches:
        print("\nMatching words:")
        for word, freq in matches:
          print(f"- {word} (frequency: {freq})")
      else:
        print("No matches found")
    elif cmd == '?':
      restored = self.restorer.restore_word(arg, 'best')
      print(f"\nRestored word: {restored}")
    elif cmd == '&':
      self._restore_text_file('all')
    elif cmd == '@':
      self._restore_text_file('best')
    elif cmd == '!':
      # Print instructions (just redisplay)
      pass
    elif cmd == '\\':
      return True
    else:
      print("Invalid command")
    return False
  
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
      choice = input("Enter choice: ").strip()
      
      if choice == '1':
        self.trie_edit_menu()
      elif choice == '2':
        self.text_restore_menu()
      elif choice == '7':
        self.running = False
        print("Exiting application. Goodbye!")
      else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
  # Entry point for the application
  app = Application()
  app.run()