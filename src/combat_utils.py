import random

def roll_dice(sides: int) -> int:
    """Roll a dice with the given number of sides."""
    return random.randint(1, sides)

def resolve_attack(attacker, target, weapon):
    """Calculate if the attack hits and apply damage."""
    hit_accuracy = roll_dice(20) + attacker["ACC"] + weapon["ACC"]
    
    if hit_accuracy >= target["DEF"]:
        damage = roll_dice(weapon["damage_dice"]) + attacker["STR"]
        target["hp"] -= damage
        return f"Hit! {attacker['name']} deals {damage} damage to {target['name']}."
    else:
        return f"Miss! {attacker['name']}'s total accuracy ({hit_accuracy}) < {target['DEF']}."
    
def resolve_spell(caster, target, spell, monsters, selected_monster_index):
    """Resolve a spell action. Handles both healing and damaging spells, as well as spell resistance."""
    if caster["mp"] < spell["mana_cost"]:
        return f"{caster['name']} does not have enough mana to cast {spell['name']}!"

    # Deduct mana
    caster["mp"] -= spell["mana_cost"]

    if spell.get("effect") == "heal":
        # Healing logic
        heal_amount = roll_dice(spell["damage_dice"]) + caster["INT"]
        caster["hp"] = min(100, caster["hp"] + heal_amount)
        return f"{caster['name']} casts {spell['name']} and heals {heal_amount} HP!"
    else:
        hit_accuracy = roll_dice(20) + caster["ACC"] + spell["ACC"]

        if hit_accuracy > target["CHA"]:
            damage = roll_dice(spell["damage_dice"]) + caster["INT"]
            target["hp"] -= damage
            return f"Hit! {caster['name']} deals {damage} damage to {target['name']}."
        else:
            return f"Miss! {caster['name']}'s total accuracy ({hit_accuracy}) < {target['DEF']}."

def resolve_attack_monster(monster, target):
    hit_accuracy = roll_dice(20) + monster["ACC"]
    if hit_accuracy >= target["DEF"]:
        damage = roll_dice(10) + monster["STR"]
        target["hp"] -= damage
        return f"{monster['name']} attacks {target['name']} and deals {damage} damage!"
    else:
        return f"Miss! {monster['name']}'s total accuracy ({hit_accuracy}) < {target['DEF']}."
