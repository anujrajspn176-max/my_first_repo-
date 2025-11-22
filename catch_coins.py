#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 22 13:16:39 2025

@author: anujraj



""# catch_coins.py
import tkinter as tk
import random
import time

WIDTH = 500
HEIGHT = 600
PLAYER_W = 80
PLAYER_H = 15
COIN_SIZE = 20
INITIAL_SPEED = 6
SPAWN_INTERVAL = 900  # milliseconds

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Falling Coins!")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#101217")
        self.canvas.pack()

        # Score & lives
        self.score = 0
        self.lives = 3
        self.speed = INITIAL_SPEED

        # Player (basket)
        self.player_x = WIDTH // 2
        self.player = self.canvas.create_rectangle(
            self.player_x - PLAYER_W//2, HEIGHT - 40,
            self.player_x + PLAYER_W//2, HEIGHT - 40 + PLAYER_H,
            fill="#ffd166", outline="#ffd166"
        )

        # HUD
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Score: {self.score}",
                                                  fill="white", font=("Helvetica", 14))
        self.lives_text = self.canvas.create_text(10, 34, anchor="nw",
                                                  text=f"Lives: {self.lives}",
                                                  fill="white", font=("Helvetica", 14))

        # Controls
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # Game lists
        self.coins = []  # list of (id, x, y)
        self.running = True

        # Start loops
        self.spawn_coin()
        self.update()

    def move_left(self, event=None):
        if self.player_x - PLAYER_W//2 > 0:
            self.player_x -= 30
            self.canvas.move(self.player, -30, 0)

    def move_right(self, event=None):
        if self.player_x + PLAYER_W//2 < WIDTH:
            self.player_x += 30
            self.canvas.move(self.player, 30, 0)

    def spawn_coin(self):
        if not self.running:
            return
        x = random.randint(COIN_SIZE//2, WIDTH - COIN_SIZE//2)
        y = -COIN_SIZE
        coin_id = self.canvas.create_oval(
            x-COIN_SIZE//2, y-COIN_SIZE//2, x+COIN_SIZE//2, y+COIN_SIZE//2,
            fill="#4cc9f0", outline="#2b5f7a"
        )
        self.coins.append({'id': coin_id, 'x': x, 'y': y})
        # speed up spawn slowly as score increases
        interval = max(300, SPAWN_INTERVAL - self.score * 10)
        self.root.after(interval, self.spawn_coin)

    def update(self):
        if not self.running:
            return
        # Move coins
        for coin in list(self.coins):
            coin['y'] += self.speed
            self.canvas.move(coin['id'], 0, self.speed)

            # Check collision with player
            px1 = self.player_x - PLAYER_W//2
            px2 = self.player_x + PLAYER_W//2
            py1 = HEIGHT - 40
            # coin position
            cx = coin['x']
            cy = coin['y']

            if cy + COIN_SIZE//2 >= py1:
                # If coin within player's x-range -> caught
                if px1 <= cx <= px2:
                    self.catch_coin(coin)
                else:
                    self.miss_coin(coin)

        # Increase difficulty slowly
        if self.score and self.score % 10 == 0:
            # small boost (but avoid repeated boost same score)
            self.speed = INITIAL_SPEED + min(8, self.score // 10)

        # Update HUD
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")

        if self.lives <= 0:
            self.game_over()
            return

        # schedule next frame
        self.root.after(30, self.update)

    def catch_coin(self, coin):
        self.score += 1
        self.canvas.delete(coin['id'])
        self.coins.remove(coin)
        # small visual burst
        self.flash_text("+1", coin['x'], coin['y'], color="#ade8f4")

    def miss_coin(self, coin):
        self.lives -= 1
        self.canvas.delete(coin['id'])
        self.coins.remove(coin)
        self.flash_text("-1 Life", coin['x'], HEIGHT - 70, color="#ff6b6b")

    def flash_text(self, text, x, y, color="#fff"):
        t = self.canvas.create_text(x, y, text=text, fill=color, font=("Helvetica", 12, "bold"))
        def fade(step=0):
            if step > 10:
                self.canvas.delete(t)
                return
            # move up a bit
            self.canvas.move(t, 0, -2)
            self.root.after(40, lambda: fade(step+1))
        fade()

    def game_over(self):
        self.running = False
        self.canvas.create_rectangle(50, HEIGHT//2 - 60, WIDTH-50, HEIGHT//2 + 60, fill="#000000aa", outline="")
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 10, text="GAME OVER", fill="#ffd166", font=("Helvetica", 28, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text=f"Final Score: {self.score}", fill="white", font=("Helvetica", 16))

        # Restart button
        btn = tk.Button(self.root, text="Play Again", command=self.restart, bg="#4cc9f0", fg="black")
        self.canvas.create_window(WIDTH//2, HEIGHT//2 + 80, window=btn)

    def restart(self):
        self.canvas.delete("all")
        self.score = 0
        self.lives = 3
        self.speed = INITIAL_SPEED
        self.coins = []
        # recreate HUD and player
        self.player = self.canvas.create_rectangle(
            WIDTH//2 - PLAYER_W//2, HEIGHT - 40,
            WIDTH//2 + PLAYER_W//2, HEIGHT - 40 + PLAYER_H,
            fill="#ffd166", outline="#ffd166"
        )
        self.player_x = WIDTH//2
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Score: {self.score}",
                                                  fill="white", font=("Helvetica", 14))
        self.lives_text = self.canvas.create_text(10, 34, anchor="nw",
                                                  text=f"Lives: {self.lives}",
                                                  fill="white", font=("Helvetica", 14))
        self.running = True
        self.spawn_coin()
        self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()