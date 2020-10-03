from collections import deque
import os
import keyboard
from pynput.keyboard import Key, Listener
from colorama import Fore
from colorama import Style
import time
from math import *

def limpiar_pantalla():
        if os.name == "posix":
            os.system("clear")
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            os.system("cls")

def juego():
    print("Ingrese las filas(entero).Luego, separado de un espacio, ingrese las columnas(entero):  ")
    print("Ejemplo: 9 9")
    n=9
    m=9
    mat=[]
    dx = [1, 1, 1, 0, 0, -1,2] 
    dy = [-1, 1, 0, 1, -1, 0,0]
    dd = list("GWDRLUS")

    limpiar_pantalla()

    def read_txt(filename):
        u=0
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                mat.append([x for x in line.strip()])
        
    def map():
        print("  ",end="")
        for l in range(n):
            print(l,end=" ")
        print("\n", end="")
        for i in range(n):
            print(i,end=" ")
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

        def diagonal(x,y):
            if (x>6) or (y>6):
                return False
            else:
                if mat[x+1][y]=='J' and mat[x+2][y]=='#' and x<=6 and y<=6:
                    return True
                    
            return False
        
        def salto_doble(x,y):
            if (x>6) or (y>6):
                return False
            else:
                if mat[x+1][y]=='J' and mat[x+2][y]=='.':
                    return True
            
            return False

        def bfs():
            while len(q):
                x, y = q.popleft()
                for k in range(len(T)):
                    if (x, y) == tuple(T[k]):
                        reconstruct_path(k)
                        return

                if (diagonal(x,y)):
                    for i in range(2):
                        nx, ny = x+dx[i], y+dy[i]
                        if valid_bfs(nx, ny):
                            p[nx][ny] = i
                            q.append((nx, ny))
                            
                elif (salto_doble(x,y)):
                        nx, ny = x+dx[6], y+dy[6]
                        if valid_bfs(nx, ny):
                            p[nx][ny] = 6
                            q.append((nx, ny))
                
                for i in range(2,6):
                    nx, ny = x + dx[i], y + dy[i]
                    if valid_bfs(nx, ny):
                        p[nx][ny] = i
                        q.append((nx, ny))

        def dfs():
            while len(q)>0:
                x,y =q.popleft()
                vis[x][y] = True
                for k in range(len(T)):
                    if (x,y) == tuple(T[k]):
                        reconstruct_path(k)
                        return
                    
                if (diagonal(x,y)):
                    for i in range(2):
                        nx, ny = x+dx[i], y+dy[i]
                    if valid_dfs(nx, ny):
                        p[nx][ny] = i
                        q.append((nx, ny))
                        
                elif (salto_doble(x,y)):
                    nx, ny = x+dx[6], y+dy[6]
                    if valid_dfs(nx, ny):
                        p[nx][ny] = 6
                        q.append((nx, ny))
                    
                for i in range(2,6):
                    nx, ny = x+dx[i], y+dy[i]
                    if valid_dfs(nx, ny):
                        p[nx][ny] = i
                        q.append((nx, ny))

        def bot_tercer_algoritmo():
            mov_posibles = list()
            mov_direccion_final = -1

            bot_coords = [[], []]

            for x in range(n):
                for y in range(m):
                    if mat[x][y] == "A":
                        bot_coords[0] = x
                        bot_coords[1] = y

            def valid(r, c):
                return (r >= 0) and (r < n) and (c >= 0) and (c < m) \
                    and (mat[r][c] == ".")

            def calcular_distancia(r, c):
                return math.sqrt((n - r) ** 2 + (m - c) ** 2)

            for i in range(4):
                if valid(bot_coords[0] + dx[i], bot_coords[1] + dy[i]):
                    mov_posibles.append([i, calcular_distancia(bot_coords[0] + dx[i], bot_coords[1] + dy[i])])
                    print(calcular_distancia(bot_coords[0] + dx[i], bot_coords[1] + dy[i]))

            menor_distancia = mov_posibles[0][1] # suponemos que el primer movimiento posible guardado es el menor

            for i in range(len(mov_posibles)):
                if mov_posibles[i][1] < menor_distancia:
                    menor_distancia = mov_posibles[i][1]
                    mov_direccion_final = mov_posibles[i][0]

            change_matriz_bot()

            bot_coords[0] = bot_coords[0] + dx[mov_direccion_final]
            bot_coords[1] = bot_coords[1] + dy[mov_direccion_final]
            mat[bot_coords[0]][bot_coords[1]] = "A"

            return False
    
        def valid_bfs(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (mat[r][c] != '#') and (p[r][c] == -1) and (mat[r][c] =='.')

        def valid_dfs(r, c):
            return (r >= 0) and (r<n) and (c >= 0) and (c < m) \
                and (mat[r][c] != '#') and (p[r][c] == -1) and (mat[r][c] =='.') and (not vis[r][c])

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

            if path[0] =='G':
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x+1][y-1]='A'

            elif path[0] =='W':
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x+1][y+1]='A'    

            elif path[0]=='D':
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

            elif path[0] =='L':
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x][y-1]='A'

            else:
                if gana_bot(x+1,y):
                    mat[x+1][y]='A'
                    
                    map()
                    print("Bot -> Ganador")
                    exit(0)
                mat[x+2][y]='A'


            map()

        start = (-1, -1)
        T=[[8,0],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7],[8,8]]
        for i in range(n):
            for j in range(m):
                if mat[i][j] == 'A':
                    start = (i, j)
        vis = [[False for y in range(m)] for x in range(n)]
        p = [[-1 for y in range(m)] for x in range(n)]
        p[start[0]][start[1]] = -2
        q = deque([start])
        
        #PROBAMOS LOS ALGORITMOS DE BÚSQUEDA:
        #bfs()
        dfs()
        #bot_tercer_algoritmo()

        
        return False

    def jugador():

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
            if not res:
                return False
            else:
                return True

        def mover_jugador(movimiento):
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
                
            if str(key) == "'w'":

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
    turno=False

    map()
    while True:
        if turno==False:
            print("Turno Jugador")
            turno = jugador()
            if turno==False:
                print("Ganador-> Jugador")
                exit(0)

        elif turno==True:
            print("Turno Bot")
            time.sleep(2)
            bot()
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