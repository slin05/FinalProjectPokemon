import asyncio
import random
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List

class StatusType(Enum):
    POISON = "poison"
    BURN = "burn"
    PARALYSIS = "paralysis"
    SLEEP = "sleep"
    FREEZE = "freeze"
    CONFUSION = "confusion"

@dataclass
class StatusEffect:
    effect_type: StatusType
    turns_remaining: int
    severity: int = 1
    message: str = ""

class AdvancedStatusManager:
    """Handles all Pokemon status conditions during battle."""
    
    def __init__(self):
        self.effect_messages = {
            StatusType.POISON: "💜 {name} is hurt by poison!",
            StatusType.BURN: "🔥 {name} is hurt by burn!",
            StatusType.PARALYSIS: "⚡ {name} is paralyzed!",
            StatusType.SLEEP: "😴 {name} is fast asleep!",
            StatusType.FREEZE: "🧊 {name} is frozen solid!",
            StatusType.CONFUSION: "😵 {name} is confused!",
        }
    
    async def apply_status_effects(self, pokemon) -> bool:
        if not hasattr(pokemon, 'status_effects'):
            pokemon.status_effects = []
        
        can_act = True
        effects_to_remove = []
        
        for effect in pokemon.status_effects:
            result = await self.process_single_effect(pokemon, effect)
            
            if result == "prevent_action":
                can_act = False
            
            effect.turns_remaining -= 1
            if effect.turns_remaining <= 0:
                effects_to_remove.append(effect)
        
        for effect in effects_to_remove:
            pokemon.status_effects.remove(effect)
            await self.show_recovery_message(pokemon, effect)
        
        return can_act
    
    async def process_single_effect(self, pokemon, effect: StatusEffect) -> str:
        if effect.effect_type == StatusType.POISON:
            damage = max(1, pokemon.max_hp // (16 - effect.severity))
            await self.animated_status_damage(pokemon, damage, "poison")
            return "continue"
        
        elif effect.effect_type == StatusType.BURN:
            damage = max(1, pokemon.max_hp // (16 - effect.severity))
            await self.animated_status_damage(pokemon, damage, "burn")
            return "continue"
        
        elif effect.effect_type == StatusType.PARALYSIS:
            print(f"⚡ {pokemon.name} is paralyzed!")
            if random.random() < 0.25:
                print(f"   {pokemon.name} can't move!")
                await asyncio.sleep(1)
                return "prevent_action"
            return "continue"
        
        elif effect.effect_type == StatusType.SLEEP:
            print(f"😴 {pokemon.name} is fast asleep!")
            await asyncio.sleep(0.8)
            return "prevent_action"
        
        elif effect.effect_type == StatusType.FREEZE:
            print(f"🧊 {pokemon.name} is frozen solid!")
            if random.random() < 0.2:
                pokemon.status_effects.remove(effect)
                print(f"🔥 {pokemon.name} thawed out!")
                await asyncio.sleep(0.5)
                return "continue"
            return "prevent_action"
        
        elif effect.effect_type == StatusType.CONFUSION:
            print(f"😵 {pokemon.name} is confused!")
            if random.random() < 0.33:
                damage = pokemon.attack // 2
                print(f"   {pokemon.name} hurt itself in its confusion!")
                await self.animated_status_damage(pokemon, damage, "confusion")
                return "prevent_action"
            return "continue"
        
        return "continue"
    
    async def animated_status_damage(self, pokemon, damage, effect_type):
        symbols = {
            "poison": "💜",
            "burn": "🔥", 
            "confusion": "😵"
        }
        
        symbol = symbols.get(effect_type, "💥")
        print(f"{symbol} {pokemon.name} takes {damage} damage from {effect_type}!")
        
        old_hp = pokemon.current_hp
        pokemon.current_hp = max(0, pokemon.current_hp - damage)
        
        await asyncio.sleep(0.5)
        print(f"❤️  {pokemon.name}: {pokemon.current_hp}/{pokemon.max_hp} HP")
        await asyncio.sleep(0.3)
    
    async def show_recovery_message(self, pokemon, effect):
        recovery_messages = {
            StatusType.POISON: f"✨ {pokemon.name} recovered from poison!",
            StatusType.BURN: f"✨ {pokemon.name} recovered from burn!",
            StatusType.PARALYSIS: f"⚡ {pokemon.name} is no longer paralyzed!",
            StatusType.SLEEP: f"😊 {pokemon.name} woke up!",
            StatusType.FREEZE: f"🔥 {pokemon.name} thawed out!",
            StatusType.CONFUSION: f"🧠 {pokemon.name} snapped out of confusion!",
        }
        
        message = recovery_messages.get(effect.effect_type, f"✨ {pokemon.name} recovered!")
        print(message)
        await asyncio.sleep(0.8)
    
    def add_status_effect(self, pokemon, effect_type: StatusType, turns: int, severity: int = 1):
        if not hasattr(pokemon, 'status_effects'):
            pokemon.status_effects = []
        
        for existing_effect in pokemon.status_effects:
            if existing_effect.effect_type == effect_type:
                existing_effect.turns_remaining = max(existing_effect.turns_remaining, turns)
                existing_effect.severity = max(existing_effect.severity, severity)
                return
        
        new_effect = StatusEffect(effect_type, turns, severity)
        pokemon.status_effects.append(new_effect)
        
        effect_names = {
            StatusType.POISON: "poisoned",
            StatusType.BURN: "burned", 
            StatusType.PARALYSIS: "paralyzed",
            StatusType.SLEEP: "put to sleep",
            StatusType.FREEZE: "frozen",
            StatusType.CONFUSION: "confused",
        }
        
        effect_name = effect_names.get(effect_type, "affected")
        print(f"🌟 {pokemon.name} was {effect_name}!")

async def test_status_system():
    from pokemon import Pokemon
    
    pikachu = Pokemon("Pikachu", "Electric", 100, 55, 40, 90)
    status_manager = AdvancedStatusManager()
    
    status_manager.add_status_effect(pikachu, StatusType.POISON, 3)
    status_manager.add_status_effect(pikachu, StatusType.PARALYSIS, 2)
    
    for turn in range(5):
        print(f"\n--- Turn {turn + 1} ---")
        can_act = await status_manager.apply_status_effects(pikachu)
        print(f"Can act: {can_act}")
        
        if pikachu.current_hp <= 0:
            print(f"{pikachu.name} fainted!")
            break

if __name__ == "__main__":
    print("🧪 Testing Advanced Status System")
    asyncio.run(test_status_system())