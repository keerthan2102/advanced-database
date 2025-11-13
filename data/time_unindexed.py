import sqlite3, time, statistics, random

DB = "chinook.sqlite"

Q = """
SELECT t.TrackId, t.Name, ar.Name, al.Title, g.Name
FROM Track_u t
JOIN Album_u  al ON t.AlbumId  = al.AlbumId
JOIN Artist_u ar ON al.ArtistId = ar.ArtistId
JOIN Genre_u  g  ON t.GenreId   = g.GenreId
WHERE t.TrackId BETWEEN ? AND ?   -- vary to reduce cache effects
"""

def run_once(conn):
    lo = random.randint(1, 3000)
    hi = lo + 500
    t0 = time.perf_counter()
    _ = list(conn.execute(Q, (lo, hi)))   # materialize results
    return (time.perf_counter() - t0) * 1000  # ms

def main():
    conn = sqlite3.connect(DB)
    times = []
    # Optional warm-up
    _ = run_once(conn)
    for i in range(10):
        dt = run_once(conn)
        times.append(dt)
        print(f"run {i+1:02d}: {dt:.2f} ms")
    print("\nAverage over 10 runs: {:.2f} ms".format(statistics.mean(times)))
    print("Median: {:.2f} ms   Min/Max: {:.2f}/{:.2f} ms"
          .format(statistics.median(times), min(times), max(times)))

if __name__ == "__main__":
    main()
