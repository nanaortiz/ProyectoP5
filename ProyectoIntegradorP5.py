import os
import readchar
import random
from functools import reduce
from typing import List, Tuple

WALL = "#"
PATH = "."
PLAYER = "P"

def crear_laberinto_desde_cadena(maze_string: str, start: Tuple[int, int], end: Tuple[int, int]) -> List[List[str]]:
    maze = [list(row) for row in maze_string.strip().split("\n")]


class Juego:
    def __init__(self, maze: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]):
        self.px, self.py = start
        self.maze = maze
        self.start = start
        self.end = end
        self.place_player()

    def imprimir_instrucciones(self) -> None:
        print("\nINSTRUCCIONES: ")
        print("\tUsa las flechas para moverte, q para salir")

    def print_maze(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar pantalla
        for row in self.maze:
            print("".join(row))
        self.imprimir_instrucciones()

    def place_player(self) -> None:
        self.maze[self.py][self.px] = PLAYER
        
    def move_player(self, dx: int, dy: int) -> None:
        new_px, new_py = self.px + dx, self.py + dy
        if (
            0 <= new_px < len(self.maze[0])
            and 0 <= new_py < len(self.maze)
            and self.maze[new_py][new_px] != WALL
        ):
            self.maze[self.py][self.px] = PATH
            self.px, self.py = new_px, new_py
            self.place_player()
            
class JuegoArchivo(Juego):
    def __init__(self, map_folder: str):
        maze_file = self.elegir_archivo_aleatorio(map_folder)
        maze_data, start, end = self.leer_maze_desde_archivo(map_folder, maze_file)
        super().__init__(maze_data, start, end)

    def elegir_archivo_aleatorio(self, map_folder: str) -> str:
        files = os.listdir(map_folder)
        return random.choice(files)

    def leer_maze_desde_archivo(self, map_folder: str, file_name: str) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
        path_to_file = os.path.join(map_folder, file_name)
        with open(path_to_file, "r") as f:
            maze_content = f.readlines()
            maze_content = reduce(lambda x, y: x + y, map(str.strip, maze_content))
            rows = len(maze_content)
            cols = len(maze_content[0])
            start = (0, 0)
            end = (cols - 1, rows - 1)
            return maze_content, start, end
        
if __name__ == "__main__":
    # Configuración del laberinto generado
    maze_string = """
    ####################
    #..................#
    #.################.#
    #.#..............#.# 
    #.#.############.#.#
    #.#..............#.# 
    #.################.#
    #..................#
    ####################
    """

    start_position = (0, 0)
    end_position = (17, 8)

    juego = Juego(crear_laberinto_desde_cadena(maze_string, start_position, end_position), start_position, end_position)
    juego.print_maze()

    while (juego.px, juego.py) != juego.end:
        key = readchar.readkey()

        if key == "q":
            break
        elif key.lower() == "a" or key == readchar.key.LEFT:
            juego.move_player(-1, 0)
        elif key.lower() == "s" or key == readchar.key.DOWN:
            juego.move_player(0, 1)
        elif key.lower() == "d" or key == readchar.key.RIGHT:
            juego.move_player(1, 0)
        elif key.lower() == "w" or key == readchar.key.UP:
            juego.move_player(0, -1)
            