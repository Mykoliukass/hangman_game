from random_word import RandomWords


def generate_random_words(min_length, max_length, num_words):
    r = RandomWords()
    words = []
    for _ in range(num_words):
        word = r.get_random_word(
            hasDictionaryDef="true", minLength=min_length, maxLength=max_length
        )
        words.append(word)
    return words


# Generate 500 random words with lengths ranging from 5 to 12 letters
random_words = generate_random_words(5, 12, 500)
print(random_words[:10])  # Print first 10 random words
