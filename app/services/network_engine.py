import networkx as nx

class ThreatNetworkEngine:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_sample_network(self):
        """
        Builds a realistic digital arrest / UPI fraud network.
        Nodes have groups: 'victim', 'scammer_phone', 'upi_id', 'bank_account', 'ip_address'
        """
        # Add Victims
        self.graph.add_node("Victim 1 (Delhi)", group="victim", title="Lost ₹2.5L", level=1)
        self.graph.add_node("Victim 2 (Pune)", group="victim", title="Lost ₹50K", level=1)
        self.graph.add_node("Victim 3 (Lucknow)", group="victim", title="Attempted Fraud", level=1)

        # Add Scammer Infrastructure
        self.graph.add_node("+91-9876543210", group="scammer_phone", title="Fake Police Caller", level=2)
        self.graph.add_node("+91-8765432109", group="scammer_phone", title="Fake CBI Officer", level=2)
        self.graph.add_node("103.15.22.45", group="ip_address", title="VPN/Proxy IP", level=3)
        
        # Add Financial Infrastructure
        self.graph.add_node("police.secure@ybl", group="upi_id", title="Mule Account UPI", level=3)
        self.graph.add_node("safe.kyc@hdfc", group="upi_id", title="Fake KYC UPI", level=3)
        self.graph.add_node("A/C 50100456789", group="bank_account", title="Master Drop Account", level=4)

        # Define Edges (Relationships)
        self.graph.add_edge("Victim 1 (Delhi)", "+91-9876543210", label="Called by")
        self.graph.add_edge("Victim 2 (Pune)", "+91-9876543210", label="Called by")
        self.graph.add_edge("Victim 3 (Lucknow)", "+91-8765432109", label="Called by")
        
        self.graph.add_edge("+91-9876543210", "103.15.22.45", label="Uses IP")
        self.graph.add_edge("+91-8765432109", "103.15.22.45", label="Uses IP")
        
        self.graph.add_edge("Victim 1 (Delhi)", "police.secure@ybl", label="Transferred ₹2.5L")
        self.graph.add_edge("Victim 2 (Pune)", "safe.kyc@hdfc", label="Transferred ₹50K")
        
        self.graph.add_edge("police.secure@ybl", "A/C 50100456789", label="Funneled")
        self.graph.add_edge("safe.kyc@hdfc", "A/C 50100456789", label="Funneled")

    def get_visjs_data(self):
        """
        Converts the NetworkX graph into the JSON format required by vis-network on the frontend.
        Calculates degree centrality to identify the most critical nodes.
        """
        self.build_sample_network()
        
        # Calculate centrality to size the nodes dynamically (highlighting the master accounts)
        centrality = nx.degree_centrality(self.graph)
        
        nodes = []
        for node, attr in self.graph.nodes(data=True):
            # Base size + centrality bonus
            size = 20 + (centrality[node] * 30) 
            nodes.append({
                "id": node,
                "label": node,
                "group": attr.get("group", "default"),
                "title": attr.get("title", ""),
                "level": attr.get("level", 1),
                "value": size
            })

        edges = []
        for source, target, attr in self.graph.edges(data=True):
            edges.append({
                "from": source,
                "to": target,
                "label": attr.get("label", ""),
                "arrows": "to"
            })

        return {"nodes": nodes, "edges": edges}