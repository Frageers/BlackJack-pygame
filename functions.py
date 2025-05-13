import pygame
import os
import random

ranks = {
    '02': '02',
    '03': '03',
    '04': '04',
    '05': '05',
    '06': '06',
    '07': '07',
    '08': '08',
    '09': '09',
    '10': '10',
    'jack': 'jack',
    'queen': 'queen',
    'king': 'king',
    'ace': 'ace'
}

suits = ['hearts', 'diamonds', 'clubs', 'spades']
card_folder = os.path.join("casino", "Cards")


def load_random_card():
    rank_key = random.choice(list(ranks.keys()))
    rank_filename = ranks[rank_key]
    suit = random.choice(suits)
    filename = f"{suit}_{rank_filename}.png"
    path = os.path.join(card_folder, filename)

    try:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (100, 145))  # Resize to 100x145
        return (img, rank_key)  # Return both the image and the rank (e.g., '05', 'jack', 'ace')
    except pygame.error:
        print(f"Failed to load image: {path}")
        return (None, None)


# Load initial hand (2 cards)
def playerHand():
    #card = load_random_card()
    #return [card, card]
    return [load_random_card(), load_random_card()]

def dealerHand():
    hidden_card_img = pygame.image.load(os.path.join("casino", "cards", "back08.png"))
    hidden_card_img = pygame.transform.scale(hidden_card_img, (100, 145))
    hidden_card = (hidden_card_img, None)  # Hidden card has no rank info yet
    return [load_random_card(), hidden_card]

def calculate_hand_value(hand):
    value = 0
    ace_count = 0
    for card in hand:
        img, rank = card
        if rank is None:
            continue  # Skip hidden cards (for dealer)
        if rank in ['jack', 'queen', 'king']:
            value += 10
        elif rank == 'ace':
            value += 11
            ace_count += 1
        else:
            value += int(rank)
    
    # If value > 21 and there are aces counted as 11, convert them to 1
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1

    return value

def drawButtonHit(surface, color, rect, text, text_color=(255, 255, 255)):
    pygame.draw.rect(surface, color, rect)
    font = pygame.font.Font(None, 40)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
def isClicked(rect, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            return True
    return False

def drawPlayerCards(surface, hand):
    for i, card in enumerate(hand):
        img, rank = card
        if img:
            surface.blit(img, (100 + i * 120, 225))
def drawSplitCards(surface, hand):
    for i, card in enumerate(hand):
        img, rank = card
        if img:
            surface.blit(img, (100 + i * 120, 405))
def drawDealerCards(surface, hand):
    startinngX = surface.get_width() - (len(hand) * 120 + 80)
    for i, card in enumerate(hand):
        img, rank = card
        if img: 
            surface.blit(img, (startinngX + i*120, 225))
def drawPokerChips(screen, chipRects, chipValues, chipImages):
    for rect, value in zip(chipRects, chipValues):
        chipImg = chipImages[value]
        screen.blit(chipImg, rect.topleft)

def checkWinner(player_hand, dealer_hand, balance, currentBet, splitActive, secondHand, playerBust):
    player_value = calculate_hand_value(player_hand)
    second_value = calculate_hand_value(secondHand) if splitActive else 0
    dealer_value = calculate_hand_value(dealer_hand)

    if splitActive:
        result = []

        # First hand outcome
        if player_value > 21:
            result.append("Player busts on the first hand")
        elif dealer_value > 21:
            balance += currentBet * 2
            result.append("Player wins on the first hand (dealer bust)")
        elif player_value == 21 and len(player_hand) == 2:
            balance += currentBet * 2.5
            result.append("Player hits blackjack on the first hand")
        elif player_value > dealer_value:
            balance += currentBet * 2
            result.append("Player wins on the first hand")
        elif player_value < dealer_value:
            result.append("Dealer wins on the first hand")
        else:
            balance += currentBet
            result.append("First hand pushes (tie)")

        # Second hand outcome
        if second_value > 21:
            result.append("Player busts on the second hand")
        elif dealer_value > 21:
            balance += currentBet * 2
            result.append("Player wins on the second hand (dealer bust)")
        elif second_value == 21 and len(secondHand) == 2:
            balance += currentBet * 2.5
            result.append("Player hits blackjack on the second hand")
        elif second_value > dealer_value:
            balance += currentBet * 2
            result.append("Player wins on the second hand")
        elif second_value < dealer_value:
            result.append("Dealer wins on the second hand")
        else:
            balance += currentBet
            result.append("Second hand pushes (tie)")

        return "; ".join(result), balance, "roundOver"

    else:
        # Single hand outcome
        if player_value > 21:
            return "Player Busts! Dealer Wins!", balance, "roundOver"
        elif dealer_value > 21:
            balance += currentBet * 2
            return "Dealer Busts! Player Wins!", balance, "roundOver"
        elif player_value == 21 and len(player_hand) == 2:
            balance += currentBet * 2.5
            return "Blackjack! Player Wins!", balance, "roundOver"
        elif player_value > dealer_value and playerBust:
            balance += currentBet * 2
            return "Player Wins!", balance, "roundOver"
        elif player_value < dealer_value:
            return "Dealer Wins!", balance, "roundOver"
        else:
            balance += currentBet
            return "It's a Tie!", balance, "roundOver"
