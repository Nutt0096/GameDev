import random

def roll_dice(sides: int) -> int:
    """Roll a dice with the given number of sides."""
    return random.randint(1, sides)

def apply_item_effect(item, target, team=None, enemies=None, coins=0):
    effect = item.get("on use", "")

    # Gros Michel Banana
    if effect == "1 in 12 chance to unlock Legendary banana (It not doing anything now)":
        if random.randint(1, 12) == 1:
            return f"{target['name']} unlocked Legendary banana!"
        else:
            return f"{target['name']} did not unlock Legendary banana."

    # Healing Potion
    elif effect == "Recover 1d8 HP":
        heal_amount = roll_dice(8)
        target["hp"] = min(target["hp"] + heal_amount, 100)
        return f"{target['name']} healed for {heal_amount} HP!"

    # Jimbo
    elif effect == "Next hit, add 4 damage":
        target["STR"] += 4
        return f"{target['name']} added 4 damage to the next hit!"

    # Chocolate Cornet
    elif effect == "Increase ACC by 1":
        target["ACC"] += 1
        return f"{target['name']} increased ACC by 1!"
    
    # Apple Juice
    elif effect == "Recover 2d8 HP":
        heal_amount = roll_dice(8) + roll_dice(8)
        target["hp"] = min(target["hp"] + heal_amount, 100)
        return f"{target['name']} healed for {heal_amount} HP!"

    # Coconut
    elif effect == "Recover 1d8 HP to all allies":
        if not team:
            return "No team provided for the healing effect!"

        heal_amount = roll_dice(8)
        for member in team:
            member["hp"] = min(member["hp"] + heal_amount, 100)
        return f"Entire team healed for {heal_amount} HP!"
    
    # Watermelon
    elif effect == "Recover 2d6 HP to all allies":
        if not team:
            return "No team provided for the healing effect!"

        heal_amount = roll_dice(6) + roll_dice(6)
        for member in team:
            member["hp"] = min(member["hp"] + heal_amount, 100)
        return f"Entire team healed for {heal_amount} HP!"

    # Ice Cream
    elif effect == "Recover 20 Mana":
        target["mp"] = target["mp"] + 20
        return f"{target['name']} restored 20 Mana!"
    
    # A Broken Toaster
    elif effect == "Deal 1d12 damage to a random enemy":
        if not target:
            return "No target enemy provided for the effect!"
        
        damage = roll_dice(12)
        target["hp"] = target["hp"] - damage
        return f"{target['name']} weakened for {damage} HP!"
    
    # Hamburger
    elif effect == "Fully recover HP":
        target["hp"] = 100
        return f"{target['name']} fully recovered HP!"
    
    # Cupcake
    elif effect == "Recover 50 Mana":
        target["mp"] = target["mp"] + 50
        return f"{target['name']} restored 50 Mana!"
    
    # Midas Bomb
    elif effect == "Deals 3d6 damage to an enemy. If it died, gain 2d4*10 coins":
        damage = roll_dice(6) + roll_dice(6) + roll_dice(6)
        target["hp"] = target["hp"] - damage
        if target["hp"] <= 0:
            coins += (roll_dice(4) + roll_dice(4)) * 10
            return f"{target['name']} died! You gain {coins} coins!"

    # Emerald Splash
    elif effect == "Deals 4d12 damage to enemies. Has 1 in 6 chance to deal on yourself":
        damage = roll_dice(12) + roll_dice(12) + roll_dice(12) + roll_dice(12)
        if random.randint(1, 6) == 1:
            target["hp"] = target["hp"] - damage
            return f"{target['name']} damaged themselves for {damage} HP!"
        else:
            if not enemies:
                return "No enemies provided for the effect!"

            for enemy in enemies:
                enemy["hp"] = enemy["hp"] - damage
            return f"{target['name']} damaged enemies for {damage} HP!"

    # John's Bible
    elif effect == "Next incoming hit deals 0 damage":
        return f"{target['name']} is immune to the next hit! (not really)"

    # Endless Eight
    elif effect == "Deals 8d8 damage to an enemy. Has 1 in 8 chance to deal additional 8d8.":
        damage = roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8)
        if random.randint(1, 8) == 1:
            damage += roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8) + roll_dice(8)
            target["hp"] = target["hp"] - damage
            return f"{target['name']} damaged for {damage} HP! with 1 in 8 chance"
        else:
            target["hp"] = target["hp"] - damage
            return f"{target['name']} damaged for {damage} HP!"
        
    # Pizza
    elif effect == "Fully recover HP to all allies":
        if not team:
            return "No team provided for the healing effect!"

        heal_amount = 100
        for member in team:
            member["hp"] = min(member["hp"] + heal_amount, 100)
        return f"Entire team healed for {heal_amount} HP!"

    else:
        return f"The item '{item['name']}' has no effect!"
