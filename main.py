import pandas as pd
import numpy as np
from collections import deque
elevation=pd.read_csv("C:/Users/dell/Desktop/hackathon/data/elevation.csv" , header=None).values
illumination=pd.read_csv("C:/Users/dell/Desktop/hackathon/data/illumination.csv" , header=None).values
signal_occultation=pd.read_csv("C:/Users/dell/Desktop/hackathon/data/signal_occultation.csv" , header=None).values
water_ice=pd.read_csv("C:/Users/dell/Desktop/hackathon/data/water_ice.csv" , header=None).values
ROWS, COLS = elevation.shape
WINDOW = 5
MAX_SLOPE = 22
TOP_N=5
def site_stats(matrix,r,c):
      area=matrix[r:r+WINDOW, c:c+WINDOW]
      elev=elevation[r:r+WINDOW, c:c+WINDOW]
      avg_val=np.mean(area)
      rough=np.std(elev)
      return avg_val, rough
def find_best_sites(matrix, top_n=TOP_N):
    candidates = []
    for r in range(ROWS - WINDOW):
        for c in range(COLS - WINDOW):
            avg, rough = site_stats(matrix, r, c)
            score = avg - rough   
            candidates.append(((r, c), avg, rough, score))
    return sorted(candidates, key=lambda x: x[3], reverse=True)[:top_n]

habitats = find_best_sites(illumination)
mines = find_best_sites(water_ice)

def bfs(start, goal):
    q = deque([(start, [start])])
    visited = set([start])
    while q:
        (r, c), path = q.popleft()
        if (r, c) == goal:
            return path
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if (nr,nc) not in visited:
                    slope = abs(elevation[nr][nc] - elevation[r][c])
                    if slope <= MAX_SLOPE:
                        visited.add((nr,nc))
                        q.append(((nr,nc), path+[(nr,nc)]))
    return None

best_score = -1
best_result = None

for h in habitats:
    for m in mines:
        h_coord, h_avg, h_rough, _ = h
        m_coord, m_avg, m_rough, _ = m

        path = bfs(h_coord, m_coord)
        if path:
            path_len = len(path)
            score = 0.5*h_avg + 0.5*m_avg - 0.001*path_len
            print(f"Habitat {h[0]} | Mining {m[0]} | Score={score:.4f} | Path={path_len}")
            if score > best_score:
                best_score = score
                best_result = (h, m, path_len, score)

with open("result.txt", "w") as f:
    f.write(f"Optimal Pair Found with Combined Score: {best_score:.4f}\n\n")

    f.write("--- Optimal Habitat Site ---\n")
    f.write(f"> Coordinates (row, col): {best_result[0][0]}\n")
    f.write(f"> Avg Illumination: {best_result[0][1]:.4f}%\n")
    f.write(f"> Terrain Roughness (Std Dev): {best_result[0][2]:.4f} m\n\n")

    f.write("--- Optimal Mining Site ---\n")
    f.write(f"> Coordinates (row, col): {best_result[1][0]}\n")
    f.write(f"> Avg Water-Ice Probability: {best_result[1][1]:.4f}\n")
    f.write(f"> Terrain Roughness (Std Dev): {best_result[1][2]:.4f} m\n\n")

    f.write("--- Power Cable Path ---\n")
    f.write(f"> Path Length: {best_result[2]} cells ({best_result[2]*100} m)\n")

print("Done! Check result.txt for output.")
print("coded by team Visionary Duo.")

with open("result.txt","r") as f:
    print("\n--- OUTPUT FROM result.ttxt---\n")
    print(f.read())
      
# coded by team Visionary Duo PB02xPB08