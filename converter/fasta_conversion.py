from Bio import SeqIO
from sklearn.cluster import KMeans
import numpy as np
import itertools
import plotly.express as px
import pandas as pd

# Step 1: Read FASTA files
sequences = []
test_data_file_path= 'data/Assessment_datasets_its1_powerlaw/35sp/jeu1/ITS1/Powerlaw/Archive/35sp_Powerlaw-01_R1.fastq'

for record in SeqIO.parse(test_data_file_path, "fastq"):
    sequences.append(str(record.seq))


# Step 2: Sequence preprocessing (convert sequences to numerical features)
# Here, we'll just use k-mer frequencies as features
def kmer_frequencies(sequence, k):
    frequencies = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        if kmer in frequencies:
            frequencies[kmer] += 1
        else:
            frequencies[kmer] = 1
    return [frequencies.get(kmer, 0) for kmer in all_kmers]


k = 4  # Choose the length of k-mers

all_kmers = [''.join(p) for p in itertools.product('ATGC', repeat=k)]
X = np.array([kmer_frequencies(seq, k) for seq in sequences])

# Step 3: Clustering
n_clusters = 3  # Choose the number of clusters
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(X)
labels = kmeans.labels_

# Step 4: Output clusters
for i in range(n_clusters):
    cluster_sequences = [sequences[j] for j in range(len(sequences)) if labels[j] == i]
    print(f"Cluster {i + 1}: {len(cluster_sequences)} sequences")
    for seq in cluster_sequences[:5]:  # Print first 5 sequences in each cluster
        print(seq)

# Assuming you have already performed clustering and have labels for each sequence
# Let's say you have a list 'labels' containing the cluster labels for each sequence

# Create a DataFrame with sequences and their cluster labels
data = {'Sequence': sequences, 'Cluster': labels}
df = pd.DataFrame(data)

# Assuming your sequences are of fixed length, you can calculate some summary statistics
# For example, let's calculate the length of each sequence
df['Sequence Length'] = df['Sequence'].apply(len)

# Visualize sequence lengths by cluster using a box plot
fig = px.box(df, x='Cluster', y='Sequence Length', title='Sequence Length Distribution by Cluster')

# Export the visualization to an HTML file
fig.write_html("cluster_visualization.html")
