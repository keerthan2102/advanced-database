-- First, enable the PostGIS extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create a table with a geometry column
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    geom GEOMETRY(Point, 4326) -- 4326 is a common spatial reference system (WGS 84)
);

-- Insert some sample points with longitude and latitude (in WGS 84)
INSERT INTO locations (name, geom) VALUES 
('Point A', ST_SetSRID(ST_Point(-73.935242, 40.730610), 4326)),
('Point B', ST_SetSRID(ST_Point(-73.935150, 40.731450), 4326));

-- Now let's find points near a specific location (for example, within 1000 meters)
SELECT name, geom
FROM locations
WHERE ST_DWithin(
  geom::geography,
 ST_SetSRID(ST_Point(-73.935200, 40.730700), 4326)::geography, 1000
);