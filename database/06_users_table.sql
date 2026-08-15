USE steel_delay_analysis;
CREATE TABLE users (

    user_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    role VARCHAR(50) DEFAULT 'user'

);
INSERT INTO users (username, password, role)
VALUES
('sai', 'sai@69', 'admin');

SELECT * FROM users;