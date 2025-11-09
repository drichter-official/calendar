def custom_rule(self, grid, row, col, num):
    # Knight's move positions relative to (row, col)
    knight_moves = [
        (-2, -1), (-2, +1), (-1, -2), (-1, +2),
        (+1, -2), (+1, +2), (+2, -1), (+2, +1)
    ]

    for dr, dc in knight_moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < self.size and 0 <= nc < self.size:
            if grid[nr][nc] == num:
                return False