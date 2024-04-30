from qiime2.plugins import feature_table
from qiime2 import Artifact

unrarefied_table = Artifact.load('data/sample-metadata.tsv')
rarefy_result = feature_table.methods.rarefy(table=unrarefied_table, sampling_depth=100)
rarefied_table = rarefy_result.rarefied_table