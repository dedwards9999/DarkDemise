from ursina import Ursina
import Game

#ursina.application.development_mode = False

app = Ursina()
Game.init()
app.run()
