import asyncio
import sys
from typing import List, Optional, Tuple

class AsyncUI:
    """Interactive battle interface for Pokemon games."""
    
    def __init__(self):
        self.input_queue = asyncio.Queue()
        self.display_lock = asyncio.Lock()
    
    async def display_battle_menu(self, pokemon, opponent) -> str:
        async with self.display_lock:
            self.clear_screen()
            await self.display_battle_status(pokemon, opponent)
            
            print("\n" + "="*50)
            print("🎮 What will you do?")
            print("="*50)
            print("1. 👊 Attack")
            print("2. 🎒 Items") 
            print("3. 🔄 Switch Pokemon")
            print("4. 🏃 Run Away")
            print("="*50)
        
        choice = await self.get_user_input("Choose an action (1-4): ")
        return choice
    
    async def display_move_menu(self, pokemon) -> Tuple[str, int]:
        async with self.display_lock:
            print("\n" + "="*40)
            print(f"🎯 {pokemon.name}'s Moves:")
            print("="*40)
            
            moves = getattr(pokemon, 'moves', ['Tackle', 'Scratch', 'Growl', 'Quick Attack'])
            
            for i, move in enumerate(moves, 1):
                pp_info = ""
                if hasattr(pokemon, 'move_pp') and move in pokemon.move_pp:
                    pp_info = f" (PP: {pokemon.move_pp[move]})"
                print(f"{i}. {move}{pp_info}")
            
            print("0. ← Back to main menu")
            print("="*40)
        
        while True:
            choice = await self.get_user_input("Choose a move (0-4): ")
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return "back", 0
                elif 1 <= choice_num <= len(moves):
                    return moves[choice_num - 1], choice_num - 1
                else:
                    print("❌ Invalid choice! Please try again.")
            except ValueError:
                print("❌ Please enter a number!")
    
    async def display_battle_status(self, pokemon, opponent):
        opponent_hp_percent = opponent.current_hp / opponent.max_hp
        opponent_bar = self.create_health_bar(opponent_hp_percent)
        
        print(f"\n🔴 {opponent.name}")
        print(f"❤️  HP: {opponent_bar} {opponent.current_hp}/{opponent.max_hp}")
        
        if hasattr(opponent, 'status_effects') and opponent.status_effects:
            if isinstance(opponent.status_effects, list):
                effects = [effect.effect_type.value for effect in opponent.status_effects]
            else:
                effects = list(opponent.status_effects.keys())
            print(f"🌟 Status: {', '.join(effects)}")
        
        print("\n" + "─"*50)
        
        player_hp_percent = pokemon.current_hp / pokemon.max_hp
        player_bar = self.create_health_bar(player_hp_percent)
        
        print(f"🔵 {pokemon.name}")
        print(f"❤️  HP: {player_bar} {pokemon.current_hp}/{pokemon.max_hp}")
        
        if hasattr(pokemon, 'status_effects') and pokemon.status_effects:
            if isinstance(pokemon.status_effects, list):
                effects = [effect.effect_type.value for effect in pokemon.status_effects]
            else:
                effects = list(pokemon.status_effects.keys())
            print(f"🌟 Status: {', '.join(effects)}")
    
    def create_health_bar(self, hp_percent: float, length: int = 20) -> str:
        filled = int(hp_percent * length)
        empty = length - filled
        
        if hp_percent > 0.5:
            bar_char = "🟢"
        elif hp_percent > 0.25:
            bar_char = "🟡"
        else:
            bar_char = "🔴"
        
        return bar_char * filled + "⬜" * empty
    
    async def get_user_input(self, prompt: str) -> str:
        print(prompt, end="", flush=True)
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input)
    
    def clear_screen(self):
        print("\033[2J\033[H", end="")
    
    async def display_message(self, message: str, delay: float = 1.0):
        async with self.display_lock:
            print(message)
            if delay > 0:
                await asyncio.sleep(delay)
    
    async def type_message(self, message: str, delay: float = 0.03):
        async with self.display_lock:
            for char in message:
                print(char, end="", flush=True)
                await asyncio.sleep(delay)
            print()
    
    async def display_pokemon_info(self, pokemon):
        async with self.display_lock:
            print(f"\n📋 {pokemon.name} Info:")
            print("─" * 30)
            print(f"❤️  HP: {pokemon.current_hp}/{pokemon.max_hp}")
            print(f"⚔️  Attack: {getattr(pokemon, 'attack', 'Unknown')}")
            print(f"🛡️  Defense: {getattr(pokemon, 'defense', 'Unknown')}")
            print(f"⚡ Speed: {getattr(pokemon, 'speed', 'Unknown')}")
            
            if hasattr(pokemon, 'pokemon_type'):
                print(f"🏷️  Type: {pokemon.pokemon_type}")
            
            if hasattr(pokemon, 'status_effects') and pokemon.status_effects:
                if isinstance(pokemon.status_effects, list):
                    effects = [effect.effect_type.value for effect in pokemon.status_effects]
                else:
                    effects = list(pokemon.status_effects.keys())
                print(f"🌟 Status Effects: {', '.join(effects)}")

