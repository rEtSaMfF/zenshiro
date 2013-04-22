import sys, pygame
from pygame.locals import *

class Story():
    def __init__(self, font, size):
        self.font = font
        self.width = size[0]
        self.height= size[1]
        self.rendered = []
        self.poses = []
        self.howtos = (""
        , ""
        , "                     The Story So Far..."
        , ""
        , "  The space colony NeoTokyo has been in"
		, "  geosynchronous orbit around earth since the year" 
		, "  2511. Our hero, Zenshiro, was born in 2608. Zenshiro" 
		, "  was the fourth child born to a popular nobleman and" 
		, "  grew up to become a legendary samurai. The year is" 
		, "  now 2633 and NeoTokyo is under attack! A rival clan" 
		, "  of samurai have flown their giant robotic dragon" 
		, "  within range of the city and it's up to Zenshiro to" 
		, "  stop them! As the Dragon swoops down, Zenshiro" 
		, "  soars towards it with his jetpack. As he nears the"
		, "  robotic scales, he activates his magnetic boots to"
		, "  ensure he doesn't go flying off into the abyss during"
        , "	 battle. Zenshiro looks towards the dragon's head in" 
		, "  the distance. It's time to create some scrap metal." 
                             							 
							 
                        , "  Press [Enter] to return to the main menu"
                        , "  Hit [ESCAPE] at any time to quit :(")
        for string in range(0,len(self.howtos)):
            self.rendered.append(self.font.render(self.howtos[string], 1, (0, 100, 255)))
        for num in range(0, len(self.howtos)):
            self.poses.append((self.width / 2 - 335, self.height / 2 - (-num * 25) - 275))

def show_story(font, screen, size, background):
    story = Story(font, size)
    #screen.blit(background, (0, 0))
    screen.fill((0,0,0))
    for item, pos in zip(story.rendered, story.poses):
        screen.blit(item, pos)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
                if event.key == K_BACKSPACE:
                    return
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_q:
                    sys.exit()