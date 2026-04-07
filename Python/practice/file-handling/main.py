import sys
from reader import read_file
from processor import *
from utils import write_output

def sayHello():
    print("Main.py says helo")

def main():
    if len(sys.argv) < 2:
        print("To run: python main.py <file>")
        return
    
    file_path = sys.argv[1]
    
    lines = read_file(file_path)
    # print(lines)
    cleaned = clean_lines(lines)
    # print(cleaned)
    
    keyword = input("Enter keyword to filter: ")
    filtered = filter_lines(cleaned, keyword)
    
    report = f"""
Total lines: {len(lines)}
Filtered lines: {len(filtered)}
Total words: {word_count(cleaned)}
Most common word: {most_common_word(cleaned)}
Total characters: {total_characters(cleaned)}
"""
    print(report)
    write_output("output.txt", report)
    
if __name__ == "__main__":
    main()