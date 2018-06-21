INSERT INTO todo_list (id, name, description)
VALUES
  ('a4e0e3bd8a0d45a9969074bdf4253852', 'mama', 'house needs'),
  ('e8f83d1b5d3e437d8674a93cd9087a2b', 'rapha', 'raphas needs');

INSERT INTO task (id, list_id, name, completed)
VALUES
  ('7f42c4ce43d44ca291eff92017966a28', 'a4e0e3bd8a0d45a9969074bdf4253852', 'get milk', FALSE),
  ('340030b790b54488bfe93e6b76818b2d', 'a4e0e3bd8a0d45a9969074bdf4253852', 'get sugar', TRUE),
  ('6494d8f81e424498a0c05a22ad94400e', 'a4e0e3bd8a0d45a9969074bdf4253852', 'get real', FALSE),
  ('6ffcc391c8bd47f99b6bb2e27dc30318', 'e8f83d1b5d3e437d8674a93cd9087a2b', 'get beer', FALSE);
