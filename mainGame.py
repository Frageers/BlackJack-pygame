import pygame
import os
import random
from functions import *
# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 36)  # Default font, size 36
screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Blackjack Random Cards")
clock = pygame.time.Clock()

#all important variables
hand = playerHand()
dealHand = dealerHand()
playerBust = False
message = None
standS17 = font.render("Dealer stands on soft 17", True, (255, 255, 0))
BJPays = font.render("Blackjack pays 3:2", True, (255, 255, 0))
standS17Width = standS17.get_width()
standS17Height = standS17.get_height()
BJPaysWidth = BJPays.get_width()
BJPaysHeight = BJPays.get_height()
xPosStand17 = (screen.get_width() - standS17Width) // 2
xPosBJPays = (screen.get_width() - BJPaysWidth) // 2
yPosStand17 = (screen.get_height() - standS17Height) // 2
yPosBJPays = yPosStand17 + standS17Height + 10
gameState = "betting"
balance = 10000
currentBet = 0
splitActive = False
splitHand = []
currentHand = "main"

chipImages = {
    1: pygame.image.load("Casino/Chips/chips9.png").convert_alpha(),
    5: pygame.image.load("Casino/Chips/chips10.png").convert_alpha(),
    10: pygame.image.load("Casino/Chips/chips11.png").convert_alpha(),
    25: pygame.image.load("Casino/Chips/chips12.png").convert_alpha(),
    100: pygame.image.load("Casino/Chips/chips13.png").convert_alpha(),
    500: pygame.image.load("Casino/Chips/chips14.png").convert_alpha(),
    1000: pygame.image.load("Casino/Chips/chips15.png").convert_alpha(),
    5000: pygame.image.load("Casino/Chips/chips16.png").convert_alpha(),
}
for value in chipImages:
    chipImages[value] = pygame.transform.scale(chipImages[value], (75, 75))
