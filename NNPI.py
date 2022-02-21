import matplotlib.pyplot as plt
import romania as ro
import random



# =============================================================================
# We are setting first population, for this example we choose population of
# hundred vectors with five features
# =============================================================================

first_population = []
for i in range(100):
    x = []
    for xi in range(5):
        xi = random.uniform(0,1)
        x.append(xi)
    first_population.append(x)

population = first_population

for i in range(50):
    # =========================================================================
    # Calculating objectives values
    # =========================================================================
    values1 = [ro.function1(x) for x in population]
    values2 = [ro.function2(x) for x in population]
    if(i < 19):
        # =====================================================================
        # Plotting population in regards to objectives
        # =====================================================================
        plot = plt.figure()
        plt.axis([-0.05, 1.05, -0.05, 7.5])
        plt.scatter(values1, values2)
        plt.savefig(f'frame {i}')
    fronts = ro.non_dominated_sorting(population, values1, values2)
    new_fronts = [ro.crowding_distance(x, values1, values2) for x in fronts]
    population = ro.making_children(ro.dividing_population(new_fronts, values1, values2))

# =============================================================================
# Last plot (pareto front)
# =============================================================================
plot = plt.figure()
plt.scatter(values1, values2)
plt.savefig('pareto')


