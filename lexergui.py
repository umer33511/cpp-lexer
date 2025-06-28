import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
from lexer import LexicalAnalyzer

class LexerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C++ Lexical Analyzer")
        self.root.geometry("800x600")
        self.analyzer = LexicalAnalyzer()
        
        # Create input file frame
        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="Input File:").pack(side=tk.LEFT)
        self.input_file_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.input_file_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Browse...", command=self.browse_input_file).pack(side=tk.LEFT)
        
        # Create output file frame
        output_frame = tk.Frame(root)
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(output_frame, text="Output File:").pack(side=tk.LEFT)
        self.output_file_var = tk.StringVar()
        tk.Entry(output_frame, textvariable=self.output_file_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Browse...", command=self.browse_output_file).pack(side=tk.LEFT)
        
        # Create analyze button
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Analyze", command=self.analyze_file, width=20).pack()
        
        # Create text area for displaying results
        tk.Label(root, text="Results:").pack(anchor=tk.W, padx=10)
        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25)
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C++ Files", "*.cpp"), ("All Files", "*.*")])
        if file_path:
            self.input_file_var.set(file_path)
            # Set default output file name
            input_dir = os.path.dirname(file_path)
            input_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(input_dir, f"{input_name}_tokens.txt")
            self.output_file_var.set(output_path)
    
    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                              filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.output_file_var.set(file_path)
    
    def analyze_file(self):
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file not found: {input_file}")
            return
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        try:
            # Generate tokens
            tokens = self.analyzer.analyze_file(input_file)
            if not tokens:
                messagebox.showerror("Error", "No tokens found. Check the input file.")
                return
            
            # Display results immediately
            self.display_results(tokens)
            
            # Attempt to save tokens
            self.analyzer.save_tokens_to_file(tokens, output_file)
            messagebox.showinfo("Success", f"Analysis complete. Tokens saved to {output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tokens: {str(e)}")

    def display_results(self, tokens):
        self.result_text.delete(1.0, tk.END)
        for token_type, value, line_num in tokens:
            self.result_text.insert(tk.END, f"Line {line_num}: Token = {value:<20} → {token_type}\n")
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = LexerGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        input("Press Enter to exit...")  # Keep terminal open