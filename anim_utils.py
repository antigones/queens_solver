from collections import defaultdict

palette = ['🟦','🟪','🟧','🟩']
queens = {'🟦':'🔵','🟪':'🟣','🟧':'🟠','🟩':'🟢'}
regions = defaultdict(list)

def get_palette(board):
    # Identify regions and group cells by unique region numbers
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            region_id = board[r][c]
            regions[region_id].append((r, c))

    # Function to get adjacent regions for a given region
    def get_adjacent_regions(region_cells):
        adjacent = set()
        for r, c in region_cells:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != board[r][c]:
                    adjacent.add(board[nr][nc])
        return adjacent

    # Assign colors to regions
    region_colors = {}
    queen_colors = {}
    for region_id in sorted(regions.keys()):
        used_colors = {region_colors[adj] for adj in get_adjacent_regions(regions[region_id]) if adj in region_colors}
        for color in palette:
            if color not in used_colors:
                region_colors[region_id] = color
                queen_colors[region_id] = queens[color]
                break
    return region_colors,queen_colors


def print_solution(board, nr_of_queens, color_areas):
    palette,queens_colors = get_palette(color_areas)

    output = []
    for i in range(nr_of_queens):
        row = []
        for j in range(nr_of_queens):
            if board[i][j] == 1:
                row.append(queens_colors[color_areas[i][j]])
            else:
                row.append(palette[color_areas[i][j]])
        row.append('\n')
        output.append(row)
    return output