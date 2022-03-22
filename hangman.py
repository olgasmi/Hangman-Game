import random
from words import words
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 25)
screen_width = 900
screen_height = 500
white = (255, 255, 255)

letters = [K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z]

images = [pygame.image.load("images/hang1.png"),
          pygame.image.load("images/hang2.png"),
          pygame.image.load("images/hang3.png"),
          pygame.image.load("images/hang4.png"),
          pygame.image.load("images/hang5.png"),
          pygame.image.load("images/hang6.png"),
          pygame.image.load("images/hang7.png"),
          pygame.image.load("images/hang8.png"),
          pygame.image.load("images/hang9.png"),
          pygame.image.load("images/hang10.png"),
          pygame.image.load("images/hang11.png")]


# words that will be guessed, will be written in lowercase
# some words has spaces or '-' character -> need to be excluded
def message(text_message, text_font):
    text_surface = text_font.render(text_message, True, white)
    return text_surface, text_surface.get_rect()


def message_display(text_message, x, y):
    text_surface, text_rect = message(text_message, font)
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(1100)


def hangman():
    word_to_guess = random.choice(words)
    while '-' in word_to_guess or ' ' in word_to_guess:
        word_to_guess = random.choice(words)

    return word_to_guess


def player(ascii_code, letters_code, user_letters_):
    if ascii_code in letters_code:
        letter = chr(ascii_code) #conversion
        user_letters_.add(letter)
        return letter
    return False


def check_if_contains(word_to_guess, letter, used_letters_):

    if letter in word_to_guess and letter not in used_letters_:
        used_letters_.add(letter)
        word_to_guess = list(filter(lambda l: l != letter, word_to_guess)) #all occurences need to be removed
        message_display("You have guessed letter :)", screen_width / 2, screen_height - 50)
    elif letter in used_letters_:
        message_display("You have already used this letter!", screen_width / 2, screen_height - 50)
    else:
        message_display("Try again! The word you are looking for does not contain this letter :(", screen_width / 2, screen_height - 50)

    return word_to_guess


word_hangman = hangman()
word = set(word_hangman)
used_letters = set()
user_letters = set()

counter = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('HANGMAN GAME')

running = True
while running:
    # user click quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            result = player(event.key, letters, user_letters)
            if not result:
                message_display('Try again!', screen_width / 2, screen_height - 50)
            else:
                new_word = check_if_contains(word, result, used_letters)
                if len(new_word) == len(word):
                    counter += 1
                word = new_word

    used_letters_text = font.render('  '.join(user_letters), True, white)
    used_letters_text_rect = used_letters_text.get_rect()
    used_letters_text_rect.topleft = (50, screen_height / 2)

    display_user_letters = font.render('Used letters:', True, white)
    display_user_letters_rect = display_user_letters.get_rect()
    display_user_letters_rect.center = (150, screen_height / 2 - 40)

    current_guess = ' '.join([quick_shot if quick_shot in used_letters else '_' for quick_shot in word_hangman])
    hangman = font.render(current_guess, True, white)
    hangman_rect = hangman.get_rect()
    hangman_rect.center = (550, screen_height / 2 - 100)

    screen.fill((10, 5, 80))
    screen.blit(images[counter], (50, 50))
    screen.blit(used_letters_text, used_letters_text_rect)
    screen.blit(display_user_letters, display_user_letters_rect)
    screen.blit(hangman, hangman_rect)

    if counter == 10:
        running = False
        message_display("YOU LOST!", screen_width / 2, screen_height - 50)
        pygame.time.wait(700)

    if not word:
        running = False
        message_display("YOU WIN! CONGRATULATIONS! :)", screen_width / 2, screen_height - 50)
        pygame.time.wait(700)

    pygame.display.update()

pygame.quit()
