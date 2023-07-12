import socket
import time
import pygame

FPS = 100
WIDTH_ROOM, HEIGHT_ROOM = 4000, 4000
WIDTH_SERVER_WINDOW, HEIGHT_SERVER_WINDOW = 300, 300
START_PLAYER_SIZE = 15

class Player():
        def __init__(self, conn, addr, x, y, r, colour) -> None:
                self.conn = conn
                self.addr = addr
                self.x = x
                self.y = y
                self.r = r
                self.colour = colour

                self.errors = 0

# создание сокета
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #отвечает за прием сообщений от пользователей
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) #отключает алгоритм нагла
main_socket.bind(('localhost', 10000))
main_socket.setblocking(0)
main_socket.listen(5)

#создадание графического окна сервера
pygame.init()
screen = pygame.display.set_mode((WIDTH_SERVER_WINDOW, HEIGHT_SERVER_WINDOW))
clock = pygame.time.Clock()
players = []
server_works = True
while server_works:
        clock.tick(FPS)
        #проверим есть ли желающие войти в игру
        try:
                new_socket, addr=main_socket.accept()
                print('Подключился ', addr)
                new_socket.setblocking(0)
                new_player = Player(new_socket, addr, 100, 200, START_PLAYER_SIZE, 'green')

                players.append(new_player)
                
        except:
                #print('Нет желающих войти в игру')
                pass


        #считываем комманды
        for player in players:
                
                try:
                        data = player.conn.recv(1024)
                        data = data.decode()
                        print('Получил ', data)
                except:
                        pass
                


        #обрабатываем команды, изменяем базу

        #Возвращаем базу
        for player in players:
                try:
                        player.conn.send('Новое состояние игры'.encode())
                        player.errors = 0
                except:
                        player.errors += 1

        #чистим список от отвалившехся игроков
        for player in players:
                if player.errors == 500:
                        player.conn.close()
                        players.remove(player)

        #нарисуем состояние комнаты
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        server_works = False

        screen.fill('black')
        for player in players:
                x = round(player.x * WIDTH_SERVER_WINDOW / WIDTH_ROOM)
                y = round(player.y * HEIGHT_SERVER_WINDOW / HEIGHT_ROOM)
                r = round(player.r * WIDTH_SERVER_WINDOW / WIDTH_ROOM)

                pygame.draw.circle(screen, (255, 0, 0), (x, y), r)
        pygame.display.update()

pygame.quit()
main_socket.close()