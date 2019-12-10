import pravila

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def addCard(self, card):
        """Добавляет карты в руку"""
        if card != None:
            self.hand.append(card)

    def removeCard(self, index):
            """Удаляет карту по выбраному индексу"""
            self.hand = self.hand[:index] + self.hand[index+1:]




class HumanPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    def promptFirstAttack(self, defender):
        """Просим игрока начать раунд"""
        print(self.name + " атакует " + defender.name +\
              ". Выберите карту.")
        print( "Карты "+self.name+":")
        print(self.hand)
        selection = input("Выберете индекс карты, которой Вы хотите походить:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand)))) # Делает список возможных индексов
        while selection not in validOptions:
            selection = input("Неверный индекс. Выберете индекс карты, которой Вы хотите походить:")
        attack = self.hand[int(selection)]
        self.removeCard(int(selection))
        return attack

    def promptFollowupAttack(self, defender, inPlay, attackCount, maxAttackCount):
        """Просит игрока подкинуть если есть чем"""
        print(self.name +", хотите продолжить атаку?") 
        print("Выберете карту для атаки, или нажмите ENTER и пропустите ход.")
        print(self.hand)
        selection = input("Выберете индекс карты, которой Вы хотите походить:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand)))) + [""]
        while selection not in validOptions:
            selection = input("Неверный индекс. Выберете индекс карты, которой Вы хотите походить:")
        while selection != "" and not pravila.validAttack(self.hand[int(selection)], attackCount, maxAttackCount, inPlay):
            print('Так не пойдет, братишка. Давай еще раз')
            print("Карты в руке: ", inPlay)
            selection = input("Выберете индекс карты, которой Вы хотите походить:")
            while selection not in validOptions:
                selection = input("Неверный индекс. Выберете индекс карты, которой Вы хотите походить:")
        if selection == "":
                return ""
        attack = self.hand[int(selection)]
        self.removeCard(int(selection))
        return attack


    def promptDefence(self, attacker, attack, trump):
        """Просим игрока-защитника отбить атаку"""
        print(attacker.name+ " атакует "+ self.name +' картой '+ attack +'.') #
        print(self.name+", выберете карту, которой будет отбиваться или нажмите ENTER, чтобы поднять карту.")
        print(self.hand)
        selection = input("Выберете индекс карты, которой Вы хотите походить:")
        validOptions = list(map(lambda x: str(x),range(len(self.hand))))+[""] # Делает список возможных индексов плюс пустой список
        while selection not in validOptions:
            selection = input("Invalid index. Select the index of the card you wish to play:")
        while selection != "" and not pravila.validDefence(attack, self.hand[int(selection)], trump[-1]):
            # Проверяет привильна ли защита
            print((self.hand[int(selection)] + "не может отбить карту " + attack + '. Выберете другую, или нажмите ENTER, чтобы поднять')

            selection = input("Выберете индекс карты, которой Вы хотите походить:")
            while selection not in validOptions:
                selection = input("Неверный индекс. Выберете индекс карты, которой Вы хотите походить:")
        if selection != "":
            defence = self.hand[int(selection)]
            self.removeCard(int(selection))
            return defence
        return ""



    