running = True
while running:
    
    screen_width, screen_height = screen.get_size()
    button_width = screen_width // 6
    button_height = screen_height // 10
    button_margin = screen_width // 50
    
    buttonRectHit = pygame.Rect(button_margin, screen_height - button_height - button_margin, button_width, button_height)
    buttonRectDouble = pygame.Rect(button_margin * 2 + button_width, screen_height - button_height - button_margin, button_width, button_height)
    buttonRectStand = pygame.Rect(button_margin * 3 + button_width * 2, screen_height - button_height - button_margin, button_width, button_height)
    buttonRectSplit = pygame.Rect(button_margin * 4 + button_width * 3, screen_height - button_height - button_margin, button_width, button_height)
    

    if calculate_hand_value(hand) < 21:
        playerBust = False
    screen.fill((0, 100, 0))
    
    if gameState == "betting":
        dealText = font.render("Deal Hand", True, (255, 255, 255))
        balanceText = font.render(f"Balance: {balance}", True, (255, 255, 255))
        currentBetText = font.render(f"Current Bet: {currentBet}", True, (255, 255, 255))
        screen.blit(balanceText, (500, 500))
        screen.blit(currentBetText, (900, 500))
        chipRects = [
            pygame.Rect(500, 350, 75, 75),
            pygame.Rect(580, 350, 75, 75),
            pygame.Rect(660, 350, 75, 75),
            pygame.Rect(740, 350, 75, 75),
            pygame.Rect(820, 350, 75, 75),
            pygame.Rect(900, 350, 75, 75),
            pygame.Rect(980, 350, 75, 75),
            pygame.Rect(1060, 350, 75, 75),
        ]
        chipValues = [1, 5, 10, 25, 100, 500, 1000, 5000]
        drawPokerChips(screen, chipRects, chipValues, chipImages)
        betDone = pygame.draw.rect(screen, (0, 102, 102), (500, 200, 200, 100))
        screen.blit(dealText, (550, 250))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if gameState == "betting":
                for rect, value in zip(chipRects, chipValues):
                    if rect.collidepoint(mouse_pos):
                        if balance >= value:
                            currentBet += value
                            balance -= value
                            print(f"Current Bet: {currentBet}, Balance: {balance}")
                if betDone.collidepoint(mouse_pos) and currentBet > 0:
                    gameState = "playing"
                    message = None
                    print(f"final bet: {currentBet}, Balance: {balance}")
            
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Press SPACE to deal new cards
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameState == "roundOver":
                    gameState = "betting"
                    currentBet = 0
                    hand = playerHand()
                    dealHand = dealerHand()
                    message = None
                    splitActive = False
                    if calculate_hand_value(hand) == 21 and len(hand) == 2:
                        message = "Blackjack! You win!"
                        gameState = "gameOver"
                    elif calculate_hand_value(hand) > 21:
                        message = "You Bust!"
                        gameState = "gameOver"
                        playerBust = True
                    else:
                        message = None
        if isClicked(buttonRectHit, event) and not playerBust:
            if currentHand == "main":
                hand.append(load_random_card())
                playerScore = calculate_hand_value(hand)
            else:
                splitHand.append(load_random_card())
            if calculate_hand_value(hand) > 21 and splitActive:
                if currentHand == "main":
                    currentHand = "split"
                    message = "Playing second hand"
                    drawPlayerCards(screen, splitHand)
                else:
                    message = "You Bust!"
                    gameState = "gameOver"
                    playerBust = True
            elif calculate_hand_value(hand) > 21:
                message, balance, gameState = checkWinner(hand, dealHand, balance, currentBet, splitActive, splitHand, playerBust)
                playerBust = True
            elif currentHand == "split" and calculate_hand_value(splitHand) > 21:
                message, balance, gameState = checkWinner(hand, dealHand, balance, currentBet, splitActive, splitHand, playerBust)
                playerBust = True
                
        if isClicked(buttonRectStand, event) and not playerBust:
            if currentHand == "main" and splitActive:
                currentHand = "split"
                message = "Playing second hand"
            else:               
                playerBust = True
                dealHand[1] = load_random_card()  # Reveal dealer's hidden card
                while calculate_hand_value(dealHand) < 17:
                    dealHand.append(load_random_card())
                message, balance, gameState = checkWinner(hand, dealHand, balance, currentBet, splitActive, splitHand, playerBust)
                gameState = "roundOver"
        if isClicked(buttonRectDouble, event) and not playerBust:
            if not splitActive:
                if len(hand) == 2 and balance >= currentBet:
                    balance -= currentBet
                    currentBet *= 2
                    hand.append(load_random_card())
                    playerBust = True  # Force end of player turn
                    dealHand[1] = load_random_card()  # Reveal dealer's hidden card
                    while calculate_hand_value(dealHand) < 17:
                        dealHand.append(load_random_card())
                    message, balance, gameState = checkWinner(hand, dealHand, balance, currentBet, splitActive, splitHand, playerBust)
                    gameState = "roundOver"
            else:
                # Double for split hand
                if currentHand == "main" and len(hand) == 2 and balance >= currentBet // 2:
                    balance -= currentBet // 2
                    hand.append(load_random_card())
                    currentHand = "split"
                    message = "Playing second hand"
                    playerBust = False
                elif currentHand == "split" and len(splitHand) == 2 and balance >= currentBet // 2:
                    balance -= currentBet // 2
                    splitHand.append(load_random_card())
                    playerBust = True
                    dealHand[1] = load_random_card()
                    while calculate_hand_value(dealHand) < 17:
                        dealHand.append(load_random_card())
                    message, balance, gameState = checkWinner(hand, dealHand, balance, currentBet, splitActive, splitHand, playerBust)
                    gameState = "roundOver"

        if isClicked(buttonRectSplit, event) and not playerBust:
            if hand[0][1] == hand[1][1] and balance >= currentBet and not splitActive:
                balance -= currentBet
                currentBet *= 2
                splitActive = True
                splitHand = [hand.pop()]
                hand.append(load_random_card())
                splitHand.append(load_random_card())
                currentHand = "main"
                message = "Playing first hand"

    
    if gameState != "betting":
        playerStats = font.render(f"Player Hand: {calculate_hand_value(hand)}", True, (255, 255, 255))
        dealerStats = font.render(f"Dealer Hand: {calculate_hand_value(dealHand)}", True, (255, 255, 255))
        screen.blit(standS17, ((screen_width - standS17.get_width()) // 2, screen_height // 15))
        screen.blit(BJPays, ((screen_width - BJPays.get_width()) // 2, screen_height // 15 + 40))
        
        
        screen.blit(playerStats, (screen_width // 20, screen_height // 5 - 40))
        screen.blit(dealerStats, (screen_width - dealerStats.get_width() - screen_width // 20, screen_height // 5 - 40))
        if splitActive:
            secondHandStats = font.render(f"Second Hand: {calculate_hand_value(splitHand)}", True, (255, 255, 255))
            screen.blit(secondHandStats, (screen_width // 5, screen_height // 5 - 40))
        currentBetText = font.render(f"Current Bet: {currentBet}", True, (255, 255, 255))
        screen.blit(currentBetText, (700, 500))
        
        
        drawPlayerCards(screen, hand)
        if splitActive:
            drawSplitCards(screen, splitHand)
        drawDealerCards(screen, dealHand)
        
            
        #draw hit button
        drawButtonHit(screen, (0, 102, 102), buttonRectHit, "Hit")
        drawButtonHit(screen, (0, 102, 102), buttonRectDouble, "Double")
        drawButtonHit(screen, (0, 102, 102), buttonRectStand, "Stand")
        drawButtonHit(screen, (0, 102, 102), buttonRectSplit, "Split")
        
    if message:
        text = font.render(message, True, (255, 255, 0))
        screen.blit(text, (100, 600))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()