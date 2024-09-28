import re

def load_dictionary(file_path):
    """Load the translation dictionary from a file."""
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if '=' in line:
                keys, value = line.strip().split('=', 1)
                for key in keys.split(','):
                    dictionary[key.strip().lower()] = value.strip().lower()
    return dictionary

def split_text_with_punctuation(text):
    """Split text into words and punctuation, preserving the order."""
    return re.findall(r'\b\w+\b|[^\w\s]', text)

def restore_punctuation(translated_words, words_with_punctuation):
    """Restore punctuation to translated words."""
    result = []
    translated_idx = 0
    for item in words_with_punctuation:
        if re.match(r'[^\w\s]', item):
            if item == ',':
                # Only add comma if it's not already at the end of result
                if result and result[-1] != ',':
                    result.append(item)
            else:
                result.append(item)
        else:
            if translated_idx < len(translated_words):
                result.append(translated_words[translated_idx])
                translated_idx += 1
    # Join result and fix any trailing punctuation issues
    return ' '.join(result).replace(' ,', ',')

def translate_phrase(text, us_pt_dict, pt_us_dict):
    """Translate a phrase while preserving punctuation and proper nouns."""
    # Split the text into words and punctuation
    words_with_punctuation = split_text_with_punctuation(text)
    
    # Split the text into words for processing
    words = [word.strip().lower() for word in re.findall(r'\b\w+\b', text)]
    
    # Attempt to match longer phrases first
    translated_words = []
    while words:
        matched = False
        for i in range(len(words), 0, -1):
            phrase = ' '.join(words[:i])
            if phrase in us_pt_dict:
                translated_words.append(us_pt_dict[phrase])
                words = words[i:]
                matched = True
                break
            elif phrase in pt_us_dict:
                translated_words.append(pt_us_dict[phrase])
                words = words[i:]
                matched = True
                break
        
        if not matched:
            # Translate remaining single words if needed
            word = words.pop(0)
            if word in us_pt_dict:
                translated_words.append(us_pt_dict[word])
            elif word in pt_us_dict:
                translated_words.append(pt_us_dict[word])
            else:
                # Preserve proper nouns and untranslatable words
                translated_words.append(word.capitalize())
    
    # Restore punctuation to translated words
    return restore_punctuation(translated_words, words_with_punctuation)

def main():
    # Load dictionaries
    us_pt_dict = load_dictionary('us_pt.txt')
    pt_us_dict = load_dictionary('pt_us.txt')

    print("========================================")
    print("          Tradutor")
    print("Digite em inglês ou em português; a tradução aparecerá na próxima linha.")
    print("Type 'exitnow' to quit.")
    print("========================================")

    while True:
        text = input("Enter text to translate: ").strip()
        if text.lower() == 'exitnow':
            print("Exiting translator...")
            break
        
        # Translate text and print result
        translation = translate_phrase(text, us_pt_dict, pt_us_dict)
        print(f"Translation: {translation}")

if __name__ == "__main__":
    main()
