import os
import re
from processors.trie_processor import TrieProcessor
from processors.text_processor import TextProcessor
from helpers.file_io import FileIO

class Application:
  def __init__(self):
    """Initialize application components"""
    # Create processor and file IO objects
    self.trie_processor = TrieProcessor()
    self.text_processor = TextProcessor(self.trie_processor)
    self.file_io = FileIO()
    self.running = True
  
  def display_header(self):
    """Display application header"""
    print("\n*****************************************************************")
    print("* ST1507 DSAA: Predictive Text Editor (Using tries)             *")
    print("*---------------------------------------------------------------*")
    print("*                                                               *")
    print("* - Done by: Andrew Pang (2423708) & Nyi Nyi Zaw (2423472)      *")
    print("* - Class DAAA/2A/04                                            *")
    print("*                                                               *")
    print("*****************************************************************")

  def display_main_menu(self):
    """Display main menu options"""
    print("\n\nPlease select your choice ('1', '2', '3', '4', '5', '6', '7'):")
    print("  1. Construct/Edit Trie")
    print("  2. Predict/Restore Text")
    print("  ---------------------------------------------------------------")
    print("  3. Extra Feature One (Andrew Pang)")
    print("  4. Extra Feature Two (Andrew Pang)")
    print("  ---------------------------------------------------------------")
    print("  5. Extra Feature One (Nyi Nyi Zaw)")
    print("  6. Extra Feature Two (Nyi Nyi Zaw)")
    print("  ---------------------------------------------------------------")
    print("  7. Exit")

  def trie_edit_menu(self):
    """Handle trie construction/edit menu"""
    # Show instructions only when first entering the menu
    self._print_trie_edit_instructions()
    
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue

        # Handle the command and exit if needed
        if self._handle_trie_edit_command(command):
          return

      except KeyboardInterrupt:
        print("\nOperation cancelled.")
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")

  def _print_trie_edit_instructions(self):
    """Print trie edit command instructions"""
    print("\n---------------------------------------------------------------")
    print("Construct/Edit Trie Commands:")
    print("    '+','-','?','#','@','~','=','!','\\'")
    print("---------------------------------------------------------------")
    print("    +sunshine        (Add a keyword)")
    print("    -moonlight       (Delete a keyword)")
    print("    ?rainbow         (Find a keyword)")
    print("    #                (Display Trie)")
    print("    @                (Write Trie to file)")
    print("    ~                (Read keywords from file to make Trie)")
    print("    =                (Write keywords from Trie to file)")
    print("    !                (Print instructions)")
    print("    \\                (Exit)")
    print("---------------------------------------------------------------")

  def _handle_trie_edit_command(self, command):
    """Process trie edit commands"""
    cmd = command[0]
    arg = command[1:].strip()

    # Map commands to their handlers
    commands = {
      '+': lambda: print(self.trie_processor.add_word(arg)),
      '-': lambda: print(self.trie_processor.delete_word(arg)),
      '?': lambda: print(
        f"Keyword '{arg}' is present in the trie" if self.trie_processor.find_word(arg)
        else f"Keyword '{arg}' is not present in the trie"
      ),
      '#': lambda: self.trie_processor.display_trie(),
      '@': self._save_trie_to_file,
      '~': self._load_keywords_from_file,
      '=': self._export_keywords_to_file,
      '!': self._print_trie_edit_instructions,
      '\\': lambda: self._exit_trie_edit_menu()
    }

    handler = commands.get(cmd, lambda: print("Invalid command"))
    return handler()

  def _exit_trie_edit_menu(self):
    """Exit trie edit menu with goodbye message"""
    print("Exiting the Edit Command Prompt. Bye...")
    input("\nPress enter key, to continue....")
    return True

  def text_restore_menu(self):
    """Handle text prediction/restoration menu"""
    # Show instructions only when first entering the menu
    self._print_text_restore_instructions()
    
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue

        # Handle the command and exit if needed
        if self._handle_text_restore_command(command):
          return

      except KeyboardInterrupt:
        print("\nOperation cancelled.")
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")

  def _print_text_restore_instructions(self):
    """Print text restore command instructions"""
    print("\n---------------------------------------------------------------")
    print("Predict/Restore Text Commands:")
    print("    '~','#','$','?','&','@','!','\\'")
    print("---------------------------------------------------------------")
    print("  ~          (Read keywords from file to make Trie)")
    print("  #          (Display Trie)")
    print("  $ra*nb*w   (List all possible matching keywords)")
    print("  ?ra*nb*w   (Restore a word using best keyword match)")
    print("  &          (Restore a text using all matching keywords)")
    print("  @          (Restore a text using best keyword matches)")
    print("  !          (Print instructions)")
    print("  \\          (Exit)")
    print("---------------------------------------------------------------")

  def _handle_text_restore_command(self, command):
    """Process text restore commands"""
    cmd = command[0]
    arg = command[1:].strip()

    # Map commands to their handlers
    commands = {
      '~': self._load_keywords_from_file,
      '#': lambda: self.trie_processor.display_trie(),
      '$': lambda: self._show_matches(arg),
      '?': lambda: print(f"Restored keyword: '{self.text_processor.restore_word(arg, 'best')}'"),
      '&': lambda: self._process_text_file('all'),
      '@': lambda: self._process_text_file('best'),
      '!': self._print_text_restore_instructions,
      '\\': lambda: self._exit_trie_edit_menu()
    }

    handler = commands.get(cmd, lambda: print("Invalid command"))
    return handler()

  def _load_keywords_from_file(self):
    """Load keywords from file into trie"""
    filename = input("Please enter input file: ").strip()
    result = self.file_io.load_keywords(filename, self.trie_processor)
    print(result)

  def _export_keywords_to_file(self):
    """Export trie keywords to file"""
    filename = input("Please enter output file: ").strip()
    words = self.trie_processor.get_all_words()
    result = self.file_io.export_keywords(filename, words)
    print(result)

  def _save_trie_to_file(self):
    """Serialize trie to file"""
    filename = input("Please enter new filename: ").strip()
    result = self.file_io.save_trie(filename, self.trie_processor)
    print(result)

  def _show_matches(self, pattern):
    """Display all matching keywords for pattern"""
    matches = self.trie_processor.find_matches(pattern)
    if matches:
        formatted = [f"[{word},{freq}]" for word, freq in matches]
        print(",".join(formatted))
    else:
        print()  

  def _process_text_file(self, mode):
    """Process text file restoration"""
    input_file = input("Please enter input file: ").strip()
    output_file = input("Please enter output file: ").strip()
    
    try:
      # Read input file
      with open(input_file, 'r') as f:
        content = f.read()
      
      # Restore text using the selected mode
      restored = self.text_processor.restore_text(content, mode)
      # Write restored text to output file
      result = self.file_io.restore_text_file(output_file, restored)
      print(result)
    except Exception as e:
      print(f"Error processing files: {e}")

  def run(self):
    """Main application loop"""
    self.display_header()
    
    while self.running:
      try:
        self.display_main_menu()
        choice = input("\nEnter choice: ").strip()
        
        if choice == '1':
          self.trie_edit_menu()
        elif choice == '2':
          self.text_restore_menu()
        elif choice == '7':
          self.running = False
          print("\nExiting application. Goodbye!")
        else:
          print("\nInvalid choice. Please try again.")
          input("Press Enter to continue...")
          
      except KeyboardInterrupt:
        print("\nOperation cancelled.")
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("Press Enter to continue...")

if __name__ == "__main__":
  # Start the application
  app = Application()
  app.run()