"""
This file contains the Comment class and its methods.

Comment class is used to generate comments for the live feed.

There are different types of comments:
1. Random comments (Hi, How are you? Where are you etc.)
2. Contextual comments (Comments based on the live feed content)

Random comments are sort of noise to make the live feed more realistic and make it look busy.
Contextual comments are based on the live feed content. 
For example, if the live feed is about a football match, the comments will be related to the match or
If the live streamer shows or mentions something, the comments will be related to that.

The comments are generated using LLM.
"""



class Comment:
    def __init__(self):
        self.comment = None

    def generate_random_comment(self):
        pass

    def generate_contextual_comment(self):
        pass

    def get_comment(self):
        return self.comment
