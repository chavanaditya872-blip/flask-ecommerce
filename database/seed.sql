USE ecommerce_db;

-- Passwords:
-- admin@shop.com -> Admin@123
-- john@gmail.com -> User@123
INSERT INTO users (name, email, password, role) VALUES 
('Store Admin', 'admin@shop.com', 'scrypt:32768:8:1$K5zQe0Q1W7eN1m4W$c6f9fb19c968f86f7b198897eb2f5569e5d4cbefcce3f0b2f5b8ddc04a79667794db54b2fc5d564ce89a80b080ef8a1cb23ca6e6c1e5d7990bfa36c4aeebf115', 'admin'),
('John Doe', 'john@gmail.com', 'scrypt:32768:8:1$pG8NkmLpQ0iM2W1r$9b5965caeb9c88289bf443f11bc023eb2594dfb148fe334cf33fe304ee0c25a07504a584fe3ef4ffbd7fbddca4c07c4bc471d2c6764d2572b43b67e2a93fbddb', 'user');

INSERT INTO products (name, description, price, category, image, stock) VALUES
('Wireless Active Noise Cancelling Headphones', 'Premium over-ear Bluetooth headphones with rich bass, 40-hour battery life, and rapid charging.', 4999.00, 'Electronics', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600', 35),
('Minimalist Stainless Steel Analog Watch', 'Sleek matte dial with genuine top-grain leather strap and scratch-resistant sapphire glass.', 2499.00, 'Fashion', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600', 40),
('Mechanical RGB Gaming Keyboard', 'Tactile blue clicky mechanical switches with customizable per-key RGB backlighting and braided cable.', 3299.00, 'Gaming', 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600', 25),
('Ergonomic Aluminum Laptop Stand', 'Foldable 6-level adjustable desk stand suitable for all MacBooks and Windows laptops up to 17 inches.', 1199.00, 'Accessories', 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600', 60),
('Artisan Ceramic Pour-Over Coffee Maker', 'Handcrafted heat-resistant ceramic carafe with reusable stainless steel ultra-fine mesh filter.', 1499.00, 'Home & Kitchen', 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600', 18),
('Ultralight Breathable Running Shoes', 'Engineered knit upper with responsive shock-absorbing EVA foam sole for athletic performance.', 2799.00, 'Footwear', 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600', 50),
('Wireless Bluetooth Compact Soundbar', 'Dual high-output neodymium drivers delivering 30W stereo audio with deep bass passive radiator.', 2199.00, 'Electronics', 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=600', 30),
('Urban Commuter Waterproof Backpack', '30L capacity durable polyester travel bag with dedicated 15.6-inch padded laptop sleeve.', 1899.00, 'Accessories', 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600', 45),
('High-Precision Wireless Gaming Mouse', 'Optical 16,000 DPI sensor, ultra-lightweight honeycomb shell, and lag-free 2.4GHz receiver.', 1699.00, 'Gaming', 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=600', 32),
('Classic Aviator UV400 Sunglasses', 'Polarized anti-glare lenses with corrosion-resistant gold-toned metal alloy frame.', 999.00, 'Fashion', 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600', 75),
('Double-Walled Insulated Flask 1000ml', 'Food-grade 304 stainless steel thermos bottle keeping beverages hot for 18h and chilled for 24h.', 849.00, 'Home & Kitchen', 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600', 90),
('Smart Fitness Tracker Smartwatch', 'Real-time SpO2, heart rate monitor, sleep stage analysis, and full touch HD color display.', 2999.00, 'Electronics', 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=600', 42),
('Classic Canvas Slip-On Skate Shoes', 'Durable vulcanized rubber sole with reinforced canvas stitching for everyday street wear.', 1799.00, 'Footwear', 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=600', 38),
('Studio USB Condenser Microphone', 'Cardioid pickup pattern with metal shock mount, pop filter, and zero-latency audio monitoring.', 3499.00, 'Electronics', 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600', 20),
('Cast Iron Skillet Pan 26cm', 'Pre-seasoned heavy-duty cast iron pan delivering uniform heat retention for searing and baking.', 1599.00, 'Home & Kitchen', 'https://images.unsplash.com/photo-1590794056226-79ef3a8147e1?w=600', 22),
('RGB Extended Desk Mouse Pad', 'Micro-textured smooth cloth surface with non-slip natural rubber base and 10 lighting modes.', 799.00, 'Gaming', 'https://images.unsplash.com/photo-1616588589676-62b3bd4ff6d2?w=600', 80),
('Genuine Leather Bi-fold Wallet', 'Hand-stitched vintage cowhide wallet featuring RFID blocking shield with 8 card slots.', 899.00, 'Fashion', 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=600', 65),
('Fast Charging Magnetic Power Bank 10000mAh', '20W PD wireless fast charging external battery pack with slim pocket-friendly build.', 1999.00, 'Electronics', 'https://images.unsplash.com/photo-1609592424364-7bc7d251d782?w=600', 50),
('Aroma Essential Oil Diffuser 500ml', 'Ultrasonic cool mist quiet humidifier featuring 7 soft ambient LED night lights.', 1299.00, 'Home & Kitchen', 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=600', 30),
('Pro High-Top Basketball Shoes', 'Cushioned ankle collar, reinforced lateral support, and traction herringbone rubber outsole.', 3799.00, 'Footwear', 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=600', 28);
