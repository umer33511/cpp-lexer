import re
import sys
import os

class LexicalAnalyzer:
    def __init__(self):
        # Token patterns
        self.patterns = {
            'COMMENT_SINGLE': r'\/\/.*',
            'COMMENT_MULTI': r'\/\*[\s\S]*?\*\/',
            'PREPROCESSOR': r'#include\s*<[^>]+>|#\w+',
            'STRING_LITERAL': r'"([^\\"]|\\.)*"',
            'CHAR_LITERAL': r"'([^\\']|\\.)'",
            'LOG_OP': r'&&|\|\||!',
            'BITWISE_OP': r'<<|>>|&|\||\^|~',
            'REL_OP': r'==|!=|<=|>=|<|>',
            'ARITH_OP': r'\+\+|--|\+|-|\*|\/|%',
            'ASSIGN_OP': r'=|\+=|-=|\*=|\/=|%=',
            'KEYWORD': r'\b(int|float|double|char|if|else|for|while|return|void|class|public|private|protected|include|define|using|namespace|new|delete|true|false|bool|switch|case|break|continue|default|static|const|this|try|catch|throw)\b',
            'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'FLOAT_LITERAL': r'\d+\.\d*',
            'INT_LITERAL': r'\b\d+\b',
            'SEPARATOR': r'[(){}\[\];,:. ]'  # Updated to include '.'
        }
        
        # Compiled patterns
        self.tokens = {key: re.compile(pattern) for key, pattern in self.patterns.items()}
        
        # Whitespace and newline patterns
        self.whitespace = re.compile(r'\s+')

    def tokenize(self, code):
        """Tokenize the input code."""
        tokens = []
        line_num = 1
        pos = 0
        code_len = len(code)
        
        while pos < code_len:
            # Skip whitespace
            match = self.whitespace.match(code, pos)
            if match:
                line_num += code[pos:match.end()].count('\n')
                pos = match.end()
                continue
            
            # Try to match a token
            matched = False
            for token_type, pattern in self.tokens.items():
                match = pattern.match(code, pos)
                if match:
                    value = match.group(0)
                    token_line = line_num  # Line where the token starts
                    newline_count = value.count('\n')
                    
                    # Add the token to the list
                    tokens.append((token_type, value, token_line))
                    
                    # Update line number for multi-line tokens (e.g., comments)
                    line_num += newline_count
                    
                    # Move position to end of matched token
                    pos = match.end()
                    matched = True
                    break
            
            # Handle unmatched characters
            if not matched:
                if code[pos] == '\n':
                    line_num += 1
                elif code[pos] not in [' ', '\t', '\r']:
                    tokens.append(('UNKNOWN', code[pos], line_num))
                pos += 1
                    
        return tokens

    def analyze_file(self, file_path):
        """Analyze a file and return tokens."""
        try:
            with open(file_path, 'r') as file:
                code = file.read()
            return self.tokenize(code)
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    def save_tokens_to_file(self, tokens, output_path):
        try:
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as file:  # Fix: Add encoding
                for token_type, value, line_num in tokens:
                    file.write(f"Line {line_num}: Token = {value:<20} → {token_type}\n")
            return True
        except Exception as e:
            print(f"Error saving tokens: {e}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python lexer.py <input_file> [output_file]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    
    analyzer = LexicalAnalyzer()
    tokens = analyzer.analyze_file(input_file)
    analyzer.save_tokens_to_file(tokens, output_file)

if __name__ == "__main__":
    main()