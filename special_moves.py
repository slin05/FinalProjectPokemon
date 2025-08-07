import asyncio
import random
from typing import Dict, Callable, Any

class SpecialMove:
    def __init__(self, name: str, power: int, move_type: str, effect_function: Callable):
        self.name = name
        self.power = power
        self.move_type = move_type
        self.effect_function = effect_function
        self.pp = 5
        self.accuracy = 100

class SpecialMoveSystem:
    """Handles powerful special moves and their cinematic effects."""
    
    def __init__(self):
        self.moves_database = self.create_moves_database()
    
    def create_moves_database(self) -> Dict[str, SpecialMove]:
        return {
            "Thunder": SpecialMove("Thunder", 110, "Electric", self.thunder_effect),
            "Blizzard": SpecialMove("Blizzard", 110, "Ice", self.blizzard_effect),
            "Fire Blast": SpecialMove("Fire Blast", 110, "Fire", self.fire_blast_effect),
            "Psychic": SpecialMove("Psychic", 90, "Psychic", self.psychic_effect),
            "Earthquake": SpecialMove("Earthquake", 100, "Ground", self.earthquake_effect),
            "Hyper Beam": SpecialMove("Hyper Beam", 150, "Normal", self.hyper_beam_effect),
        }
    
    async def use_special_move(self, attacker, defender, move_name: str) -> bool:
        if move_name not in self.moves_database:
            return False
        
        move = self.moves_database[move_name]
        
        if move.pp <= 0:
            print(f"❌ {move_name} has no PP left!")
            return False
        
        if random.randint(1, 100) > move.accuracy:
            print(f"💨 {attacker.name}'s {move_name} missed!")
            await asyncio.sleep(1)
            return True
        
        await self.move_cinematic(move_name)
        
        damage = self.calculate_special_damage(attacker, move)
        defender.current_hp = max(0, defender.current_hp - damage)
        
        print(f"💥 {defender.name} takes {damage} damage!")
        await asyncio.sleep(0.8)
        
        await move.effect_function(attacker, defender)
        
        move.pp -= 1
        
        return True
    
    async def move_cinematic(self, move_name: str):
        cinematics = {
            "Thunder": ["⚡⚡⚡", "🌩️ THUNDER! 🌩️", "⚡⚡⚡"],
            "Blizzard": ["❄️❄️❄️", "🌨️ BLIZZARD! 🌨️", "❄️❄️❄️"],
            "Fire Blast": ["🔥🔥🔥", "💥 FIRE BLAST! 💥", "🔥🔥🔥"],
            "Psychic": ["🔮🔮🔮", "🧠 PSYCHIC! 🧠", "🔮🔮🔮"],
            "Earthquake": ["🌍🌍🌍", "⛰️ EARTHQUAKE! ⛰️", "🌍🌍🌍"],
            "Hyper Beam": ["✨✨✨", "💫 HYPER BEAM! 💫", "✨✨✨"],
        }
        
        frames = cinematics.get(move_name, ["💥", f"{move_name}!", "💥"])
        
        for frame in frames:
            print(frame)
            await asyncio.sleep(0.6)
    
    def calculate_special_damage(self, attacker, move: SpecialMove) -> int:
        base_attack = getattr(attacker, 'special_attack', getattr(attacker, 'attack', 50))
        
        damage = (move.power * base_attack) // 50
        
        damage = random.randint(int(damage * 0.85), int(damage * 1.15))
        
        return max(1, damage)
    
    async def thunder_effect(self, attacker, defender):
        if random.random() < 0.3:
            print("⚡ Static electricity fills the air!")
            from status_effects import StatusType, StatusEffect
            effect = StatusEffect(StatusType.PARALYSIS, 3)
            defender.status_effects.append(effect)
            print(f"🌟 {defender.name} was paralyzed!")
            await asyncio.sleep(0.5)
    
    async def blizzard_effect(self, attacker, defender):
        if random.random() < 0.1:
            print("🧊 The cold is overwhelming!")
            from status_effects import StatusType, StatusEffect
            effect = StatusEffect(StatusType.FREEZE, 2)
            defender.status_effects.append(effect)
            print(f"🌟 {defender.name} was frozen!")
            await asyncio.sleep(0.5)
    
    async def fire_blast_effect(self, attacker, defender):
        if random.random() < 0.3:
            print("🔥 Intense flames linger!")
            from status_effects import StatusType, StatusEffect
            effect = StatusEffect(StatusType.BURN, 3)
            defender.status_effects.append(effect)
            print(f"🌟 {defender.name} was burned!")
            await asyncio.sleep(0.5)
    
    async def psychic_effect(self, attacker, defender):
        if random.random() < 0.1:
            print("🌀 Mind-bending energy swirls around!")
            from status_effects import StatusType, StatusEffect
            effect = StatusEffect(StatusType.CONFUSION, 2)
            defender.status_effects.append(effect)
            print(f"🌟 {defender.name} was confused!")
            await asyncio.sleep(0.5)
    
    async def earthquake_effect(self, attacker, defender):
        print("🌍 The ground shakes violently!")
        await asyncio.sleep(0.8)
    
    async def hyper_beam_effect(self, attacker, defender):
        print("💫 Incredible power was unleashed!")
        print(f"⚡ {attacker.name} must recharge!")
        from status_effects import StatusType, StatusEffect
        effect = StatusEffect(StatusType.SLEEP, 1)
        attacker.status_effects.append(effect)
        await asyncio.sleep(1)

async def test_special_moves():
    from pokemon import Pokemon
    
    charizard = Pokemon("Charizard", "Fire", 150, 80, 60, 100)
    blastoise = Pokemon("Blastoise", "Water", 150, 75, 100, 78)
    
    move_system = SpecialMoveSystem()
    
    print("🔥 Charizard uses Fire Blast!")
    await move_system.use_special_move(charizard, blastoise, "Fire Blast")
    
    print(f"\n❤️ Blastoise HP: {blastoise.current_hp}/{blastoise.max_hp}")

if __name__ == "__main__":
    print("🧪 Testing Special Move System")
    asyncio.run(test_special_moves())
    