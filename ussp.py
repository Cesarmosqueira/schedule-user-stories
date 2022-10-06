import numpy as np
import random
import matplotlib.pyplot as plt
from datetime import datetime
import sys


target = 0
epochs = 100
op = 0
if '-target' in sys.argv:
    target = int(sys.argv[sys.argv.index('-target')+1])
    op = 1
elif '-epochs' in sys.argv:
    epochs = int(sys.argv[sys.argv.index('-epochs')+1])
    op = 2
elif '-h' in sys.argv:
    s = """use: ussp [-option]
Note: Try not to use only one flag + the '-file' flag
-target         : The target value that you're trying to minimze (numerical)

-epoch          : The number of epochs you want to train the population (numerical)

-file           : The path of the file where you store your user stories information (str)
"""
    print(s)
    quit()
else:
    op = 3

filename = "inputs/many_us"
if '-file' in sys.argv:
    filename = sys.argv[sys.argv.index('-file')+1]

random.seed(datetime.now())
def randomize_with_size(arrays, size):
    """
        Args:
            - arrays: list of arrays representing the different orders of trasks
            - size: the number of arrays that will be returned. 
        Returns:
            -  An array of size 'size' with the same arrays given.
    """
    res = []
    for i in range(size):
        res += [arrays[i % len(arrays)]]
    random.shuffle(res)
    return res

# static data from the problem
with open(filename) as f:
    n, m = [int(x) for x in f.readline().split()]
    user_stories = np.zeros((n, m, 2), dtype=int)
    i = 0
    for line in f:
        user_stories[i] = np.array([int(x) for x in line.split()]).reshape(m, 2)
        i += 1

class USSP:
    def __init__(self):
        self.n=0
        self.m=0
        self.makespan=0

    def load_data(self, user_stories, n, m):
        self.user_stories = user_stories
        self.n = n
        self.m = m

    def set_reps(self, rep_):
        self.rep = rep_


    def calc_makespan(self, v=False):

        mstart = np.zeros((max(n,m)), dtype=int)
        jend = np.zeros((max(n,m)), dtype=int)
        idxs = np.zeros((n), dtype=int)
        makespan = 0
        for e in self.rep:
            i = idxs[e]
            idxs[e] += 1
            midx = self.user_stories[e, i, 0]
            time = self.user_stories[e, i, 1]
            if v:
                print(f"User story {e} item {i} to developer {midx} starting at {mstart[midx]} duration {time}")
                print(mstart, len(jend))

            mstart[midx] = max(mstart[midx], jend[e]) + time
            jend[e] = mstart[midx]
            if mstart[midx] > makespan:
                makespan = mstart[midx]
        self.makespan = makespan
        return makespan

    def random_sample(self):
        # gen m instances for each number between 0 and n (copilot did NOT wrote this)
        l = [x%self.n for x in range(self.n*self.m)]
        random.shuffle(l)
        return l

    def plot_graph(self, makespan):
        mstart = np.zeros((max(n,m)), dtype=int)
        jend = np.zeros((max(n,m)), dtype=int)
        idxs = np.zeros((n), dtype=int)
        width = 30
        schedule = np.zeros((self.m*width, makespan))

        for e in self.rep:
            i = idxs[e]
            idxs[e] += 1
            midx = self.user_stories[e, i, 0]
            time = self.user_stories[e, i, 1]
            mstart[midx] = max(mstart[midx], jend[e])
            schedule[midx*width:(midx+1)*width, mstart[midx]:mstart[midx] + time] = e+1
            mstart[midx] += time
            jend[e] = mstart[midx]

        plt.imshow(schedule)
        plt.show()


def genetic_stuff(reps, size):
    crossover_point = int(len(reps[0]) * 0.7)

    crossovered = []
    for t in  randomize_with_size(reps,  size):

        rest = t[crossover_point:].copy()
        random.shuffle(rest)
        res = [t[:crossover_point] + rest]


        # mutation
        if random.uniform(0.0, 1.0) <= 0.3:
            random.shuffle(res)
        crossovered +=  res

    return crossovered



size = 30 # population
population = []

for i in range(size):
    jssp = USSP()
    jssp.load_data(user_stories, n, m)
    jssp.set_reps(jssp.random_sample())
    jssp.calc_makespan()
    population += [jssp]


best_makespan = float('inf')
best_gnome = []

evolution_best = []
evolution_average = []
evolution_current_best = []
highlights = [[], []]
cross_validations = [[], []]
cross_validation_count = 0
i = 0




print("USSP with genetic algorithms")


while (op == 1 and best_makespan >= target) or (op == 2 and i < epochs) or (op == 3 and i < epochs):
    # Table [genomes, makespans]
    table = list(zip(population, [p.calc_makespan() for p in population]))
    table = sorted(table, key=lambda x: x[1], reverse=False)
    
    epoch_best_genome, epoch_best_makespan = table[0]
    if epoch_best_makespan <= best_makespan:
        best_makespan = epoch_best_makespan
        best_genome = epoch_best_genome.rep
        highlights[0] += [i]
        highlights[1] += [epoch_best_makespan]
    else:
        cross_validation_count += 1
        if cross_validation_count >= 50:
            cross_validations[0] += [i]
            cross_validations[1] += [epoch_best_makespan]
            for p in population:
                p.set_reps(p.random_sample())
            cross_validation_count = 0
            continue


            
    average = sum([x[1] for x in table])/len(table)

    print(f"Epoch #{i} Best: {epoch_best_makespan} Average: {average} Global: {best_makespan}")


    # telemetry
    evolution_best += [best_makespan]
    evolution_current_best += [epoch_best_makespan]
    evolution_average += [average]



    # crossover
    reps_array = [g[0].rep for g in table[:5]]
    reps_multiplied = randomize_with_size(reps_array, size)

    new_reps = genetic_stuff(reps_multiplied, size)

    # update pop
    for p in population:
        p.set_reps(new_reps[0])
    i += 1



model = USSP()
model.load_data(user_stories, n, m)
print(" == Best Genetic Evolution == ")
print(best_genome)
model.set_reps(best_genome)
print("Best makespan:", best_makespan)
print("Number of random samples:", len(cross_validations))
plt.title(f"Best solution. Total delay: {best_makespan}")
model.plot_graph(best_makespan)


plt.title(f"Evolution results: {best_makespan}")
plt.plot(evolution_best, c='r', label="Best genomes overall")
plt.plot(evolution_current_best, c='g', label="Best genomes in epoch")
# plt.plot(evolution_average, c='b', label="Average fitness in epoch")

plt.scatter(highlights[0], highlights[1], c='y', marker='X', cmap='summer')

plt.scatter(cross_validations[0], cross_validations[1], c='b', marker='o', cmap='summer', label="Shuffles")

plt.legend()
plt.ylabel("Delay")
plt.xlabel("Epoch")
plt.show()

