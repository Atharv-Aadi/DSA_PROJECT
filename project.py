import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import heapq

MAX = 20

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeliverEase - Route Planner")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2f") 

        self.n = 0
        self.graph = []

        self.create_ui()

    #  UI
    def create_ui(self):

        title = tk.Label(
            self.root,
            text="🚚 DeliverEase - Route Planner",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        )
        title.pack(pady=15)

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(pady=10)

        btn_style = {
            "font": ("Arial", 12, "bold"),
            "width": 15,
            "height": 2,
            "bd": 0,
            "fg": "white"
        }

        tk.Button(frame, text="Set Nodes", bg="#4CAF50", command=self.set_nodes, **btn_style).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(frame, text="Add Edge", bg="#2196F3", command=self.add_edge, **btn_style).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(frame, text="Show Matrix", bg="#9C27B0", command=self.show_matrix, **btn_style).grid(row=0, column=2, padx=10, pady=10)

        tk.Button(frame, text="BFS", bg="#FF9800", command=self.run_bfs, **btn_style).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(frame, text="DFS", bg="#FF5722", command=self.run_dfs, **btn_style).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(frame, text="Dijkstra", bg="#00BCD4", command=self.run_dijkstra, **btn_style).grid(row=1, column=2, padx=10, pady=10)

        tk.Button(frame, text="Save", bg="#8BC34A", command=self.save_graph, **btn_style).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(frame, text="Load", bg="#FFC107", command=self.load_graph, **btn_style).grid(row=2, column=1, padx=10, pady=10)

        self.output = tk.Text(
            self.root,
            height=18,
            width=80,
            font=("Consolas", 11),
            bg="#2c2c3e",
            fg="#00ffcc",
            insertbackground="white"
        )
        self.output.pack(pady=15)

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    #Graph Setup
    def set_nodes(self):
        try:
            self.n = int(simpledialog.askstring("Input", "Enter number of nodes (max 20):"))
            if self.n <= 0 or self.n > MAX:
                raise ValueError
            self.graph = [[0]*self.n for _ in range(self.n)]
            self.log(f"Graph initialized with {self.n} nodes.")
        except:
            messagebox.showerror("Error", "Invalid number of nodes.")

    def add_edge(self):
        try:
            u = int(simpledialog.askstring("Input", "Enter source node:"))
            v = int(simpledialog.askstring("Input", "Enter destination node:"))
            w = int(simpledialog.askstring("Input", "Enter weight:"))

            if u<0 or v<0 or u>=self.n or v>=self.n or w<0:
                raise ValueError

            if u == v and w != 0:
                messagebox.showerror("Error", "Self-loop allowed only with weight 0.")
                return

            self.graph[u][v] = w
            self.graph[v][u] = w
            self.log(f"Edge added: {u} <-> {v} (weight {w})")

        except:
            messagebox.showerror("Error", "Invalid edge input.")

    def show_matrix(self):
        self.log("Adjacency Matrix:")
        for row in self.graph:
            self.log(str(row))

    #  BFS
    def bfs(self, src):
        visited = [False]*self.n
        queue = [src]
        visited[src] = True

        result = []
        while queue:
            v = queue.pop(0)
            result.append(v)
            for i in range(self.n):
                if self.graph[v][i] != 0 and not visited[i]:
                    visited[i] = True
                    queue.append(i)
        return result

    def run_bfs(self):
        try:
            src = int(simpledialog.askstring("Input", "Enter source node:"))
            res = self.bfs(src)
            self.log(f"BFS: {res}")
        except:
            messagebox.showerror("Error", "Invalid input.")

    # DFS
    def dfs_util(self, v, visited, result):
        visited[v] = True
        result.append(v)
        for i in range(self.n):
            if self.graph[v][i] != 0 and not visited[i]:
                self.dfs_util(i, visited, result)

    def dfs(self, src):
        visited = [False]*self.n
        result = []
        self.dfs_util(src, visited, result)
        return result

    def run_dfs(self):
        try:
            src = int(simpledialog.askstring("Input", "Enter source node:"))
            res = self.dfs(src)
            self.log(f"DFS: {res}")
        except:
            messagebox.showerror("Error", "Invalid input.")

    # Dijkstra
    def dijkstra(self, src, dest):
        dist = [float('inf')]*self.n
        prev = [-1]*self.n
        dist[src] = 0

        pq = [(0, src)]

        while pq:
            d, u = heapq.heappop(pq)

            for v in range(self.n):
                if self.graph[u][v] != 0:
                    new_dist = d + self.graph[u][v]
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = u
                        heapq.heappush(pq, (new_dist, v))

        path = []
        cur = dest
        while cur != -1:
            path.append(cur)
            cur = prev[cur]

        path.reverse()
        return dist[dest], path

    def run_dijkstra(self):
        try:
            src = int(simpledialog.askstring("Input", "Enter source:"))
            dest = int(simpledialog.askstring("Input", "Enter destination:"))

            dist, path = self.dijkstra(src, dest)

            if dist == float('inf'):
                self.log("No path exists.")
            else:
                self.log(f"Shortest Distance: {dist}")
                self.log(f"Path: {path}")

        except:
            messagebox.showerror("Error", "Invalid input.")

    #  STORAGE 
    def save_graph(self):
        try:
            with open("graph_data.json", "a") as f:
                json.dump({"n": self.n, "graph": self.graph}, f)
            self.log("Graph saved to file.")
        except:
            messagebox.showerror("Error", "Save failed.")

    def load_graph(self):
        try:
            with open("graph_data.json", "r") as f:
                data = json.load(f)
                self.n = data["n"]
                self.graph = data["graph"]
            self.log("Graph loaded from file.")
        except:
            messagebox.showerror("Error", "Load failed.")


root = tk.Tk()
app = GraphApp(root)
root.mainloop()