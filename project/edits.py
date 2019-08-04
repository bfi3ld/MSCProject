import difflib

class edits():

    def get_difference(text_1, text_2):
        text1 = text_1.split(".")
        text2 = text_2.split(".")
        lib = difflib.Differ()
        difference = lib.compare(text1, text2)
        return difference

        

    
            

        
