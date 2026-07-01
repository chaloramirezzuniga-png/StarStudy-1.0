def build_schedule_table(entries, day_values):
    all_times = []
    for e in entries:
        time_str = e.start_time.strftime('%H:%M')
        if time_str not in all_times:
            all_times.append(time_str)
    all_times.sort()

    if not all_times:
        all_times = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']

    grid = {}
    for e in entries:
        key = (e.day, e.start_time.strftime('%H:%M'))
        if key not in grid:
            grid[key] = []
        grid[key].append(e)

    rows = []
    for slot in all_times:
        cells = []
        for day_value in day_values:
            entries_in_cell = grid.get((day_value, slot), [])
            cells.append(entries_in_cell)
        rows.append((slot, cells))

    return rows
