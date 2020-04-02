#!usr/bin/python3

import wx, string, functools, random

alphabet = string.ascii_uppercase

words = [
    "apple",
    "Hangman",
    "planet",
    "circular",
    "horrific",
    "blaze",
    "lighting",
    "teapot",
    "snow",
    "discrete",
    "intrinsic",
    "stupendous",
    "entertaining",
    "statuesque",
    "tomatoes",
    "connection",
    "adaptable",
    "energetic",
    "envy",
    "recess",
    "nauseating",
    "innovate",
    "aspiring",
    "dispensable",
    "aspiring",
    "detail",
    "imaginary",
    "flavor",
    "distribution",
    "destruction",
    "wooden",
    "economic",
    "promise",
    "live",
    "wave",
    "spring",
]

words = [el.upper() for el in words]


class Hangman(wx.Frame):
    def __init__(self, *args, **kw):
        super(Hangman, self).__init__(*args, **kw)

        self.countTries = 0
        self.pluralOrSingular = ""
        self.word = ""
        self.hiddenWord = ""
        self.textSentence = ""

        self.InitUI()
        self.SetTitle("Hangman")
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#ffffff")

        self.word = random.choice(words)
        self.countTries = 6
        self.pluralOrSingular = "tries"

        if len(self.word) - 2 >= 1:
            missing = "?" * (len(self.word) - 2)

        self.hiddenWord = self.word[0] + missing + self.word[-1]
        self.textSentence = "Guess the word! You have {} {} left!".format(self.countTries, self.pluralOrSingular)

        self.text1 = wx.StaticText(panel, label=self.hiddenWord, style=wx.ALIGN_CENTER)
        self.text2 = wx.StaticText(panel, label=self.textSentence, style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)

        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        self.text1.SetFont(font)
        self.text2.SetFont(font)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.text1, flag=wx.ALL | wx.ALIGN_CENTER, border=25)
        self.vbox.Add(self.text2, flag=wx.ALL | wx.ALIGN_CENTER, border=25)

        ############################################################
        # REPLACE IMAGE PATH WITH PATH TO IMAGES OR THEY WONT WORK #
        ############################################################
        self.hangmanImg = wx.Bitmap("hangman0.jpg", wx.BITMAP_TYPE_ANY)
        self.bitmapCtrl = wx.StaticBitmap(panel, id=-1, bitmap=self.hangmanImg, pos=(180, 260), name="hangmanCtrl")

        posCounterX = 30
        posCounterY = 200

        for i in range(26):
            if i == 13:
                posCounterY += 30
            posCounterX = (posCounterX % 420) + 30

            letter = str(alphabet[i])
            button = wx.Button(panel, label=letter, pos=(posCounterX, posCounterY), size=(30, 30))

            func = functools.partial(self.press_button, label=letter)
            button.Bind(wx.EVT_BUTTON, func)

        panel.SetSizer(self.vbox)
        self.SetSize(500, 480)

    def press_button(self, event, label):
        if self.textSentence != "You lose!" and self.textSentence != "You win!":
            currLetter = label[:]
            listOG = list(self.word)
            listEncrypted = list(self.hiddenWord)

            if currLetter in listOG:
                for el in range(0, len(listEncrypted)):
                    if currLetter == listOG[el]:
                        listEncrypted[el] = currLetter

                self.hiddenWord = "".join(str(e) for e in listEncrypted)
                self.checkCondition()
            else:
                self.countTries = self.countTries - 1
                self.checkCondition()

    def checkCondition(self):
        if self.hiddenWord == self.word:
            self.textSentence = "You win!"
            self.updateUI()

        elif self.countTries > 1:
            self.textSentence = "Guess the word! You have {} {} left!".format(self.countTries, self.pluralOrSingular)
            self.updateUI()

        elif self.countTries == 1:
            self.pluralOrSingular = "try"
            self.textSentence = "Guess the word! You have {} {} left!".format(self.countTries, self.pluralOrSingular)
            self.updateUI()

        else:
            self.textSentence = "You lose!"
            self.updateUI()


    def updateUI(self):
        ############################################################
        # REPLACE IMAGE PATH WITH PATH TO IMAGES OR THEY WONT WORK #
        ############################################################
        self.hangmanImg = wx.Bitmap("hangman%d.jpg" % (6 - self.countTries), wx.BITMAP_TYPE_ANY)
        self.bitmapCtrl.SetBitmap(self.hangmanImg)
        self.text1.SetLabel(self.hiddenWord)
        self.text1.SetSize(self.text1.GetTextExtent(self.text1.GetLabel()))
        self.text2.SetLabel(self.textSentence)


def main():

    app = wx.App()
    prog = Hangman(None)
    prog.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
