from collections import deque
import heapq

class SocialNetwork:
    """
    Represents a simple social network using an adjacency list (dictionary).
    Each user has a set of friends/followers (directed edges).
    User profiles are stored in a separate dictionary (hash table).
    """

    def __init__(self):
        # Adjacency list: user -> set of connections (friends/followers)
        self.adj = {}  # e.g., {'alice': {'bob', 'carol'}, ...}
        # User profile storage: user -> dict of profile attributes
        self.profiles = {}

    def add_user(self, user_id):
        """
        Add a new user to the network.
        If the user already exists, nothing happens.
        """
        if user_id not in self.adj:
            self.adj[user_id] = set()
            self.profiles[user_id] = {}
            print(f"User '{user_id}' added.")
        else:
            print(f"User '{user_id}' already exists.")

    def add_connection(self, user_from, user_to):
        """
        Add a connection (directed edge) from user_from to user_to.
        Both users must exist.
        """
        if user_from not in self.adj or user_to not in self.adj:
            print("Both users must exist to create a connection.")
            return
        self.adj[user_from].add(user_to)
        print(f"Connection added: {user_from} -> {user_to}")

    def add_profile(self, user_id, profile_dict):
        """
        Update or create the profile for a user.
        """
        if user_id in self.profiles:
            self.profiles[user_id].update(profile_dict)
            print(f"Profile updated for '{user_id}'.")
        else:
            print(f"User '{user_id}' not found.")

    def get_profile(self, user_id):
        """
        Get the profile dictionary for a user.
        """
        return self.profiles.get(user_id, None)

    def degree_centrality(self):
        """
        Calculate the degree centrality for each user (number of outgoing connections).
        Returns a dictionary: user -> degree
        """
        centrality = {}
        for user, neighbors in self.adj.items():
            centrality[user] = len(neighbors)
        return centrality

    def top_k_influencers(self, centrality, k):
        """
        Return the top-k users with the highest degree centrality.
        Uses a max-heap for efficiency.
        """
        # Negate degree so largest degree comes first
        heap = [(-deg, user) for user, deg in centrality.items()]
        heapq.heapify(heap)
        top_k = []
        for _ in range(min(k, len(heap))):
            deg, user = heapq.heappop(heap)
            top_k.append((user, -deg))
        return top_k

    def bfs(self, start_user):
        """
        Perform Breadth-First Search to find all users reachable from start_user.
        Returns a set of reachable users.
        """
        if start_user not in self.adj:
            print(f"User '{start_user}' not found.")
            return set()
        visited = set()
        queue = deque()
        queue.append(start_user)
        visited.add(start_user)
        while queue:
            user = queue.popleft()
            for neighbor in self.adj[user]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return visited

    def __str__(self):
        """
        Simple string representation for debugging.
        """
        return f"Users: {list(self.adj.keys())}\nConnections: {self.adj}\nProfiles: {self.profiles}"


# Example usage and demonstration script:
if __name__ == "__main__":
    # Initialize the network
    network = SocialNetwork()

    # Add users
    network.add_user("alice")
    network.add_user("bob")
    network.add_user("carol")
    network.add_user("alice")  # Test duplicate

    # Add connections
    network.add_connection("alice", "bob")
    network.add_connection("bob", "carol")
    network.add_connection("carol", "alice")
    network.add_connection("bob", "dave")  # Test connection with non-existent user

    # Add and retrieve profile
    network.add_profile("alice", {"name": "Alice", "bio": "Loves algorithms"})
    print("Alice's profile:", network.get_profile("alice"))

    # Centrality and top influencers
    cent = network.degree_centrality()
    print("Degree centrality:", cent)
    top2 = network.top_k_influencers(cent, 2)
    print("Top 2 influencers:", top2)

    # BFS
    reachable = network.bfs("alice")
    print("Reachable from Alice:", reachable)

    # Print final network state for review
    print("\nNetwork snapshot:")
    print(network)
