from collections import deque
import os
import keyboard
from pynput.keyboard import Key, Listener
from colorama import Fore
from colorama import Style
import time

def limpiar_pantalla():
        if os.name == "posix":
            os.system("clear")
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            os.system("cls")

def juego():
    n, m = [int(x) for x in input().strip().split(' ')] 
    #n=9
    #m=9
    #mat = [[] for x in range(n)] 
    mat=[]
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    dd = list("DURL") 
    
    #Ingresar los valores a la matriz:
    # for i in range(n):
    #     mat[i] = list(input())

    limpiar_pantalla()

    def read_txt(filename):
        u=0
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                mat.append([x for x in line.strip()])
        

    def map():
        for i in range(n):
            for j in range(m):
                if mat[i][j] == '.':
                    print("x ", end="")
                elif mat[i][j] == 'J':
                    print(f'{Fore.GREEN}x{Style.RESET_ALL} ', end="")
                elif mat[i][j] == 'A':
                    print(f'{Fore.RED}x{Style.RESET_ALL} ', end="")
                elif mat[i][j] == '#':
                    print("- ", end="")
            print("\n", end="")

    def change_matriz_bot():
        for i in range(n):
            for j in range(m):
                if mat[i][j]=='A':
                    mat[i][j]='.'

    def bot():
        def valid(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (mat[r][c] != '#') and (p[r][c] == -1)
        def gana_bot(r,c):
            return (r==8) and (c>=0) and (c<9)
        def reconstruct_path(k):
            limpiar_pantalla()
            x, y  = tuple(T[k])
            path = deque()
            while p[x][y] >= 0:
                i = p[x][y] 
                path.appendleft(dd[i])
                x -= dx[i]
                y -= dy[i]

            change_matriz_bot()
            if path[0]=='D':
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x+1][y]='A'
            elif path[0] =='U':
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x-1][y]='A'
            elif path[0] =='R':
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x][y+1]='A'
            else:
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x][y-1]='A'
            map()
        start = (-1, -1)
        T=[[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7],[8,8]]
        for i in range(n):
            for j in range(m):
                if mat[i][j] =='A' and mat[i+1][j]=='J':
                    limpiar_pantalla()
                    change_matriz_bot()
                    mat[i+2][j]='A'
                    map()
                    return              
                else:
                    if mat[i][j] == 'A':
                        start = (i, j)
        p = [[-1 for y in range(m)] for x in range(n)]
        p[start[0]][start[1]] = -2
        q = deque([start])

        while len(q):
            x, y = q.popleft()
            for k in range(len(T)):
                if (x, y) == tuple(T[k]):
                    reconstruct_path(k)
                    return
                
                for i in range(4):
                    nx, ny = x + dx[i], y + dy[i]
                    if valid(nx, ny):
                        p[nx][ny] = i
                        q.append((nx, ny))
        return False

    def jugador():

        def colision_cerca(x,y):
            if mat[x][y] =='#':
                return False
            return True

        def gana_jugador(r,c):
            return (r==0) and (c>=0) and (c<9)

        def change_matriz_jugador():
            for i in range(n):
                for j in range(m):
                    if mat[i][j]=='J':
                        mat[i][j]='.'

        def es_movimiento_valido(x, y):
            res = (x >= 0) and (x < n)
            res = res and (y >= 0) and (y < m)
            res = res and (mat[x][y] != '#')
            res = res and (mat[x][y] !='A')
            if not res:
                return False
            else:
                return True

        def mover_jugador(movimiento):
            def diagonal():
                if mat[jugador_coords[0]-1][jugador_coords[1]+1]=='#':
                    jugador_coords[0] = jugador_coords[0] - 1
                    jugador_coords[1] = jugador_coords[1] - 1
                elif mat[jugador_coords[0]-1][jugador_coords[1]-1]=='#':
                    jugador_coords[0] = jugador_coords[0] - 1
                    jugador_coords[1] = jugador_coords[1] + 1

            change_matriz_jugador()
            
            if movimiento == "arriba":
                if mat[jugador_coords[0]-1][jugador_coords[1]]=='A' and mat[jugador_coords[0]-2][jugador_coords[1]]=='.':
                    jugador_coords[0] = jugador_coords[0] - 2

                else:
                    jugador_coords[0] = jugador_coords[0] - 1
                
            elif movimiento == "abajo":
                jugador_coords[0] = jugador_coords[0] + 1
                
            elif movimiento == "derecha":
                jugador_coords[1] = jugador_coords[1] + 1
                
            elif movimiento == "izquierda":
                jugador_coords[1] = jugador_coords[1] - 1
            
            elif movimiento == "diaizq":
                jugador_coords[0] = jugador_coords[0] - 1
                jugador_coords[1] = jugador_coords[1] - 1

            elif movimiento == "diader":
                jugador_coords[0] = jugador_coords[0] - 1
                jugador_coords[1] = jugador_coords[1] + 1
            
            mat[jugador_coords[0]][jugador_coords[1]] = 'J'
            
            map()

        def on_press(key):
            if key == Key.esc:
                return False
                
            elif str(key) == "'w'":

                if es_movimiento_valido(jugador_coords[0] - 1, jugador_coords[1]):
                    limpiar_pantalla()
                    mover_jugador("arriba")
                    return False    
                    
            elif str(key) == "'s'":
                
                if es_movimiento_valido(jugador_coords[0] + 1, jugador_coords[1]):
                    limpiar_pantalla()
                    mover_jugador("abajo")
                    return False

            elif str(key) == "'a'":
                
                if es_movimiento_valido(jugador_coords[0], jugador_coords[1]-1):
                    limpiar_pantalla()
                    mover_jugador("izquierda")
                    return False
            
            elif str(key) == "'d'":
                
                if es_movimiento_valido(jugador_coords[0], jugador_coords[1]+1):
                    limpiar_pantalla()
                    mover_jugador("derecha")
                    return False
            
            elif str(key) == "'q'":
                
                if es_movimiento_valido(jugador_coords[0]-1, jugador_coords[1]-1) \
                    and mat[jugador_coords[0]-1][jugador_coords[1]]=='A' and mat[jugador_coords[0]-2][jugador_coords[1]]=='#':
                    limpiar_pantalla()
                    mover_jugador("diaizq")
                    return False

            elif str(key) == "'e'":
                
                if es_movimiento_valido(jugador_coords[0]-1, jugador_coords[1]+1) \
                    and mat[jugador_coords[0]-1][jugador_coords[1]]=='A' and mat[jugador_coords[0]-2][jugador_coords[1]]=='#':
                    limpiar_pantalla()
                    mover_jugador("diader")
                    return False
                
            else:
                return True
            
            return True

        finalizado=True
        start = (-1, -1)
        T=[[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8]]
        for i in range(n):
            for j in range(m):
                if mat[i][j] == 'J':
                    jugador_coords = [i,j]

        with Listener(
            on_press=on_press) as listener:
            listener.join()
        
        return (gana_jugador(jugador_coords[0], jugador_coords[1])==False)

    #Ingresar los valores por archivo txt:
    read_txt('tablero.txt')        
    #Número de jugada del bot
    B=[int(x) for x in range(1,20)]
    u=0

    #Número de jugada del jugador
    J=[int(x) for x in range(1,20)]
    v=0
    turno=False

    map()
    while True:
        if turno==False:
            print("Turno Jugador")
            turno = jugador()
            v+=1
            if turno==False:
                print("Ganador-> Jugador")
                exit(0)

        elif turno==True:
            print("Turno Bot")
            time.sleep(2)
            bot()
            u+=1
            turno=False


if __name__ == '__main__':
    print("####################")
    print("#Bienvenido Jugador#")
    print("#    Tu Objetivo   #")
    print("#  LLegar al lado  #")
    print("#    opuesto del   #")
    print("#      tablero     #")
    print("#...Buena suerte...#")
    os.system("PAUSE")
    limpiar_pantalla()
    juego()
