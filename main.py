from processors.trie_processor import TrieProcessor
from processors.text_processor import TextProcessor
from processors.batch_restorer import BatchRestorer
from helpers.file_io import FileIO

class Application:
  def __init__(self):
    """Initialize application components"""
    self.trie_processor = TrieProcessor()
    self.text_processor = TextProcessor(self.trie_processor)
    self.file_io = FileIO()
    self.batch_restorer = BatchRestorer(self.text_processor, self.file_io)
    self.running = True

    # state for Option 5 (context) and Option 6 (fuzzy)
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
    print("  3. Batch Restore with Summary (Andrew Pang)")
    print("  4. Random Word Challenge: Gamified Testing (Andrew Pang)")
    print("  ---------------------------------------------------------------")
    print("  5. Context-Aware Restore (Nyi Nyi Zaw)")
    print("  6. Fuzzy Scan & OCR Confusables (Nyi Nyi Zaw)")
    print("  ---------------------------------------------------------------")
    print("  7. Exit")

  # =========================================
  # ===== Option 1: Construct/Edit Trie =====
  # =========================================
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
    print("    '+', '-', '?', '#', '@', '~', '=', '!', '\\'")
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
      '@': lambda: FileIO.prompt_save_trie(self.trie_processor),
      '~': lambda: FileIO.prompt_load_keywords(self.trie_processor),
      '=': lambda: FileIO.prompt_export_keywords(self.trie_processor),
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

  # ==========================================
  # ===== Option 2: Predict/Restore Text =====
  # ==========================================
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
    print("    '~', '#', '$', '?', '&', '@', '!', '\\'")
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
      '~': lambda: FileIO.prompt_load_keywords(self.trie_processor),
      '#': lambda: self.trie_processor.display_trie(),
      '$': lambda: FileIO.prompt_show_matches(self.trie_processor, arg),
      '?': lambda: print(f"Restored keyword: '{self.text_processor.restore_word(arg, 'best')}'"),
      '&': lambda: FileIO.prompt_process_text_file(self.text_processor, self.file_io, 'all'),
      '@': lambda: FileIO.prompt_process_text_file(self.text_processor, self.file_io, 'best'),
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

  # ================================================
  # ===== Option 3: Batch Restore with Summary =====
  # ================================================
  def _print_batch_restore_instructions(self):
    """Print batch restore command instructions"""
    print("\n---------------------------------------------------------------")
    print("Batch Restore with Summary Commands:")
    print("    '~', '#', 'r', '!', '\\'")
    print("---------------------------------------------------------------")
    print("     ~      (Read keywords from file to make Trie)")
    print("     #      (Display Trie)")
    print("     r      (Run batch restore on all .txt files in a folder)")
    print("     !      (Print instructions)")
    print("     \\      (Exit)")
    print("---------------------------------------------------------------")

  def batch_restore_menu(self):
    """Batch restore all .txt files in a folder and print a summary report (OOP)"""
    self._print_batch_restore_instructions()
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue
        if command == '!':
          self._print_batch_restore_instructions()
        elif command == '~':
          from processors.batch_restorer import BatchRestorer
          BatchRestorer.prompt_load_keywords(self.trie_processor)
        elif command == '#':
          from processors.batch_restorer import BatchRestorer
          BatchRestorer.prompt_display_trie(self.trie_processor)
        elif command == '\\':
          print("Exiting Batch Restore. Bye...")
          input("\nPress Enter to continue...")
          return
        elif command.lower() == 'r':
          from processors.batch_restorer import BatchRestorer
          BatchRestorer.prompt_run_batch_restore(self.batch_restorer)
        else:
          print("Invalid command. Type '!', '~', '#', or 'r' to run batch restore.")
      except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")

  # ============================================
  # ===== Option 4: Random World Challenge =====
  # ============================================
  def random_word_challenge_menu(self):
    from processors.random_word_challenge import RandomWordChallenge
    challenge = RandomWordChallenge(self.trie_processor)
    self._print_random_word_challenge_instructions()
    while True:
      try:
        command = input("\n>").strip()
        if not command:
          continue
        if command == '!':
          self._print_random_word_challenge_instructions()
        elif command == '~':
          FileIO.prompt_load_keywords(self.trie_processor)
        elif command == '#':
          self.trie_processor.display_trie()
        elif command == '\\':
          print("Exiting Random Word Challenge. Bye...")
          input("\nPress Enter to continue...")
          return
        elif command == 'r':
          challenge.play_round()
        else:
          print("Invalid command. Type '!', '~', '#', or 'r' to play.")
      except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
      except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")
  
  def _print_random_word_challenge_instructions(self):
    """Print instructions for Random Word Challenge"""
    print("\n---------------------------------------------------------------")
    print("Random Word Challenge Commands:")
    print("    '~', '#', 'r', '!', '\\'")
    print("---------------------------------------------------------------")
    print("     ~       (Read keywords from file to make Trie)")
    print("     #       (Display Trie)")
    print("     r       (Run random word challenge)")
    print("     !       (Print instructions)")
    print("     \\       (Exit)")
    print("---------------------------------------------------------------")
    
  # ===========================================        
  # ===== Option 5: Context-Aware Restore =====
  # ===========================================        
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
    print("    '~', '#', 'C', 'T', '@', '!', '\\'")
    print("---------------------------------------------------------------")
    print("  ~          (Read keywords from file to make Trie)")
    print("  #          (Display Trie)")
    print("  C          (Load/Build corpus language model)")
    print("  T          (Set confidence threshold)")
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
    '~': lambda: FileIO.prompt_load_keywords(self.trie_processor),
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

  # ====================================================
  # ===== Option 6: Fuzzy Scan & OCR Confusables =====
  # ====================================================
  def fuzzy_scan_menu(self):
    """Command panel for Fuzzy Scan & OCR Confusables"""
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
    """Print instructions for Fuzzy Scan panel"""
    print("\n---------------------------------------------------------------")
    print("Fuzzy Scan & OCR Confusables Commands:")
    print("    '~', '#', 'C', 'D', '@', '!', '\\'")
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
    """Process commands in Fuzzy Scan panel"""
    cmd = command[0]
    arg = command[1:].strip()

    commands = {
    '~': lambda: FileIO.prompt_load_keywords(self.trie_processor),
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
    print("Exiting the Fuzzy Scan panel. Bye...")
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

      with open(input_file, 'r', encoding='utf-8') as f:
        raw = f.read()

      conf_map = default_confusables() if self._fuzzy_conf_on else {}
      searcher = TrieFuzzySearcher(self.trie_processor, confusables=conf_map)
      suggestions = searcher.suggest_for_text(raw, max_dist=self._fuzzy_max_dist)

      with open(out_suggestions, 'w', encoding='utf-8') as f:
        for tok, suggs in suggestions:
          f.write(f"{tok} -> {suggs}\n")

      print(f"Fuzzy suggestions complete.")
    except Exception as e:
      print(f"Error running fuzzy repair: {e}")

# ===============================
# ==== Main application loop ====
# ===============================
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
        elif choice == '3':
          self.batch_restore_menu()
        elif choice == '4':
          self.random_word_challenge_menu()
        elif choice == '5':
          self.context_restore_menu()
        elif choice == '6':
          self.fuzzy_scan_menu()
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

# ===============================
# Main application entry point
# ===============================
if __name__ == "__main__":
  # Start the application
  app = Application()
  app.run()
