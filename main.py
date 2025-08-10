import os
import re
from processors.trie_processor import TrieProcessor
from processors.text_processor import TextProcessor
from helpers.file_io import FileIO

class Application:
  def __init__(self):
    """Initialize application components"""
    self.trie_processor = TrieProcessor()
    self.text_processor = TextProcessor(self.trie_processor)
    self.file_io = FileIO()
    self.running = True

    # NEW: state for Option 5 (context) and Option 6 (fuzzy)
    self._lm = None                 # language model for Option 5
    self._ctx_threshold = 0.6       # confidence threshold for Option 5
    self._fuzzy_conf_on = True      # confusables toggle for Option 6
    self._fuzzy_max_dist = 1        # edit distance for Option 6
  
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
    print("  5. Context-Aware Restore (Nyi Nyi Zaw)")
    print("  6. Fuzzy Repair & OCR Confusables (Nyi Nyi Zaw)")
    print("  ---------------------------------------------------------------")
    print("  7. Exit")

  # ===== Option 1: Construct/Edit Trie =====
  def trie_edit_menu(self):
    """Handle trie construction/edit menu"""
    self._print_trie_edit_instructions()
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue
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

  # ===== Option 2: Predict/Restore Text =====
  def text_restore_menu(self):
    """Handle text prediction/restoration menu"""
    self._print_text_restore_instructions()
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue
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
      '\\': lambda: self._exit_restore_menu()
    }

    handler = commands.get(cmd, lambda: print("Invalid command"))
    return handler()

  def _exit_restore_menu(self):
    """Exit restore menu with goodbye message"""
    print("Exiting the Restore Command Prompt. Bye...")
    input("\nPress enter key, to continue....")
    return True

  # ===== Option 5: Context-Aware Restore =====
  def context_restore_menu(self):
    """Command panel for Context-Aware Restore"""
    self._print_context_restore_instructions()
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue
        if self._handle_context_restore_command(command):
          return
      except KeyboardInterrupt:
        print("\nOperation cancelled.")
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")

  def _print_context_restore_instructions(self):
    """Print instructions for Context-Aware Restore"""
    print("\n---------------------------------------------------------------")
    print("Context-Aware Restore Commands:")
    print("    '~','#','C','T','@','!','\\'")
    print("---------------------------------------------------------------")
    print("  ~          (Read keywords from file to make Trie)")
    print("  #          (Display Trie)")
    print("  C          (Load/Build corpus language model)")
    print("  T0.75      (Set confidence threshold)")
    print("  @          (Restore a text with context)")
    print("  !          (Print instructions)")
    print("  \\          (Exit)")
    print("---------------------------------------------------------------")
    if self._lm is None:
      print("LM status: NOT LOADED | Threshold:", self._ctx_threshold)
    else:
      print("LM status: LOADED      | Threshold:", self._ctx_threshold)

  def _handle_context_restore_command(self, command):
    """Process commands in Context-Aware Restore"""
    cmd = command[0]
    arg = command[1:].strip()

    commands = {
      '~': self._load_keywords_from_file,
      '#': lambda: self.trie_processor.display_trie(),
      'C': self._load_corpus_language_model,
      'T': lambda: self._set_context_threshold(arg),
      '@': self._run_context_restore,
      '!': self._print_context_restore_instructions,
      '\\': lambda: self._exit_context_menu()
    }
    handler = commands.get(cmd, lambda: print("Invalid command"))
    return handler()

  def _exit_context_menu(self):
    print("Exiting the Context-Aware Restore panel. Bye...")
    input("\nPress enter key, to continue....")
    return True

  def _load_corpus_language_model(self):
    """Load/build the bigram language model from a corpus file"""
    try:
      from models.language_model import NGramLanguageModel
      corpus_file = input("Please enter corpus file: ").strip()
      self._lm = NGramLanguageModel(k=1.0)
      print("Building language model...")
      self._lm.fit_from_file(corpus_file)
      print("Language model loaded.")
    except Exception as e:
      print(f"Error loading language model: {e}")

  def _set_context_threshold(self, arg):
    """Set the confidence threshold (e.g., T0.75)"""
    try:
      if not arg:
        val = input("Enter threshold (0.0 - 1.0): ").strip()
      else:
        val = arg
      thr = float(val)
      if 0.0 <= thr <= 1.0:
        self._ctx_threshold = thr
        print(f"Threshold set to {self._ctx_threshold}")
      else:
        print("Please enter a value between 0.0 and 1.0")
    except Exception as e:
      print(f"Invalid threshold: {e}")

  def _run_context_restore(self):
    """Run context-aware restoration for a defect file"""
    if self._lm is None:
      print("No language model loaded. Use 'C' to load/build one first.")
      return
    try:
      input_file = input("Please enter input defect file: ").strip()
      out_text  = input("Please enter output restored file: ").strip()
      out_csv   = input("Please enter output review CSV filename: ").strip()

      with open(input_file, 'r', encoding='utf-8') as f:
        raw = f.read()

      restored, review_rows = self.text_processor.restore_text_with_context(
        raw, self._lm, threshold=self._ctx_threshold
      )

      with open(out_text, 'w', encoding='utf-8') as f:
        f.write(restored)

      with open(out_csv, 'w', encoding='utf-8') as f:
        f.write('original,choice,confidence,left,right,candidates\n')
        for orig, choice, conf, left, right, cands in review_rows:
          f.write(f"{orig},{choice},{conf},{left},{right},{cands}\n")

      print(f"Context restore complete.\n- Text: {out_text}\n- Review: {out_csv}")
    except Exception as e:
      print(f"Error running context restore: {e}")

  # ===== Option 6: Fuzzy Repair & OCR Confusables =====
  def fuzzy_repair_menu(self):
    """Command panel for Fuzzy Repair & OCR Confusables"""
    self._print_fuzzy_instructions()
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue
        if self._handle_fuzzy_command(command):
          return
      except KeyboardInterrupt:
        print("\nOperation cancelled.")
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")

  def _print_fuzzy_instructions(self):
    """Print instructions for Fuzzy Repair panel"""
    print("\n---------------------------------------------------------------")
    print("Fuzzy Repair & OCR Confusables Commands:")
    print("    '~','#','C','D','@','!','\\'")
    print("---------------------------------------------------------------")
    print("  ~          (Read keywords from file to make Trie)")
    print("  #          (Display Trie)")
    print("  C          (Toggle confusables on/off)")
    print("  D2         (Set max edit distance to 2; D1 for 1)")
    print("  @          (Suggest fuzzy fixes for a text)")
    print("  !          (Print instructions)")
    print("  \\          (Exit)")
    print("---------------------------------------------------------------")
    print(f"Confusables: {'ON' if self._fuzzy_conf_on else 'OFF'} | MaxDist: {self._fuzzy_max_dist}")

  def _handle_fuzzy_command(self, command):
    """Process commands in Fuzzy Repair panel"""
    cmd = command[0]
    arg = command[1:].strip()

    commands = {
      '~': self._load_keywords_from_file,
      '#': lambda: self.trie_processor.display_trie(),
      'C': self._toggle_confusables,
      'D': lambda: self._set_fuzzy_maxdist(arg),
      '@': self._run_fuzzy_on_file,
      '!': self._print_fuzzy_instructions,
      '\\': lambda: self._exit_fuzzy_menu()
    }
    handler = commands.get(cmd, lambda: print("Invalid command"))
    return handler()

  def _exit_fuzzy_menu(self):
    print("Exiting the Fuzzy Repair panel. Bye...")
    input("\nPress enter key, to continue....")
    return True

  def _toggle_confusables(self):
    """Toggle OCR confusables map on/off"""
    self._fuzzy_conf_on = not self._fuzzy_conf_on
    print(f"Confusables now {'ON' if self._fuzzy_conf_on else 'OFF'}.")

  def _set_fuzzy_maxdist(self, arg):
    """Set max edit distance: D1 or D2 (or prompt)"""
    try:
      if arg in ('1', '2'):
        val = int(arg)
      else:
        s = input("Max edit distance (1 or 2): ").strip()
        val = 2 if s == '2' else 1
      self._fuzzy_max_dist = val
      print(f"Max edit distance set to {self._fuzzy_max_dist}")
    except Exception as e:
      print(f"Invalid value: {e}")

  def _run_fuzzy_on_file(self):
    """Run fuzzy suggestions over a text file"""
    try:
      from processors.fuzzy_search import TrieFuzzySearcher, default_confusables
      input_file = input("Please enter input file: ").strip()
      out_suggestions = input("Please enter output suggestions file: ").strip()
      out_csv = input("Please enter output review CSV filename: ").strip()

      with open(input_file, 'r', encoding='utf-8') as f:
        raw = f.read()

      conf_map = default_confusables() if self._fuzzy_conf_on else {}
      searcher = TrieFuzzySearcher(self.trie_processor, confusables=conf_map)
      suggestions = searcher.suggest_for_text(raw, max_dist=self._fuzzy_max_dist)

      with open(out_suggestions, 'w', encoding='utf-8') as f:
        for tok, suggs in suggestions:
          f.write(f"{tok} -> {suggs}\n")

      with open(out_csv, 'w', encoding='utf-8') as f:
        f.write('token,suggestions\n')
        for tok, suggs in suggestions:
          f.write(f"{tok},\"{'|'.join(suggs)}\"\n")

      print(f"Fuzzy suggestions complete.\n- Suggestions: {out_suggestions}\n- Review: {out_csv}")
    except Exception as e:
      print(f"Error running fuzzy repair: {e}")

  # ===== Shared helpers =====
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
      print()  # blank line

  def _process_text_file(self, mode):
    """Process text file restoration"""
    input_file = input("Please enter input file: ").strip()
    output_file = input("Please enter output file: ").strip()
    try:
      with open(input_file, 'r') as f:
        content = f.read()
      restored = self.text_processor.restore_text(content, mode)
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
        elif choice == '5':
          self.context_restore_menu()
        elif choice == '6':
          self.fuzzy_repair_menu()
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