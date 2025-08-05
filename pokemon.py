import asyncio

class Pokemon:
    """Pokemon class with async battle capabilities."""
    
    def __init__(self, name, pokemon_type, hp, attack, defense, speed):
        self.name = name
        self.pokemon_type = pokemon_type
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.status_effects = {}
        self.moves = self.get_type_moves(pokemon_type)
    
    def get_type_moves(self, ptype):
        type_moves = {
            "Electric": ["Thunder Shock", "Quick Attack", "Thunder Wave", "Spark"],
            "Fire": ["Ember", "Scratch", "Fire Blast", "Flame Wheel"],
            "Water": ["Water Gun", "Tackle", "Bubble Beam", "Surf"],
            "Grass": ["Vine Whip", "Tackle", "Razor Leaf", "Solar Beam"],
            "Normal": ["Tackle", "Scratch", "Quick Attack", "Body Slam"],
        }
        return type_moves.get(ptype, ["Tackle", "Scratch", "Quick Attack", "Rest"])
    
    def is_alive(self):
        return self.current_hp > 0
    
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)
    
    def calculate_damage(self, move_name, target):
        base_damage = self.attack
        return max(10, base_damage - (target.defense // 4))
    
    async def use_move_async(self, move_name, target):
        print(f"{self.name} is preparing {move_name}...")
        await asyncio.sleep(0.5)
        
        damage = self.calculate_damage(move_name, target)
        
        print(f"💫 {move_name} hits {target.name}!")
        await asyncio.sleep(0.3)
        
        target.take_damage(damage)
        return damage

    async def status_effect_tick(self):
        effects_to_remove = []
        
        for effect_name, effect_data in self.status_effects.items():
            await asyncio.sleep(0.2)
            
            if effect_name == "poison":
                damage = self.max_hp // 16
                print(f"💜 {self.name} is hurt by poison! (-{damage} HP)")
                self.current_hp = max(0, self.current_hp - damage)
                
            elif effect_name == "burn":
                damage = self.max_hp // 16
                print(f"🔥 {self.name} is hurt by burn! (-{damage} HP)")
                self.current_hp = max(0, self.current_hp - damage)
            
            effect_data["turns"] -= 1
            if effect_data["turns"] <= 0:
                effects_to_remove.append(effect_name)
        
        for effect in effects_to_remove:
            del self.status_effects[effect]
            print(f"✨ {self.name} recovers from {effect}!")
            await asyncio.sleep(0.3)

    def add_status_effect(self, effect_name, turns=3):
        self.status_effects[effect_name] = {"turns": turns}
        print(f"🌟 {self.name} is affected by {effect_name}!")

if __name__ == "__main__":
    # Test the Pokemon class
    pikachu = Pokemon("Pikachu", "Electric", 100, 55, 40, 90)
    charmander = Pokemon("Charmander", "Fire", 95, 52, 43, 65)
    
    print(f"{pikachu.name} - HP: {pikachu.current_hp}, Moves: {pikachu.moves}")
    print(f"{charmander.name} - HP: {charmander.current_hp}, Moves: {charmander.moves}")
    