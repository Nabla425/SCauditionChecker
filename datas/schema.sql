USE SCDB;

CREATE TABLE support (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    idol VARCHAR(10) NOT NULL,
    totu INT NOT NULL,
    Vo INT NOT NULL,
    Da INT NOT NULL,
    Vi INT NOT NULL,
    Vo_rate FLOAT NOT NULL DEFAULT 0.0,
    Da_rate FLOAT NOT NULL DEFAULT 0.0,
    Vi_rate FLOAT NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(10) DEFAULT 'admin'
);

CREATE TABLE buff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    color VARCHAR(5) NOT NULL,
    rate INT NOT NULL,
    turn INT NOT NULL,
    val VARCHAR(100),
    support_id INT, 
    pweapon_id INT, 
    link_id INT, 
    FOREIGN KEY (support_id) REFERENCES support(id),
    FOREIGN KEY (pweapon_id) REFERENCES pweapon(id),
    FOREIGN KEY (link_id) REFERENCES pweapon(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(10) DEFAULT 'admin'
);

CREATE TABLE pweapon(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    ATK_type VARCHAR(6) NOT NULL,
    Vo FLOAT DEFAULT 0.0,
    Da FLOAT DEFAULT 0.0,
    Vi FLOAT DEFAULT 0.0,
    link_type VARCHAR(6) NOT NULL,
    link_Vo FLOAT ,
    link_Da FLOAT ,
    link_Vi FLOAT ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(10) DEFAULT "admin",
    CHECK (ATK_type IN ('single', 'whole')),
    CHECK (link_type IN ('ATK', 'buff'))
);

CREATE  TABLE passive(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    short_name VARCHAR(10) NOT NULL,
    times INT NOT NULL,
    rate INT NOT NULL,
    request VARCHAR(20) NOT NULL,
    args VARCHAR(100),
    pweapon_id INT, 
    support_id INT, 
    FOREIGN KEY (pweapon_id) REFERENCES pweapon(id),
    FOREIGN KEY (support_id) REFERENCES support(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(10) DEFAULT "admin"    
);

CREATE TABLE passive_rate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passive_id INT,
    FOREIGN KEY (passive_id) REFERENCES passive(id),
    color VARCHAR(5) NOT NULL,
    rate INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(10) DEFAULT 'admin'
);