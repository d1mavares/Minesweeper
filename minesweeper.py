import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.set):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell) # mark the cell as a move that has been made
        self.mark_safe(cell)        # mark the cell as safe
        # updates sentences that contain cell

        # removing empty knowledge
        for sent in self.knowledge:
            if len(sent.cells) == 0:
                self.knowledge.remove(sent)
        
        # removing safes and mines from knowledge
        for sent in self.knowledge:
            for safe in self.safes:
                if safe in sent.cells.copy():
#                    print(f'removing new safe {safe} from {sent.cells} = {sent.count}\n')
                    sent.cells.difference_update({safe})        
            for mine in self.mines:
                if mine in sent.cells.copy():
#                    print(f'removing new mine {mine} from {sent.cells} = {sent.count}\n')
                    sent.cells.difference_update({mine})
                    sent.count -= 1        

        # add a new sentence to the AI's knowledge
        neighbors = []
        if cell[0] == 0:
            if cell[1] == 0: #(0,0) corner
                for n1 in range(0,2):
                    for n2 in range(0,2):
                        neighbors.append((cell[0]+n1,cell[1]+n2))
            elif cell[1] == self.width-1: #(0,7) corner
                for n1 in range(0,2):
                    for n2 in range(-1,1):
                        neighbors.append((cell[0]+n1,cell[1]+n2))
            else:# (0,j) row
                for n1 in range(0,2):
                    for n2 in range(-1,2):
                        neighbors.append((cell[0]+n1,cell[1]+n2))
        elif cell[0] == self.height-1:
            if cell[1] == 0:#(7,0) corner
                for n1 in range(-1,1):
                    for n2 in range(0,2):
                        neighbors.append((cell[0]+n1,cell[1]+n2))
            elif cell[1] == self.width-1:#(7,7) corner
                for n1 in range(-1,1):
                    for n2 in range(-1,1):
                        neighbors.append((cell[0]+n1,cell[1]+n2))
            else:#(7,j) row
                for n1 in range(-1,1):
                    for n2 in range(-1,2):
                        neighbors.append((cell[0]+n1,cell[1]+n2))
        elif (cell[1] == 0) and (cell[0]>0) and (cell[0]<self.width-1):#(i,0) column
             for n1 in range(-1,2):
                for n2 in range(0,2):
                    neighbors.append((cell[0]+n1,cell[1]+n2))
        elif (cell[1] == self.height-1) and (cell[0]>0) and (cell[0]<self.width-1):#(i,7) column
             for n1 in range(-1,2):
                for n2 in range(-1,1):
                    neighbors.append((cell[0]+n1,cell[1]+n2))
        else:
            for n1 in range(-1,2):
                for n2 in range(-1,2):
                    neighbors.append((cell[0]+n1,cell[1]+n2))
        # remove safes from neighbors
        aux = copy.deepcopy(self.safes)
        for neigh in neighbors:
            if neigh in self.safes:
                neighbors.remove(neigh)
            elif neigh in self.mines:
                if count > 0:
                    count -= 1 
                    neighbors.remove(neigh)
                #else:
                    #print('Warning: negative count!')
        self.knowledge.append(Sentence(neighbors,count))
#        print(f'adding knowledge: {self.knowledge[-1].cells}={self.knowledge[-1].count}')
    
        # mark any additional cells as safe
        # {A,B}=0 => A=B=0
        for sent in self.knowledge:
            aux = []
            if sent.count == 0:
                for newsafe in sent.cells.copy():
                    self.mark_safe(newsafe)
                    aux.append(newsafe)
                self.knowledge.remove(sent)
#                print(f'{aux} safe cells added.')
        # mark any additional cells as mines
        #{A,B,C}=3 => A=B=C=1
            elif sent.count == len(sent.cells):
                aux = []
                for newmine in sent.cells.copy():
                    self.mark_mine(newmine)
                    aux.append(newmine)
                self.knowledge.remove(sent)
#                print(f'{aux} mine cells added.')

        # removing empty knowledge    
        for sent in self.knowledge:
            if len(sent.cells) == 0:
                self.knowledge.remove(sent)

        # add any new sentences from inference to the AI's knowledge base
        # {A,B,C,D,E}=3 and {A,B,C}=1 => {D,E}=2
        for sent0 in self.knowledge:
            for sent1 in self.knowledge:
                 if (sent0.cells < sent1.cells):
 #                   print(f'getting infered knowledge from {sent0.cells} = {sent0.count} and {sent1.cells} = {sent1.count}\n')
                    self.knowledge.append(Sentence(sent1.cells.difference(sent0.cells),sent1.count-sent0.count))
                    self.knowledge.remove(sent1)
 #                   print(f'infered knowledge added:{self.knowledge[-1].cells} = {self.knowledge[-1].count}. Removing {sent1.cells} = {sent1.count}')

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes)-len(self.moves_made) > 0:
            return self.safes.difference(self.moves_made).pop()
            #return auxset.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if len(self.safes)-len(self.moves_made) < 1:
            auxcell = (random.randint(0,self.width-1),random.randint(0,self.height-1))
            # while (random move is not a safe or a mine) and (there are unchecked squares)
            while (auxcell not in self.moves_made.union(self.mines)) and (len(self.safes)+len(self.mines)<(self.height-1)*(self.width-1)):
                return auxcell

