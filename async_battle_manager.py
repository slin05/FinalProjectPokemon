import asyncio
from typing import Optional, Dict, Any

class AsyncBattleManager:
    """Battle system for Pokemon trainer battles."""
    
    def __init__(self):
        self.battle_active = False
        self.current_animations = []
        self.status_effects = {}
    
    async def start_battle(self, pokemon1, pokemon2):
        print(f"🔥 Battle starting: {pokemon1.name} vs {pokemon2.name}!")
        self.battle_active = True
        
        await self.battle_intro_animation()
        
        return await self.battle_loop(pokemon1, pokemon2)
    
    async def battle_intro_animation(self):
        messages = [
            "Trainers prepare for battle!",
            "Let the battle begin!"
        ]
        
        for message in messages:
            print(f"📢 {message}")
            await asyncio.sleep(1.2)
    
    async def execute_move(self, attacker, defender, move_name):
        print(f"\n⚡ {attacker.name} uses {move_name}!")
        
        await asyncio.sleep(0.8)
        
        damage = self.calculate_move_damage(attacker, move_name)
        
        await self.damage_animation(defender, damage)
        
        return damage
    
    async def damage_animation(self, pokemon, damage):
        print(f"💥 {pokemon.name} takes {damage} damage!")
        await asyncio.sleep(0.6)
        
        pokemon.current_hp = max(0, pokemon.current_hp - damage)
        
        print(f"❤️  {pokemon.name}: {pokemon.current_hp}/{pokemon.max_hp} HP")
        await asyncio.sleep(0.4)
    
    async def battle_loop(self, pokemon1, pokemon2):
        turn = 1
        
        while self.battle_active and pokemon1.current_hp > 0 and pokemon2.current_hp > 0:
            print(f"\n🔄 Turn {turn}")
            await asyncio.sleep(0.5)
            
            if pokemon1.current_hp > 0:
                await self.pokemon_turn(pokemon1, pokemon2)
                if pokemon2.current_hp <= 0:
                    break
            
            if pokemon2.current_hp > 0:
                await self.pokemon_turn(pokemon2, pokemon1)
                if pokemon1.current_hp <= 0:
                    break
            
            turn += 1
            await asyncio.sleep(1)
        
        winner = pokemon1 if pokemon1.current_hp > 0 else pokemon2
        await self.battle_end_animation(winner)
        return winner
    
    async def pokemon_turn(self, attacker, defender):
        move = "Tackle"
        await self.execute_move(attacker, defender, move)
    
    async def battle_end_animation(self, winner):
        print(f"\n🎉 {winner.name} wins the battle!")
        await asyncio.sleep(1)
        print("Battle concluded!")
    
    def calculate_move_damage(self, pokemon, move_name):
        base_damage = getattr(pokemon, 'attack', 50)
        return max(10, base_damage // 2)

async def test_async_battle():
    class MockPokemon:
        def __init__(self, name, hp=100, attack=50):
            self.name = name
            self.current_hp = hp
            self.max_hp = hp
            self.attack = attack
    
    pikachu = MockPokemon("Pikachu", 100, 55)
    charmander = MockPokemon("Charmander", 95, 52)
    
    battle_manager = AsyncBattleManager()
    winner = await battle_manager.start_battle(pikachu, charmander)
    
    print(f"Final winner: {winner.name}")

if __name__ == "__main__":
    print("🧪 Testing Async Battle Manager")
    asyncio.run(test_async_battle())