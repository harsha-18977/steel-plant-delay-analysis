USE steel_delay_analysis;

INSERT INTO shops (shop_name) VALUES
('Coke Oven'),
('Blast Furnace'),
('Steel Melting Shop'),
('Rolling Mill'),
('Power Plant');

INSERT INTO agencies (agency_name) VALUES
('ABC Maintenance'),
('XYZ Services'),
('Prime Engineering'),
('Steel Tech Solutions'),
('Industrial Care');

INSERT INTO seasons (season_name) VALUES
('Summer'),
('Monsoon'),
('Winter');
SELECT * FROM shops;
SELECT * FROM agencies;
SELECT * FROM seasons;
INSERT INTO equipment (equipment_name, shop_id) VALUES
('Motor',1),
('Pump',1),
('Gearbox',2),
('Crusher',2),
('Conveyor Motor',3),
('Hydraulic Pump',3),
('Cooling Fan',4),
('Compressor',4),
('Belt Drive',5),
('Roller Motor',5);
select * from equipment;
INSERT INTO conveyors (conveyor_name, equipment_id) VALUES
('CV-101',1),
('CV-102',2),
('CV-103',3),
('CV-104',4),
('CV-105',5),
('CV-106',6),
('CV-107',7),
('CV-108',8),
('CV-109',9),
('CV-110',10);
INSERT INTO delay_types (delay_description) VALUES
('Motor Failure'),
('Bearing Failure'),
('Power Failure'),
('Belt Slip'),
('Material Jam'),
('Sensor Fault'),
('Maintenance Delay'),
('Hydraulic Failure'),
('Roller Damage'),
('Emergency Shutdown');
SELECT * FROM delay_types;
SELECT COUNT(*) AS Total_Records
FROM delay_records;
DESC delay_records;
DESC shops;
DESC equipment;
DESC conveyors;
DESC agencies;
DESC delay_types;
DESC seasons;
SELECT * FROM shops;
SELECT * FROM equipment;
SELECT * FROM conveyors;
SELECT * FROM agencies;
SELECT * FROM delay_types;
SELECT * FROM seasons;