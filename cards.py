import random
from igrok import HumanPlayer 
import pravila

class Game:
    def __init__(self, numHuman, deck=[]):
        if deck == []:
            self.deck = ['6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',\
                         '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦',\
                         '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',\
                         '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠']
            random.shuffle(self.deck)
        else:
            self.deck = deck
        self.trump = self.deck[0]
        # определяем игроков
        self.players = []
        for i in range(numHuman):
            self.players.append(HumanPlayer("Игрок " + str(i+1)))
            for _ in range(6):
                self.players[i].addCard(self.drawCard())

    def runFullGame(self):
        '''Начало ИГРЫ'''
        print('Добро пожаловать в дурак. Козырная карта - '+ self.trump)
        print('Делайте ходы')
        self.players = pravila.playOrder(self.players,self.trump[-1])

        while len(self.players) > 1:
            attacker = self.players[0]  # Ходит первым аттакующий
            defender = self.players[1]  #Защищающийся после
            inPlay = []                 #Карты которые играются в этом раунде
            attackCount = 0
            maxAttackCount = min(len(defender.hand),6) #максимальное количество возможных ходов или 6 или же то количество катр которое осталось в руке у защищающегося
            attack = attacker.promptFirstAttack(defender)
            inPlay.append(attack) # Добавляется карта, которой сделали ход
            attackCount +=1
            defence = defender.promptDefence(attacker, attack, self.trump)
            while defence != "" and attack != "":
                inPlay.append(defence)
                print(defender.name + " отбился катрой"+ defence + ". Карты на столе: ")
                print(inPlay)
                attack = attacker.promptFollowupAttack(defender, inPlay, attackCount, maxAttackCount)
                if attack != "": # Если игрок атаковал
                    inPlay.append(attack)
                    attackCount += 1
                    defence = defender.promptDefence(attacker, attack, self.trump)
            if defence == "": # Если защищиающийся не может/хочет отбиваться
                print(defender.name + " поднял карты")
                print(inPlay," добавлены в колоду ",defender.name)
                defender.hand += inPlay
                for player in self.players: #Игроки пополняют карты до тех пор пока они есть в колоде
                    if len(player.hand) < 6:
                        for _ in range(min(6 - len(player.hand), len(self.deck))):
                            player.addCard(self.drawCard())
                self.players = self.players[2:] + self.players[:2] #Защищающийся пропускает  ход
            if attack == "": #attacker has chosen to stop attacking
                print("Атака завершена. Бита: ")
                print(inPlay)
                for player in self.players: #all players draw cards until they have 6, starting at the attacker, so long as there are cards in the deck
                    if len(player.hand) < 6:
                        for _ in range(min(6 - len(player.hand), len(self.deck))):
                            player.addCard(self.drawCard())
                self.players = self.players[1:] + self.players[:1] #Атакующий идет в конец очереди
            self.players = list(filter(lambda x: len(x.hand) != 0, self.players))
            if len(self.players) == 1: #Победитель
                print(self.players[0].name + " Победитель!!!")
            if len(self.players) == 0: #Ничья
                print("Ничья!!!")






    def drawCard(self):
        """берет последнюю карту из колоды и возвращаеи её значение"""
        if self.deck != []:
            dealtCard = self.deck[-1]
            self.deck = self.deck[:-1]
            return dealtCard

game = Game(2)
game.runFullGame()