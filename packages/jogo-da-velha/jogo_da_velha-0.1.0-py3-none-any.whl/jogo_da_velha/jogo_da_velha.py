import random
import os

fim_jogo = False
jogada = 0



class Player():
    
    def __init__(self, name, auto, sign):
        self.name = name
        self.auto = auto
        self.sign = sign
        
    def joga(self, tab, jogada):
        ok = False
        while not ok:
           aux = input("Jogador " + g.current_player.name + "! Digite posicao de 0 a 8 ")
           pos = int(aux)

           if pos not in range(9):
              print ('Digite numero de 0 a 8')
           elif not tab.posicao_vazia(pos):
              print ('Posição já selecionada')
           else:
              ok = True
    
        return pos

class AutoPlayer(Player):

    def __init__(self, name, auto, sign):
        super().__init__(name, auto, sign)

    def joga(self, tab, jogada):     

       borders = [0,2,6,8]
       not_borders = [1,3,5,7]
       if jogada == 1 or jogada == 3:
          posOk = False 
          while not posOk: 
            pos = random.choice(borders)
            if tab.posicao_vazia(pos) :
               posOk = True
          return pos

       if jogada == 2: 
          if tab.posicao_vazia(4) :
             pos = 4
             return pos
            
          posOk = False       
          while not posOk: 
            pos = random.choice(borders)
            if tab.posição_vazia(pos) :
               posOk = True
          return pos

       if jogada == 5 or jogada == 7:
          
          pos = tab.verifica_padrao21('X')
          if pos != 999:
             return pos
          else:  
             pos = tab.verifica_padrao21('0' )
             if pos != 999:
               return pos
            
          posOk = False 
          while not posOk: 
            pos = random.choice(borders)
            if tab.posicao_vazia(pos) :
               posOk = True

       if jogada == 4 or jogada == 6 or jogada == 8:
          
          pos = tab.verifica_padrao21('X')
          if pos != 999:
             return pos
          else:  
             pos = tab.verifica_padrao21('0' )
             if pos != 999:
               return pos
            
          posOk = False 
          while not posOk: 
            pos = random.choice(not_borders)
            if tab.posicao_vazia(pos):
               posOk = True

       if jogada in (6,8, 9):
          pos = tab.procura_vazio()
          
       return pos  

class Tabuleiro():
    line = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
        ]



    def __init__(self):
        self.tab = ['_']*9

    def posicao_vazia(self, pos):
        if self.tab[pos] == "_":
           return True
        else:
           return False 

    def marca_posicao(self, player,pos):
        self.tab[pos] = player.sign
        
    def procura_vazio(self):
        pos = 999
        for i in range(0,9):
            if self.tab[i] == "_":
               pos = i
        return pos

    def verifica_padrao21(self, padrao):

        conta_padrao = 0
        conta_vazio = 0
        pos_vazia = 999
        for i in range(0,8):
           for j in range (0,3) :
               if self.tab[self.line[i][j]] == padrao:
                  conta_padrao += 1
               else:
                  if self.tab[self.line[i][j]] == "_":
                     conta_vazio += 1
                     pos_vazia = int(self.line[i][j])
                  
           if conta_padrao == 2 and conta_vazio == 1:
              return pos_vazia
            
           conta_padrao = 0
           conta_vazio = 0
           pos_vazia = 999
            
        return 999

    

    def verifica_ganhador(self):

    
      for i in range(0,8):
          if self.tab[self.line[i][0]] != "_" and self.tab[self.line[i][1]] != "_" and self.tab[self.line[i][2]] != "_":
            if self.tab[self.line[i][0]] == self.tab[self.line[i][1]] == self.tab[self.line[i][2]] :
               return True;

      return False 
 
    def printTabuleiro(self,player):

        print (" Sua vez jogador : " + player.name)  

        os.system('clear') or None
        print('+-----------+')
        print('|',self.tab[0], "|", self.tab[1], "|", self.tab[2],'|')
        print('|','-'* 9,'|')
        print('|',self.tab[3], "|", self.tab[4], "|", self.tab[5],'|')
        print('|','-'* 9,'|')
        print('|',self.tab[6], "|", self.tab[7], "|", self.tab[8],'|')
        print('+-----------+')


class Game():
    
    def __init__(self, player):
        self.autoplayer = AutoPlayer('TTVS', True, 'X')
        self.player =  Player(player, False, '0')
        self.tabuleiro = Tabuleiro()
        self.current_player = None

    def set_current_player(self):
       if not self.current_player:
          n = random.choice([1,2])
          if n == 1:
             self.current_player = self.autoplayer
          else:
             self.current_player = self.player
       else: 
          if self.current_player.auto:
             self.current_player = self.player  
          else:
             self.current_player = self.autoplayer

    def joga(self, jogada):
       if self.current_player.auto:
           pos = self.autoplayer.joga(self.tabuleiro, jogada)
       else: 
          pos = self.player.joga(self.tabuleiro, jogada)
          
       return pos   

    def marca_posicao(self, pos):
        self.tabuleiro.marca_posicao(self.current_player, pos) 

    def printTabuleiro(self):
        self.tabuleiro.printTabuleiro(self.current_player)

    def verifica_ganhador(self):
        return self.tabuleiro.verifica_ganhador()
    
nameOk = False
while not nameOk:
   name = input ('Digite nome do jogador ===> ')
   if name :
      nameOk = True 

g = Game(name)

g.set_current_player()

a = input (g.current_player.name + ' começa jogando! Tecle Enter ')

g.printTabuleiro()

while not fim_jogo:
    
     jogada += 1

     pos = g.joga(jogada)
             
     g.marca_posicao(pos) 

     g.printTabuleiro()
     
     if jogada > 4 and g.verifica_ganhador():
        a = input ("O vencedor é " + g.current_player.name)
        break

     if jogada == 9:
        a = input("Fim do jogo")
        break


     g.set_current_player()


