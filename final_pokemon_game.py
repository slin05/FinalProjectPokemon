import asyncio
import random
from typing import List, Optional

from pokemon import Pokemon
from async_ui import AsyncUI, InteractiveBattleSystem
from status_effects import AdvancedStatusManager, StatusType, StatusEffect
from special_moves import SpecialMoveSystem
from enhanced_battle import EnhancedBattleSystem

class CompletePokemonGame:
    """Main Pokemon battle game with all systems integrated."""
    
    def __init__(self):
        self.ui = AsyncUI()
        self.status_manager = AdvancedStatusManager()
        self.special_moves = SpecialMoveSystem()
        self.battle_system = InteractiveBattleSystem()
        self.player_team = []
        self.current_opponent = None
    
    async def start_game(self):
        await self.ui.type_message("🎮 Welcome to Pokemon Battle Arena! 🎮", 0.05)
        await asyncio.sleep(1)
        
        await self.setup_player_team()
        
        await self.main_game_loop()
    
    async def setup_player_team(self):
        await self.ui.type_message("🏆 Choose your starter Pokemon!", 0.05)
        
        starters = [
            Pokemon("Pikachu", "Electric", 100, 55, 50, 90),
            Pokemon("Charmander", "Fire", 95, 52, 48, 65),
            Pokemon("Squirtle", "Water", 98, 48, 55, 43),
        ]
        
        print("\n" + "="*50)
        for i, pokemon in enumerate(starters, 1):
            print(f"{i}. {pokemon.name} ({pokemon.pokemon_type} type)")
            print(f"   HP: {pokemon.max_hp}, Attack: {pokemon.attack}, Defense: {pokemon.defense}")
        print("="*50)
        
        while True:
            choice = await self.ui.get_user_input("Choose your starter (1-3): ")
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= 3:
                    chosen_starter = starters[choice_num - 1]
                    self.player_team.append(chosen_starter)
                    await self.ui.type_message(f"🎉 You chose {chosen_starter.name}!")
                    break
                else:
                    print("❌ Please choose 1, 2, or 3!")
            except ValueError:
                print("❌ Please enter a number!")
        
        await asyncio.sleep(1.5)
    
    async def main_game_loop(self):
        while True:
            await self.show_main_menu()
            
            choice = await self.ui.get_user_input("Choose an option (1-4): ")
            
            if choice == "1":
                await self.wild_pokemon_battle()
            elif choice == "2":
                await self.trainer_battle()
            elif choice == "3":
                await self.show_team_status()
            elif choice == "4":
                await self.ui.type_message("👋 Thanks for playing! Goodbye!")
                break
            else:
                await self.ui.display_message("❌ Invalid choice! Please try again.")
    
    async def show_main_menu(self):
        self.ui.clear_screen()
        print("\n" + "="*50)
        print("🎮 POKEMON BATTLE ARENA")
        print("="*50)
        print("1. 🌿 Battle Wild Pokemon")
        print("2. 👨‍🎓 Battle Trainer")
        print("3. 📋 Check Team Status")
        print("4. 🚪 Exit Game")
        print("="*50)
    
    async def wild_pokemon_battle(self):
        wild_pokemon_list = [
            ("Rattata", "Normal", 80, 45, 35, 72),
            ("Pidgy", "Flying", 85, 50, 40, 56),
            ("Caterpie", "Bug", 75, 30, 35, 45),
            ("Geodude", "Rock", 90, 60, 70, 20),
        ]
        
        wild_data = random.choice(wild_pokemon_list)
        wild_pokemon = Pokemon(*wild_data)
        
        await self.ui.type_message(f"🌿 A wild {wild_pokemon.name} appeared!")
        
        player_pokemon = self.player_team[0]
        await self.enhanced_battle(player_pokemon, wild_pokemon)
    
    async def trainer_battle(self):
        trainer_teams = [
            [("Machop", "Fighting", 90, 60, 50, 35), ("Geodude", "Rock", 90, 60, 70, 20)],
            [("Magikarp", "Water", 60, 10, 55, 80), ("Gyarados", "Water", 150, 90, 79, 81)],
            [("Pichu", "Electric", 60, 40, 15, 60), ("Raichu", "Electric", 110, 85, 50, 110)],
        ]
        
        enemy_team_data = random.choice(trainer_teams)
        enemy_team = [Pokemon(*data) for data in enemy_team_data]
        
        await self.ui.type_message("👨‍🎓 Trainer challenges you to battle!")
        await self.ui.type_message(f"Trainer sends out {enemy_team[0].name}!")
        
        await self.multi_pokemon_battle(self.player_team, enemy_team)
    
    async def enhanced_battle(self, player_pokemon, opponent):
        battle_active = True
        turn = 1
        
        while (battle_active and 
               player_pokemon.current_hp > 0 and 
               opponent.current_hp > 0):
            
            await self.ui.display_battle_status(player_pokemon, opponent)
            
            print(f"\n🔄 Turn {turn}")
            
            player_can_act = await self.status_manager.apply_status_effects(player_pokemon)
            opponent_can_act = await self.status_manager.apply_status_effects(opponent)
            
            if player_pokemon.current_hp <= 0 or opponent.current_hp <= 0:
                break
            
            if player_pokemon.speed >= opponent.speed:
                if player_can_act:
                    await self.player_enhanced_turn(player_pokemon, opponent)
                if opponent.current_hp > 0 and opponent_can_act:
                    await self.ai_enhanced_turn(opponent, player_pokemon)
            else:
                if opponent_can_act:
                    await self.ai_enhanced_turn(opponent, player_pokemon)
                if player_pokemon.current_hp > 0 and player_can_act:
                    await self.player_enhanced_turn(player_pokemon, opponent)
            
            turn += 1
            await asyncio.sleep(1)
        
        if player_pokemon.current_hp > 0:
            await self.ui.type_message(f"🎉 {player_pokemon.name} won!")
        else:
            await self.ui.type_message(f"💀 {player_pokemon.name} fainted!")
    
    async def player_enhanced_turn(self, player_pokemon, opponent):
        action = await self.ui.display_battle_menu(player_pokemon, opponent)
        
        if action == "1":
            move_choice, _ = await self.ui.display_move_menu(player_pokemon)
            
            if move_choice != "back":
                if move_choice in self.special_moves.moves_database:
                    await self.special_moves.use_special_move(player_pokemon, opponent, move_choice)
                else:
                    await self.execute_regular_move(player_pokemon, opponent, move_choice)
        elif action == "4":
            await self.ui.type_message("🏃 You ran away from the battle!")
            return False
        return True
    
    async def ai_enhanced_turn(self, ai_pokemon, target):
        await self.ui.display_message(f"🤖 {ai_pokemon.name} is deciding...")
        await asyncio.sleep(1)
        
        moves = ai_pokemon.moves
        
        if ai_pokemon.current_hp > ai_pokemon.max_hp * 0.5:
            special_moves = [move for move in moves if move in self.special_moves.moves_database]
            if special_moves and random.random() < 0.3:
                chosen_move = random.choice(special_moves)
                await self.special_moves.use_special_move(ai_pokemon, target, chosen_move)
                return
        
        chosen_move = random.choice(moves)
        await self.execute_regular_move(ai_pokemon, target, chosen_move)
    
    async def execute_regular_move(self, attacker, defender, move_name):
        await self.ui.type_message(f"⚡ {attacker.name} uses {move_name}!")
        
        base_damage = attacker.attack
        damage = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        
        defender.current_hp = max(0, defender.current_hp - damage)
        
        await self.ui.type_message(f"💥 {defender.name} takes {damage} damage!")
        
        await self.apply_move_side_effects(move_name, attacker, defender)
    
    async def apply_move_side_effects(self, move_name, attacker, defender):
        effect_chances = {
            "Thunder Shock": ("paralysis", 0.1),
            "Ember": ("burn", 0.1),
            "Water Gun": ("none", 0),
            "Thunder Wave": ("paralysis", 0.9),
        }
        
        if move_name in effect_chances:
            effect, chance = effect_chances[move_name]
            if effect != "none" and random.random() < chance:
                self.status_manager.add_status_effect(
                    defender, 
                    getattr(StatusType, effect.upper()), 
                    3
                )
    
    async def show_team_status(self):
        print("\n" + "="*50)
        print("👥 YOUR TEAM STATUS")
        print("="*50)
        
        for i, pokemon in enumerate(self.player_team, 1):
            await self.ui.display_pokemon_info(pokemon)
            if i < len(self.player_team):
                print("─" * 30)
        
        await self.ui.get_user_input("\nPress Enter to continue...")
    
    async def multi_pokemon_battle(self, team1, team2):
        await self.enhanced_battle(team1[0], team2[0])

async def main():
    game = CompletePokemonGame()
    try:
        await game.start_game()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please report this issue!")

if __name__ == "__main__":
    asyncio.run(main())
    