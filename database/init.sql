CREATE TABLE IF NOT EXISTS devices (
    device_id   TEXT PRIMARY KEY,
    hostname    TEXT NOT NULL,
    location    TEXT NOT NULL,
    vendor      TEXT NOT NULL,
    capacity_tb NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS metrics (
    id           SERIAL PRIMARY KEY,
    device_id    TEXT REFERENCES devices(device_id),
    used_tb      NUMERIC NOT NULL,
    capacity_tb  NUMERIC NOT NULL,
    latency_ms   NUMERIC NOT NULL,
    iops         INTEGER NOT NULL,
    health_status TEXT NOT NULL,
    collected_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_metrics_device_id ON metrics(device_id);
CREATE INDEX IF NOT EXISTS idx_metrics_collected_at ON metrics(collected_at);

INSERT INTO devices (device_id, hostname, location, vendor, capacity_tb) VALUES
  ('dev001', 'storage-east-01', 'East Data Center',  'NetApp',  500),
  ('dev002', 'storage-east-02', 'East Data Center',  'NetApp',  750),
  ('dev003', 'storage-west-01', 'West Data Center',  'Pure Storage', 1000),
  ('dev004', 'storage-west-02', 'West Data Center',  'Pure Storage', 1200),
  ('dev005', 'storage-central-01', 'Central DC',     'Dell EMC', 2000),
  ('dev006', 'storage-central-02', 'Central DC',     'Dell EMC', 800),
  ('dev007', 'storage-dr-01',   'DR Site',           'IBM',      600),
  ('dev008', 'storage-dr-02',   'DR Site',           'IBM',      900)
ON CONFLICT DO NOTHING;