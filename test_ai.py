from ai import DescribeImage, AiAgent
from PIL import Image

image = Image.open("./test.jpg")
di = DescribeImage()
context_description = di.get_description_of_(image)
print(context_description)

# def test_describe_image():
#     """
#     Test the describe method of DescribeImage class.
#     """
#     image = Image.open("./test.jpg")
#     di = DescribeImage()
#     print(di.get_description_of_(image))

def test_fan_comment():
    """
    Test the generate_comment method of AI class with persona as 'fan'.
    """
    ai = AiAgent(persona='fan')
    print(ai.generate_comment(context_description))

def test_hater_comment():
    """
    Test the generate_comment method of AI class with persona as 'hater'.
    """
    ai = AiAgent(persona='hater')
    print(ai.generate_comment(context_description))

def test_curious_comment():
    """
    Test the generate_comment method of AI class with persona as 'curious'.
    """
    ai = AiAgent(persona='curious')
    print(ai.generate_comment(context_description))




# Call all 3 test functions
# test_describe_image()
test_fan_comment()
test_hater_comment()
test_curious_comment()
