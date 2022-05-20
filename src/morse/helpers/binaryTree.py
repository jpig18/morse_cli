class Queue:

    def __init__(self, lst=[]):
        self.data = lst

    def __repr__(self):
        return str(self.data)

    def add(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop(0) if len(self.data) > 0 else None

    def peek(self):
        return self.data[0]

    def size(self):
        return len(self.data)


class Leaf:
    def __init__(self, leaf_name:str):
        self.leaf_name = leaf_name
        self.left_leaf = None
        self.right_leaf = None


class MorseTree:

    def __init__(self):
        self.__head = Leaf(None)
        self.__current_iter_node = None

        chars = ['E', 'T', 'I', 'A', 'N', 'M', 'S', 'U', 'R', 'W', 'D', 'K', 'G', 'O', 'H', 'V', 'F', 'L', 'P', 'J', 'B', 'X', 'C', 'Y', 'Z', 'Q', '5', '4', '3', '2', '+', '1', '6', '=', '/', '7', '8', '9', '0']
        morse_code_list = ['.', '-', '..', '.-', '-.', '--', '...', '..-', '.-.', '.--', '-..', '-.-', '--.', '---', '....', '...-', '..-.', '.-..', '.--.', '.---', '-...', '-..-', '-.-.', '-.--', '--..', '--.-', '.....', '....-', '...--', '..---', '.-.-.', '.----', '-....', '-...-', '-..-.', '--...', '---..', '----.', '-----']

        for index, char in enumerate(chars):
            if not self.__append_leaf(morse_code_list[index], char):
                raise RuntimeError("Could not add leaf {0} using morse code {1}".format(char, morse_code_list[index]))

    def __repr__(self): 
        #breadth first traversal
        visited = []
        frontier = Queue()
        frontier.add(self.__head)

        while frontier:
            leaf = frontier.pop()
            if leaf.leaf_name not in visited:
                visited.append(leaf.leaf_name)
                print(leaf.leaf_name)
            else:
                continue

            if leaf.left_leaf is not None:
                frontier.add(leaf.left_leaf)
            if leaf.right_leaf is not None:
                frontier.add(leaf.right_leaf)

    def reset_traverse(self):
        self.__current_iter_node = self.__head
            

    def traverse(self, blip: str)->str:
        if self.__current_iter_node is None:
            self.__current_iter_node = self.__head

        if blip == '.' and self.__current_iter_node.left_leaf is not None:
            self.__current_iter_node = self.__current_iter_node.left_leaf
            return self.__current_iter_node.leaf_name

        elif blip == '-' and self.__current_iter_node.right_leaf is not None:
            self.__current_iter_node = self.__current_iter_node.right_leaf
            return self.__current_iter_node.leaf_name

        else:
            return -1



    def __append_leaf(self, morse_code_for_char: str, char:str)->bool:
        """
        Desc

        Args:
            morse_code_for_char (str): _description_
            char (str): _description_

        Returns:
            bool: _description_
        """
        current_leaf = self.__head
        for index, blip in enumerate(morse_code_for_char):
            if blip == '.':
                #At insertion point
                if len(morse_code_for_char)-1 == index: 
                    if current_leaf.left_leaf is not None:
                        #Node exists change child name if not overwritting
                        if current_leaf.left_leaf.leaf_name is None:  
                            current_leaf.left_leaf.leaf_name = char
                            return True
                        else:
                            return False
                    else: 
                        #Leaf doesn't exist create new
                        current_leaf.left_leaf = Leaf(char)
                        return True
                #Iteration incomplete
                elif current_leaf.left_leaf is not None:
                    current_leaf = current_leaf.left_leaf
                else:
                    #Path doesnt exist add none leaf
                    current_leaf.left_leaf = Leaf(None)
                    current_leaf = current_leaf.left_leaf
            elif blip == '-':
                #At insertion point
                if len(morse_code_for_char)-1 == index: 
                    if current_leaf.right_leaf is not None:
                        #Node exists change child name if not overwritting
                        if current_leaf.right_leaf.leaf_name is None:  
                            current_leaf.right_leaf.leaf_name = char
                            return True
                        else:
                            return False
                    else: 
                        #Leaf doesn't exist create new
                        current_leaf.right_leaf = Leaf(char)
                        return True
                #Iteration incomplete
                elif current_leaf.right_leaf is not None:
                    current_leaf = current_leaf.right_leaf
                else:
                    #Path doesnt exist add none leaf
                    current_leaf.right_leaf = Leaf(None)
                    current_leaf = current_leaf.right_leaf
            #Unknown char
            else:
                return False

        return False


if __name__ == '__main__':
    t = MorseTree()
    print(t.traverse('-'))
    print(t.traverse('.'))
    print(t.traverse('-'))
    print(t.traverse('-'))
    print(t.traverse('-'))
    print(t.traverse('-'))


    
