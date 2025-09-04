from ursina import Ursina, EditorCamera
import Game

#ursina.application.development_mode = False

def update():
    Game.update()

app = Ursina()
Game.init()

app.run()
