import asyncio
import random
from typing import List, Optional
from pokemon import Pokemon

class EnhancedBattleSystem:
    """Advanced battle mechanics with trainer teams."""
    
    def __init__(self):
        self.battle_log = []
        self.special_effects_active = True
    
    async def trainer_battle(self, trainer1_team: List[Pokemon], trainer2_team: List[Pokemon]):
        print("🏆 TRAINER BATTLE BEGINS! 🏆")
        await asyncio.sleep(1.5)
        
        trainer1_active = 0
        trainer2_active = 0
        
        while (trainer1_active < len(trainer1_team) and 
               trainer2_active < len(trainer2_team)):
            
            pokemon1 = trainer1_team[trainer1_active]
            pokemon2 = trainer2_team[trainer2_active]
            
            print(f"\n⚔️  {pokemon1.name} vs {pokemon2.name}!")
            winner = await self.single_pokemon_battle(pokemon1, pokemon2)
            
            if winner == pokemon1:
                trainer2_active += 1
                if trainer2_active < len(trainer2_team):
                    next_pokemon = trainer2_team[trainer2_active]
                    print(f"🔄 Trainer 2 sends out {next_pokemon.name}!")
                    await asyncio.sleep(1)
            else:
                trainer1_active += 1
                if trainer1_active < len(trainer1_team):
                    next_pokemon = trainer1_team[trainer1_active]
                    print(f"🔄 Trainer 1 sends out {next_pokemon.name}!")
                    await asyncio.sleep(1)
        
        if trainer1_active < len(trainer1_team):
            print("🎉 Trainer 1 wins the battle!")
        else:
            print("🎉 Trainer 2 wins the battle!")
    
    async def single_pokemon_battle(self, pokemon1, pokemon2):
        turn = 1
        
        while pokemon1.current_hp > 0 and pokemon2.current_hp > 0:
            print(f"\n--- Turn {turn} ---")
            
            if pokemon1.speed >= pokemon2.speed:
                first, second = pokemon1, pokemon2
            else:
                first, second = pokemon2, pokemon1
            
            if first.current_hp > 0:
                await self.execute_turn(first, second)
                if second.current_hp <= 0:
                    break
            
            if second.current_hp > 0:
                await self.execute_turn(second, first)
            
            await first.status_effect_tick()
            await second.status_effect_tick()
            
            turn += 1
            await asyncio.sleep(0.8)
        
        winner = pokemon1 if pokemon1.current_hp > 0 else pokemon2
        print(f"🏆 {winner.name} wins!")
        return winner
    
    async def execute_turn(self, attacker, defender):
        available_moves = getattr(attacker, 'moves', ['Tackle', 'Scratch'])
        chosen_move = random.choice(available_moves)
        
        is_paralyzed = any(effect.effect_type.value == 'paralysis' 
                          for effect in getattr(attacker, 'status_effects', []))
        
        if is_paralyzed and random.random() < 0.25:
            print(f"⚡ {attacker.name} is paralyzed and can't move!")
            await asyncio.sleep(1)
            return
        
        await self.use_move_with_effects(attacker, defender, chosen_move)
    
    async def use_move_with_effects(self, attacker, defender, move_name):
        print(f"🎯 {attacker.name} uses {move_name}!")
        
        for i in range(3):
            print("⚡" * (i + 1))
            await asyncio.sleep(0.2)
        
        base_damage = getattr(attacker, 'attack', 50)
        damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        
        if random.random() < 0.0625:
            damage = int(damage * 1.5)
            print("💥 Critical hit!")
            await asyncio.sleep(0.5)
        
        await self.animated_damage(defender, damage)
        
        await self.apply_move_effects(move_name, attacker, defender)
    
    async def animated_damage(self, target, damage):
        print(f"💢 {target.name} takes {damage} damage!")
        
        old_hp = target.current_hp
        target.current_hp = max(0, target.current_hp - damage)
        
        steps = 5
        hp_diff = old_hp - target.current_hp
        for i in range(steps):
            current_display = old_hp - (hp_diff * (i + 1) // steps)
            print(f"❤️  HP: {current_display}/{target.max_hp}", end='\r')
            await asyncio.sleep(0.1)
        
        print(f"❤️  {target.name}: {target.current_hp}/{target.max_hp} HP")
        await asyncio.sleep(0.5)
    
    async def apply_move_effects(self, move_name, attacker, defender):
        move_effects = {
            'Poison Sting': 'poison',
            'Ember': 'burn',
            'Thunder Wave': 'paralysis',
            'Sleep Powder': 'sleep',
        }
        
        if move_name in move_effects and random.random() < 0.3:
            from status_effects import StatusType, StatusEffect
            effect_type = getattr(StatusType, move_effects[move_name].upper())
            effect = StatusEffect(effect_type, 3)
            defender.status_effects.append(effect)
            print(f"🌟 {defender.name} was {move_effects[move_name]}ed!")
            await asyncio.sleep(0.5)

async def test_enhanced_battle():
    pikachu = Pokemon("Pikachu", "Electric", 100, 55, 40, 90)
    charmander = Pokemon("Charmander", "Fire", 95, 52, 43, 65)
    
    battle_system = EnhancedBattleSystem()
    await battle_system.single_pokemon_battle(pikachu, charmander)

if __name__ == "__main__":
    print("🧪 Testing Enhanced Battle System")
    asyncio.run(test_enhanced_battle())