import numpy as np
import random
import matplotlib.pyplot as plt
from datetime import datetime

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
with open('demo') as f:
    n, m = [int(x) for x in f.readline().split()]
    jobs = np.zeros((n, m, 2), dtype=int)
    i = 0
    for line in f:
        jobs[i] = np.array([int(x) for x in line.split()]).reshape(m, 2)
        i += 1

class JSSP:
    def __init__(self):
        self.n=0
        self.m=0
        self.makespan=0

    def load_data(self, jobs, n, m):
        self.jobs = jobs
        self.n = n
        self.m = m

    def set_reps(self, rep_):
        self.rep = rep_


    def calc_makespan(self, v=False):
        mstart = np.zeros((self.m), dtype=int)
        jend = np.zeros((self.m), dtype=int)
        idxs = np.zeros((self.n), dtype=int)
        makespan = 0
        for e in self.rep:
            i = idxs[e]
            idxs[e] += 1
            midx = self.jobs[e, i, 0]
            time = self.jobs[e, i, 1]
            if v:
                print(f"Job {e} task {i} to machine {midx} starting at {mstart[midx]} duration {time}")
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
        mstart = np.zeros((self.m), dtype=int)
        jend = np.zeros((self.m), dtype=int)
        idxs = np.zeros((self.n), dtype=int)
        schedule = np.zeros((self.m*10, makespan))

        for e in self.rep:
            i = idxs[e]
            idxs[e] += 1
            midx = self.jobs[e, i, 0]
            time = self.jobs[e, i, 1]
            mstart[midx] = max(mstart[midx], jend[e])
            schedule[midx*10:(midx+1)*10, mstart[midx]:mstart[midx] + time] = e+1
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
        if random.uniform(0.0, 1.0) <= 0.02:
            random.shuffle(res)
        crossovered +=  res

    return crossovered

print("JSSP with genetic algorithms")


size = 30 # population
population = []

for i in range(size):
    jssp = JSSP()
    jssp.load_data(jobs, n, m)
    jssp.set_reps(jssp.random_sample())
    jssp.calc_makespan()
    population += [jssp]


best_makespan = float('inf')
best_gnome = []
epochs = 100
for i in range(epochs):
    
    # Table [genomes, makespans]
    table = list(zip(population, [p.calc_makespan() for p in population]))
    table = sorted(table, key=lambda x: x[1], reverse=False)
    
    epoch_best_genome, epoch_best_makespan = table[0]
    if epoch_best_makespan <= best_makespan:
        best_makespan = epoch_best_makespan
        best_genome = epoch_best_genome.rep
    

    average = sum([x[1] for x in table])/len(table)

    print(f"Epoch #{i} Best: {epoch_best_makespan} Average: {average} Global: {best_makespan}")

    # crossover
    reps_array = [g[0].rep for g in table[:5]]
    reps_multiplied = randomize_with_size(reps_array, size)

    new_reps = genetic_stuff(reps_multiplied, size)

    # update pop
    for p in population:
        p.set_reps(new_reps[0])


model = JSSP()
model.load_data(jobs, n, m)
print(" == Best Genetic Evolution == ")
print(best_genome)
model.set_reps(best_genome)
print(" Best makespan:", best_makespan)
plt.title("Best solution")
model.plot_graph(best_makespan)


