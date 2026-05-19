import sound

class Mood:
    def play_sound(self): pass

class HappyMood(Mood):
    def play_sound(self):
        sound.happy.play()

class AngryMood(Mood):
    def play_sound(self):
        sound.angry.play()

class BoredMood(Mood):
    def play_sound(self):
        sound.bored.play()

class NeutralMood(Mood):
    def play_sound(self):
        sound.neutral.play()

class SadMood(Mood):
    def play_sound(self):
        sound.sad.play()
