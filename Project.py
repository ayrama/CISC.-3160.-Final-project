import os

# exception class for interpreter errors
class InterpreterError(Exception):
  pass

# main class
class Interpreter:
  def __init__(self):
      # this is the symbol table for storing variable assignments
      self.sym_tab = {}

  # this function reads a file and returns its contents
  def read_file(self, file_path):
        # checking if the file exists
        if not os.path.exists(file_path):
            raise InterpreterError(f"File not found: {file_path}")

        # opening and reading the file.
        with open(file_path, 'r') as file:
            return file.read()
        
  # function that tokenize the input string
  def tokenize(self, input_string):
        tokens = []
        i = 0
        while i < len(input_string):
            # skipping whitespaces
            if input_string[i].isspace():
                i += 1
            # operators and parentheses are being recognized
            elif input_string[i] in "+-*/=;()":
                tokens.append(input_string[i])
                i += 1
            # tokenizing numbers
            elif input_string[i].isdigit():
                num = input_string[i]
                i += 1
                while i < len(input_string) and input_string[i].isdigit():
                    num += input_string[i]
                    i += 1

                # validating number format (no leading zeros)
                if num.startswith('0') and len(num) > 1:
                    raise InterpreterError("Invalid literal: " + num)

                tokens.append(int(num))
            # tokenizing identifiers (variables)
            elif input_string[i].isalpha() or input_string[i] == '_':
                id_str = input_string[i]
                i += 1
                while i < len(input_string) and (input_string[i].isalnum() or input_string[i] == '_'):
                    id_str += input_string[i]
                    i += 1
                tokens.append(id_str)
            else:
                # unrecognized character error
                raise InterpreterError(f"Unrecognized character: {input_string[i]}")
        return tokens
  
  # this is the function to parse the tokens and evaluate the expressions.
  def parse(self, tokens):
      def parse_factor(tokens):
            if not tokens:
                raise InterpreterError("Unexpected end of input in factor")

            # handling parentheses for expressions.
            if tokens[0] == '(':
                result, rest = parse_expression(tokens[1:])
                if rest[0] != ')':
                    raise InterpreterError("Expected ')' at the end of expression")
                return result, rest[1:]
            
            # handling unary plus and minus.
            if tokens[0] in ['+', '-']:
                op = tokens[0]
                value, rest = parse_factor(tokens[1:])
                return (value if op == '+' else -value), rest

            # getting value of variables from the symbol table.
            if isinstance(tokens[0], str) and tokens[0] in self.sym_tab:
                return self.sym_tab[tokens[0]], tokens[1:]

            # directly returning numbers.
            if isinstance(tokens[0], int):
                return tokens[0], tokens[1:]

            raise InterpreterError(f"Invalid factor: {tokens[0]}")
      
      # Nested function to parse terms (it handles multiplication).
      def parse_term(tokens):
          result, rest = parse_factor(tokens)
          while rest and rest[0] == '*':
              next_result, next_rest = parse_factor(rest[1:])
              result *= next_result
              rest = next_rest
          return result, rest
      
      # nested function to parse expressions (it handles addition and subtraction).
      def parse_expression(tokens):
          result, rest = parse_term(tokens)
          while rest and rest[0] in "+-":
              op = rest[0]
              next_result, next_rest = parse_term(rest[1:])
              result = result + next_result if op == '+' else result - next_result
              rest = next_rest
          return result, rest
      
      # loop for parsing: processing each assignment statement.
      i = 0
      while i < len(tokens):
            identifier = tokens[i]
            if tokens[i + 1] != '=':
                raise InterpreterError("Expected '=' after identifier")
            value, rest = parse_expression(tokens[i + 2:])
            if rest and rest[0] != ';':
                raise InterpreterError("Expected ';' at the end of assignment")
            
            # checking if the identifier is already in the symbol table
            if isinstance(identifier, int) or identifier in self.sym_tab:
                self.sym_tab[identifier] = value
            else:
                # updating symbol table with variable values.
                self.sym_tab[identifier] = value

            # moving to the next statement.
            i = i + 3 + len(tokens[i + 2:]) - len(rest) 
  
  # main function to interpret the input string.
  def interpret(self, input_string):
      tokens = self.tokenize(input_string)
      self.parse(tokens)

      output = ""
      for key, val in self.sym_tab.items():
          output += f"{key} = {val}\n"
      return output.strip()


interpreter = Interpreter()

# you can change the pathway in " "; create the you_file.txt file before.
file_path = r"C:\Users\ayram\OneDrive\Desktop\testing.txt" 

try:
    file_content = interpreter.read_file(file_path)
    result = interpreter.interpret(file_content)
    print(result)
except InterpreterError as e:
    print("error:", e)
