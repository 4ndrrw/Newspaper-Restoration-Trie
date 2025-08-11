import os

class BatchRestorer:
  def __init__(self, text_processor, file_io):
    self.text_processor = text_processor
    self.file_io = file_io

  def restore_folder(self, folder, mode='best', output_dir=None):
    if not output_dir:
      output_dir = folder
    if not os.path.isdir(folder):
      raise ValueError("Invalid folder path.")
    files = [f for f in os.listdir(folder) if f.lower().endswith('.txt')]
    if not files:
      raise ValueError("No .txt files found in the folder.")
    summary = []
    total_restored = 0
    total_matches = 0
    total_unmatched = 0
    unmatched_tokens_per_file = {}
    # Ensure output directory exists
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    for fname in files:
      in_path = os.path.join(folder, fname)
      out_path = os.path.join(output_dir, f"restored_{fname}")
      try:
        with open(in_path, 'r', encoding='utf-8') as f:
          content = f.read()
        restored = self.text_processor.restore_text(content, mode)
        import re
        # Count wildcards in original
        wildcards = re.findall(r"[a-zA-Z0-9*']*\*[a-zA-Z0-9*']*", content)
        num_wildcards = len(wildcards)
        # Count restored tokens in output (for 'best', wrapped in < >)
        restored_tokens = re.findall(r"<([^>]+)>", restored) if mode == 'best' else []
        num_restored = len(restored_tokens) if mode == 'best' else restored.count('[')
        num_matches = num_restored
        num_unmatched = num_wildcards - num_restored
        total_restored += num_restored
        total_matches += num_matches
        total_unmatched += max(0, num_unmatched)
        with open(out_path, 'w', encoding='utf-8') as f:
          f.write(restored)
        summary.append((fname, num_restored, num_matches, max(0, num_unmatched)))
        # Optionally, list unmatched wildcards (if any)
        if num_unmatched > 0:
          unmatched_tokens_per_file[fname] = [w for i, w in enumerate(wildcards) if i >= num_restored]
      except Exception as e:
        summary.append((fname, 'ERROR', 'ERROR', str(e)))
    return summary, total_restored, total_matches, total_unmatched, unmatched_tokens_per_file

  def print_summary(self, summary, total_restored, total_matches, total_unmatched, unmatched_tokens_per_file=None):
    print("\n📄 Batch Restore Summary")
    print("=" * 92)
    header = f"{'File Name':30} | {'Restored':8} | {'Matches':7} | {'Unmatched':9} | {'% Match':9} | {'% Unmatched':14}"
    print(header)
    print("-" * 92)
    
    for fname, nres, nmat, nunm in summary:
      total_items = (nres if isinstance(nres, int) else 0) + (nunm if isinstance(nunm, int) else 0)
      match_pct = (nmat / total_items * 100) if total_items > 0 and isinstance(nmat, int) else 0
      unmatch_pct = (nunm / total_items * 100) if total_items > 0 and isinstance(nunm, int) else 0
      print(f"{fname:30} | {nres:8} | {nmat:7} | {nunm:9} | {match_pct:8.2f}% | {unmatch_pct:12.2f}%")

    print("-" * 92)
    grand_total = total_restored + total_unmatched
    total_match_pct = (total_matches / grand_total * 100) if grand_total > 0 else 0
    total_unmatch_pct = (total_unmatched / grand_total * 100) if grand_total > 0 else 0
    print(f"{'TOTAL':30} | {total_restored:8} | {total_matches:7} | {total_unmatched:9} | {total_match_pct:8.2f}% | {total_unmatch_pct:12.2f}%")
    print("=" * 92)
    if unmatched_tokens_per_file:
      print("\nUnmatched wildcards per file:")
      for fname, tokens in unmatched_tokens_per_file.items():
        print(f"  {fname}: {tokens}")
