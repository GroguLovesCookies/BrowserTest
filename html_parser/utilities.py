from typing import List


# A function to intelligently split strings, while ignoring split points within quotation marks
def smart_split(in_string: str, split_character: chr = " ", ignore_character: chr = "\"") -> List[str]:
    output: List[str] = []
    within_ignore: bool = False
    current_split: str = ""


    for char in in_string:
        if char == ignore_character:
            within_ignore = not within_ignore
            current_split += char
        elif char == split_character and not within_ignore:
            output.append(current_split)
            current_split = ""
        else:
            current_split += char
    output.append(current_split)
    
    return output


def copy_string(string: str) -> str:
    return (string + ".")[:-1]