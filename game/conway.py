import numpy as np
import random

class ConwayGameOfLife:
    """Core Conway's Game of Life implementation with AI evolution"""
    
    def __init__(self, width=80, height=60):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.generation = 0
        
    def initialize_random(self, density=0.3):
        """Initialize grid with random cells"""
        self.grid = np.random.choice([0, 1], size=(self.height, self.width), p=[1-density, density])
        
    def initialize_pattern(self, pattern, x, y):
        """Place a pattern at position (x, y)"""
        h, w = pattern.shape
        self.grid[y:y+h, x:x+w] = pattern
        
    def count_neighbors(self, x, y):
        """Count live neighbors using toroidal topology"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                count += self.grid[ny, nx]
        return count
    
    def update(self):
        """Apply Conway's Game of Life rules"""
        new_grid = np.copy(self.grid)
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                
                # Apply rules
                if self.grid[y, x] == 1:  # Cell is alive
                    if neighbors < 2 or neighbors > 3:
                        new_grid[y, x] = 0  # Dies
                else:  # Cell is dead
                    if neighbors == 3:
                        new_grid[y, x] = 1  # Comes alive
        
        self.grid = new_grid
        self.generation += 1
        
    def get_grid(self):
        """Return current grid state"""
        return self.grid.copy()
    
    def get_population(self):
        """Return number of live cells"""
        return np.sum(self.grid)
    
    def is_stable(self):
        """Check if pattern is stable (no changes)"""
        test_grid = np.copy(self.grid)
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                if self.grid[y, x] == 1:
                    if neighbors < 2 or neighbors > 3:
                        return False
                else:
                    if neighbors == 3:
                        return False
        return True


class AICreature:
    """AI creature with genetic code for Game of Life"""
    
    def __init__(self, dna=None, name=""):
        self.dna = dna if dna else self.random_dna()
        self.name = name
        self.fitness_score = 0
        self.battles_won = 0
        self.battles_lost = 0
        
    @staticmethod
    def random_dna(length=16):
        """Generate random DNA sequence"""
        return [random.randint(0, 1) for _ in range(length)]
    
    def create_initial_pattern(self):
        """Convert DNA to initial pattern"""
        size = int(np.sqrt(len(self.dna)))
        pattern = np.array(self.dna[:size*size]).reshape(size, size)
        return pattern
    
    def evaluate_fitness(self, generations=50):
        """Run creature in Game of Life and evaluate fitness"""
        game = ConwayGameOfLife(width=40, height=40)
        pattern = self.create_initial_pattern()
        game.initialize_pattern(pattern, 15, 15)
        
        max_population = 0
        generations_alive = 0
        
        for _ in range(generations):
            game.update()
            population = game.get_population()
            
            if population > 0:
                generations_alive += 1
                max_population = max(max_population, population)
            else:
                break
        
        # Fitness = longevity * population success
        self.fitness_score = generations_alive * (max_population / 100.0)
        return self.fitness_score
    
    def crossover(self, partner):
        """Create offspring through genetic crossover"""
        crossover_point = len(self.dna) // 2
        child_dna = self.dna[:crossover_point] + partner.dna[crossover_point:]
        child = AICreature(dna=child_dna, name=f"{self.name}_child")
        return child
    
    def mutate(self, mutation_rate=0.01):
        """Randomly mutate DNA"""
        for i in range(len(self.dna)):
            if random.random() < mutation_rate:
                self.dna[i] = 1 - self.dna[i]  # Flip bit
    
    def battle(self, opponent, generations=100):
        """Battle between two creatures"""
        game = ConwayGameOfLife(width=100, height=100)
        
        # Place creature 1
        p1_pattern = self.create_initial_pattern()
        game.initialize_pattern(p1_pattern, 10, 10)
        
        # Place creature 2
        p2_pattern = opponent.create_initial_pattern()
        game.initialize_pattern(p2_pattern, 70, 70)
        
        for _ in range(generations):
            game.update()
        
        final_population = game.get_population()
        
        # Determine winner (creature with more influence)
        if final_population > 50:
            self.battles_won += 1
            opponent.battles_lost += 1
            return True
        else:
            self.battles_lost += 1
            opponent.battles_won += 1
            return False


class EvolutionEngine:
    """Engine for evolving creature population"""
    
    def __init__(self, population_size=50):
        self.population = [AICreature(name=f"Creature_{i}") for i in range(population_size)]
        self.generation = 0
        self.history = []
        
    def evaluate_generation(self):
        """Evaluate fitness of all creatures"""
        for creature in self.population:
            creature.evaluate_fitness()
    
    def select_parents(self, tournament_size=3):
        """Tournament selection"""
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda c: c.fitness_score)
    
    def create_next_generation(self):
        """Create new generation through breeding"""
        self.evaluate_generation()
        
        # Keep best creatures (elitism)
        elite_size = len(self.population) // 10
        self.population.sort(key=lambda c: c.fitness_score, reverse=True)
        elite = self.population[:elite_size]
        
        # Breed new population
        new_population = elite.copy()
        while len(new_population) < len(self.population):
            parent1 = self.select_parents()
            parent2 = self.select_parents()
            child = parent1.crossover(parent2)
            child.mutate(mutation_rate=0.05)
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
        
        # Track best fitness
        best_fitness = max(c.fitness_score for c in self.population)
        self.history.append(best_fitness)
        
    def get_best_creature(self):
        """Return the best creature in current generation"""
        return max(self.population, key=lambda c: c.fitness_score)