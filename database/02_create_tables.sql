CREATE TABLE shops (
    shop_id INT AUTO_INCREMENT PRIMARY KEY,
    shop_name VARCHAR(100) NOT NULL
);
CREATE TABLE equipment (

    equipment_id INT AUTO_INCREMENT PRIMARY KEY,

    equipment_name VARCHAR(100) NOT NULL,

    shop_id INT,

    FOREIGN KEY (shop_id)

    REFERENCES shops(shop_id)

);
CREATE TABLE conveyors (

    conveyor_id INT AUTO_INCREMENT PRIMARY KEY,

    conveyor_name VARCHAR(100) NOT NULL,

    equipment_id INT,

    FOREIGN KEY (equipment_id)

    REFERENCES equipment(equipment_id)

);
CREATE TABLE agencies (

    agency_id INT AUTO_INCREMENT PRIMARY KEY,

    agency_name VARCHAR(100) NOT NULL

);
CREATE TABLE delay_types (

    delay_type_id INT AUTO_INCREMENT PRIMARY KEY,

    delay_description VARCHAR(150) NOT NULL

);
CREATE TABLE seasons (

    season_id INT AUTO_INCREMENT PRIMARY KEY,

    season_name VARCHAR(50) NOT NULL

);
CREATE TABLE delay_records (

    delay_id INT AUTO_INCREMENT PRIMARY KEY,

    delay_date DATE NOT NULL,

    shop_id INT NOT NULL,

    equipment_id INT NOT NULL,

    conveyor_id INT NOT NULL,

    agency_id INT NOT NULL,

    delay_type_id INT NOT NULL,

    season_id INT NOT NULL,

    delay_minutes INT NOT NULL,

    FOREIGN KEY (shop_id) REFERENCES shops(shop_id),

    FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id),

    FOREIGN KEY (conveyor_id) REFERENCES conveyors(conveyor_id),

    FOREIGN KEY (agency_id) REFERENCES agencies(agency_id),

    FOREIGN KEY (delay_type_id) REFERENCES delay_types(delay_type_id),

    FOREIGN KEY (season_id) REFERENCES seasons(season_id)

);