from better_profanity import profanity 

def check_if_censored(word):
    # Check if the word contains profanity
    flag_censor = profanity.contains_profanity(word)
    return flag_censor

# Example usage
# word = 'stupid'
# status = check_if_censored(word)
# print(status)