class InteractiveBattleSystem:
    """Real-time battle system with player interaction."""
    
    def __init__(self):
        self.ui = AsyncUI()
        self.battle_active = False
    
    async def start_interactive_battle(self, player_pokemon, opponent_pokemon):
        self.battle_active = True
        
        await self.ui.type_message("🔥 A wild Pokemon appears!", 0.05)
        await asyncio.sleep(1)
        
        await self.ui.type_message(f"Go, {player_pokemon.name}!", 0.05)
        await asyncio.sleep(1.5)
        
        while (self.battle_active and 
               player_pokemon.current_hp > 0 and 
               opponent_pokemon.current_hp > 0):
            
            action_taken = await self.player_turn(player_pokemon, opponent_pokemon)
            
            if not action_taken or not self.battle_active:
                break
            
            if opponent_pokemon.current_hp <= 0:
                await self.ui.type_message(f"💀 {opponent_pokemon.name} fainted!")
                await self.ui.type_message(f"🎉 {player_pokemon.name} won the battle!")
                break
            
            await self.opponent_turn(opponent_pokemon, player_pokemon)
            
            if player_pokemon.current_hp <= 0:
                await self.ui.type_message(f"💀 {player_pokemon.name} fainted!")
                await self.ui.type_message("💀 You lost the battle!")
                break
        
        self.battle_active = False
    
    async def player_turn(self, player_pokemon, opponent) -> bool:
        while True:
            action = await self.ui.display_battle_menu(player_pokemon, opponent)
            
            if action == "1":
                move_choice, move_index = await self.ui.display_move_menu(player_pokemon)
                
                if move_choice == "back":
                    continue
                
                await self.execute_player_attack(player_pokemon, opponent, move_choice)
                return True
            
            elif action == "2":
                await self.ui.display_message("🎒 No items available in this demo!")
                await asyncio.sleep(1)
                continue
            
            elif action == "3":
                await self.ui.display_message("🔄 No other Pokemon available!")
                await asyncio.sleep(1)
                continue
            
            elif action == "4":
                await self.ui.type_message("🏃 You ran away from the battle!")
                self.battle_active = False
                return False
            
            else:
                await self.ui.display_message("❌ Invalid choice! Please try again.")
                await asyncio.sleep(1)
    
    async def execute_player_attack(self, attacker, defender, move_name):
        await self.ui.type_message(f"⚡ {attacker.name} uses {move_name}!")
        await asyncio.sleep(1)
        
        base_damage = getattr(attacker, 'attack', 50)
        damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        
        defender.current_hp = max(0, defender.current_hp - damage)
        
        await self.ui.type_message(f"💥 {defender.name} takes {damage} damage!")
        await asyncio.sleep(1)
    
    async def opponent_turn(self, opponent, player_pokemon):
        await self.ui.type_message(f"🤖 {opponent.name} is thinking...")
        await asyncio.sleep(1.5)
        
        moves = getattr(opponent, 'moves', ['Tackle', 'Scratch'])
        chosen_move = random.choice(moves)
        
        await self.ui.type_message(f"⚡ {opponent.name} uses {chosen_move}!")
        await asyncio.sleep(1)
        
        base_damage = getattr(opponent, 'attack', 45)
        damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        
        player_pokemon.current_hp = max(0, player_pokemon.current_hp - damage)
        
        await self.ui.type_message(f"💢 {player_pokemon.name} takes {damage} damage!")
        await asyncio.sleep(1)

async def test_interactive_battle():
    from pokemon import Pokemon
    
    pikachu = Pokemon("Pikachu", "Electric", 100, 55, 40, 90)
    wild_pokemon = Pokemon("Wild Rattata", "Normal", 80, 45, 35, 72)
    
    battle_system = InteractiveBattleSystem()
    await battle_system.start_interactive_battle(pikachu, wild_pokemon)

if __name__ == "__main__":
    import random
    print("🧪 Testing Interactive Battle System")
    asyncio.run(test_interactive_battle())