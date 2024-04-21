-- Table: Ships
CREATE TABLE Ships (
    ship_id INT PRIMARY KEY,
    ship_name VARCHAR(100) NOT NULL,
    ship_capacity INT NOT NULL,
    ship_stars INT NOT NULL
);

-- Table: Cruises
CREATE TABLE Cruises (
    cruise_id INT PRIMARY KEY,
    cruise_name VARCHAR(100) NOT NULL,
    departure_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    cruise_category VARCHAR(100) NOT NULL,
    ship_id INT NOT NULL,
    FOREIGN KEY (ship_id) REFERENCES Ships(ship_id)
);

-- Table: Passengers
CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    passenger_name VARCHAR(100) NOT NULL,
    passenger_surname VARCHAR(100) NOT NULL,
    passenger_country VARCHAR(100) NOT NULL,
    passenger_age INT NOT NULL,
    passenger_gender VARCHAR(1) CHECK(passenger_gender IN ('M', 'F')) NOT NULL,
    passenger_class VARCHAR(1) CHECK(passenger_class IN ('U', 'M', 'L')) NOT NULL -- U: Upper, M: Middle, L: Lower
);

-- Table: Tickets
CREATE TABLE Tickets (
    ticket_id INT PRIMARY KEY,
    cruise_id INT,
    passenger_id INT,
    ticket_price DECIMAL(10, 2) NOT NULL,
    ticket_category VARCHAR(100) CHECK(ticket_category IN ('S', 'P', 'D')) NOT NULL,
    -- S: Standard, P: Premium, D: Deluxe
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    FOREIGN KEY (cruise_id) REFERENCES Cruises(cruise_id),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id)
);

-- Table: Places
CREATE TABLE Places (
    place_id INT PRIMARY KEY,
    place_name VARCHAR(100) NOT NULL,
    place_country VARCHAR(100) NOT NULL
);

-- Table: Cruises_Places (junction table to represent the many-to-many relationship between Cruises and Places)
CREATE TABLE Cruises_Places (
    cruise_id INT,
    place_id INT,
    PRIMARY KEY (cruise_id, place_id),
    FOREIGN KEY (cruise_id) REFERENCES Cruises(cruise_id),
    FOREIGN KEY (place_id) REFERENCES Places(place_id)
);

-- Table: Staff
CREATE TABLE Staff (
    staff_id INT PRIMARY KEY,
    staff_name VARCHAR(100) NOT NULL,
    staff_surname VARCHAR(100) NOT NULL,
    staff_age INT NOT NULL,
    staff_gender VARCHAR(1) CHECK(staff_gender IN ('M', 'F')) NOT NULL,
    staff_position VARCHAR(100) NOT NULL,
    wage_per_hour DECIMAL(10, 2) NOT NULL,
    daily_hours INT NOT NULL
);

-- Table: Cruises_Staff (junction table to represent the many-to-many relationship between Cruises and Staff)
CREATE TABLE Cruises_Staff (
    cruise_id INT,
    staff_id INT,
    PRIMARY KEY (cruise_id, staff_id),
    FOREIGN KEY (cruise_id) REFERENCES Cruises(cruise_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);