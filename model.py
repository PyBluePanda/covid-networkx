import networkx as nx
import numpy as np
import plotly.graph_objects as go
import pandas as pd

 
def create_interactive_plot(param_values: dict):
    
    N = param_values.get("N")
    p_asymptomatic = param_values.get("p_asymptomatic")
    p_transmission = param_values.get("p_transmission")
    incubation_period = param_values.get("incubation_period")
    recovery_time = param_values.get("recovery_time")
    timesteps = param_values.get("timesteps")
    network_type = param_values.get("network_type")
    

    if network_type == "small-world":
        G = nx.watts_strogatz_graph(N, k=4, p=0.2)
    elif network_type == "scale-free":
        G = nx.barabasi_albert_graph(N, m=2)
    elif network_type == "random":
        G = nx.erdos_renyi_graph(N, p=0.1)
    elif network_type == "complete":
        G = nx.complete_graph(N)
    elif network_type == "complete":
        G = nx.complete_graph(N)
    elif network_type == "cycle":
        G = nx.cycle_graph(N)
    elif network_type == "lollipop":
        m = round(0.8 * N)  # Approx 80% for the clique
        n = N - m
        G = nx.lollipop_graph(m,n)
    
    pos = nx.spring_layout(G, seed=37) 
    

    states = np.full((timesteps, N), 'S')  # Everyone starts as susceptible
    infection_timers = np.full(N, -1) 

    initial_infected = np.random.choice(N, size=1, replace=False)
    states[0, initial_infected] = 'E'  # Starts as exposed
    infection_timers[initial_infected] = 0

    state_counts = pd.DataFrame(columns=['timestep', 'S', 'E', 'A', 'I', 'R'])

    for t in range(1, timesteps):
        states[t] = states[t-1].copy()
        
        for node in G.nodes():
            if states[t-1, node] == 'S':
                infected_neighbors = [n for n in G.neighbors(node) if states[t-1, n] in ['A', 'I']]
                if infected_neighbors:
                    exposure_chance = 1 - (1 - p_transmission) ** len(infected_neighbors)
                    if np.random.rand() < exposure_chance:
                        states[t, node] = 'E'
                        infection_timers[node] = 0

            elif states[t-1, node] == 'E':
                infection_timers[node] += 1
                if infection_timers[node] >= incubation_period:
                    states[t, node] = 'A' if np.random.rand() < p_asymptomatic else 'I'

            elif states[t-1, node] in ['A', 'I']:
                infection_timers[node] += 1
                if infection_timers[node] >= recovery_time:
                    states[t, node] = 'R'

        counts = {state: np.sum(states[t] == state) for state in ['S', 'E', 'A', 'I', 'R']}
        state_counts.loc[t] = {'timestep': t, **counts}

    state_counts = state_counts.astype(int)

    network_metrics = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "avg_degree": sum(dict(G.degree()).values()) / N,
        "clustering_coeff": nx.average_clustering(G),
        "avg_path_length": nx.average_shortest_path_length(G) if nx.is_connected(G) else None,
        "avg_node_conn": nx.average_node_connectivity(G),
        "num_isolates": nx.number_of_isolates(G),
        "network_density": nx.density(G),
    }
    network_metrics_results = {
        "peak_infections": state_counts['I'].max(),
        "final_attack_rate": (state_counts['R'].max() / N) * 100,
        "epidemic_duration": state_counts[state_counts['I'] > 0]['timestep'].max(),
        "initial_infected_count": 1,  # Initial exposed node
        "R0_estimate": state_counts['R'].max() / 1
    }

    df_network_metrics = pd.DataFrame(network_metrics.items(), 
                                      columns=["Measure", "Value"])
    df_network_metrics_results = pd.DataFrame(network_metrics_results.items(), 
                                              columns=["Measure", "Value"])

    state_colors = {'S': 'blue', 
                    'E': 'orange', 
                    'A': 'white', 
                    'I': 'red', 
                    'R': 'green'}

    # frames for animation
    frames = []
    for t in range(timesteps):
        node_colors = [state_colors[states[t, i]] for i in range(N)]
        
        node_trace = go.Scatter(
            x=[pos[node][0] for node in G.nodes()],
            y=[pos[node][1] for node in G.nodes()],
            mode='markers',
            marker=dict(size=10, color=node_colors),
            text=[f"Node {i}: {states[t, i]}" for i in range(N)],
            hoverinfo='text'
        )

        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y, mode='lines', line=dict(width=1, color='gray'),
            hoverinfo='none'
        )

        frames.append(go.Frame(data=[edge_trace, node_trace], name=str(t)))


    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="COVID SEAIR Model Simulation",
            width=1000,
            height=450,
            showlegend=False,
            hovermode='closest',
            updatemenus=[{
                "buttons": [
                    {"args": [None, {"frame": {"duration": 500, "redraw": True},
                                      "fromcurrent": True}],
                    "label": "Play", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate"}],
                    "label": "Pause", "method": "animate"}
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 80},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0.2,
                "yanchor": "top"
            }],
            sliders=[{
                "steps": [
                    {"args": [[str(t)], {"frame": {"duration": 0, 
                                                   "redraw": True}, 
                                                   "mode": "immediate"}],
                    "label": str(t), "method": "animate"}
                    for t in range(timesteps)
                ],
                "active": 0,
                "x": 0.1, "y": 0.1,
                "xanchor": "left", "yanchor": "top"
            }]
        ),
        frames=frames
    )

    fig.update_layout(xaxis=dict(showgrid=False, visible=False),
                      yaxis=dict(showgrid=False, visible=False)
                      )

    return fig, state_counts, df_network_metrics, df_network_metrics_results


import plotly.express as px

def create_results_plot(state_counts):

    fig_time_series = px.line(
        state_counts.melt(id_vars=['timestep'], 
                          var_name='State', 
                          value_name='Count'),
        x='timestep', y='Count', color='State', 
        color_discrete_sequence=["blue","orange","white","red","green"],
        title="COVID Infection Curve Over Time",
        labels={'timestep': 'Time Step', 'Count': 'Number of Nodes'},
        width=1000,
        height=550,
        markers=True
    )

    return fig_time_series
