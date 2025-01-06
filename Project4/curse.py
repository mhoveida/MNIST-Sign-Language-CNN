import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.datasets import make_blobs
import numpy as np

# Create figure and styling for plotting
fig, ax = plt.subplots(1, 1, figsize=(6, 3))
ax.set(xlabel='dimensions (m)', ylabel='log(dmax/dmin)', title='dmax/dmin vs. dimensionality')
line_styles = {0: 'ro-', 1: 'b^-', 2: 'gs-', 3: 'cv-'}

# Plot dmax/dmin ratio
# TODO: fill in valid test numbers
sample_size_list = [100, 500, 1000, 5000]

for idx, num_samples in enumerate(sample_size_list):
    # TODO: Fill in a valid feature range
    feature_range = range (1, 101)
    ratios = []
    for num_features in feature_range:
        # TODO: Generate synthetic data using make_classification
        X, _ = make_classification(
            n_samples=num_samples,
            n_features=num_features,
            n_informative=num_features,
            n_redundant=0,
            n_repeated=0,
            n_clusters_per_class=1,
            n_classes=1,
            random_state=42
        )
        # TODO: Choose random query point from X
        #query_point = X[np.random.randint(0, num_samples)]
        query_index = np.random.randint(0, len(X))
        query_point = X[query_index]
        
        # TODO: remove query pt from X so it isn't used in distance calculations
        X_except_query = np.delete(X, query_index, axis = 0)

        # TODO: Calculate distances
        distances = np.linalg.norm(X_except_query - query_point, axis=1)
        ratio = np.max(distances) / np.min(distances)
        ratios.append(ratio)

    ax.plot(feature_range, np.log(ratios), line_styles[idx], label=f'N={num_samples:,}')

plt.legend()
plt.tight_layout()
plt.grid(True)
#plt.savefig('dmax_dmin_vs_dimensionality.png', dpi=300)
plt.show()
