import networkx as nx
import plotly.graph_objects as go

# Load graph from file
graph_file = "./test.graph"
graph = nx.read_graph6(graph_file)

# Create Plotly figure from NetworkX graph
fig = go.Figure(go.Scatter(
    x=[],
    y=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(size=10, color='blue')
))

# Add nodes to the figure
for node in graph.nodes():
    x, y = graph.nodes[node]['pos']
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode='markers',
        marker=dict(size=10, color='blue'),
        hovertext=str(node)
    ))

# Add edges to the figure
for edge in graph.edges():
    x0, y0 = graph.nodes[edge[0]]['pos']
    x1, y1 = graph.nodes[edge[1]]['pos']
    fig.add_trace(go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode='lines',
        line=dict(color='black'),
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    title="Graph Visualization",
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False)
)

# Save figure to HTML file
html_file = "graph_visualization.html"
fig.write_html(html_file)

print("Graph visualization saved to", html_file)
