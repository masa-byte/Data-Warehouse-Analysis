CREATE TABLE Cruise_Dimension (
    cruise_dim_id INT PRIMARY KEY,
    cruise_id INT NOT NULL,
    -- slowly changing dimension in case of cruise info change
    date_from DATE,
    date_to DATE,
    cruise_name VARCHAR(100) NOT NULL,
    cruise_category VARCHAR(100) NOT NULL,
    departure_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    ship_id INT NOT NULL,
    ship_capacity INT NOT NULL,
    ship_stars INT NOT NULL
);

CREATE SEQUENCE cruise_dim_id_seq;

CREATE
OR REPLACE TRIGGER cruise_dim_on_insert BEFORE
INSERT
    ON cruise_dimension FOR EACH ROW BEGIN
SELECT
    cruise_dim_id_seq.NEXTVAL INTO :NEW.cruise_dim_id
FROM
    DUAL;

END;

CREATE TABLE Passenger_Dimension (
    passenger_dim_id INT PRIMARY KEY,
    passenger_id INT NOT NULL,
    -- slowly changing dimension in case of passenger info change
    date_from DATE,
    date_to DATE,
    passenger_name VARCHAR(100) NOT NULL,
    passenger_surname VARCHAR(100) NOT NULL,
    passenger_country VARCHAR(100) NOT NULL,
    passenger_age INT NOT NULL,
    passenger_gender VARCHAR(1) CHECK(passenger_gender IN ('M', 'F')) NOT NULL,
    passenger_class VARCHAR(1) CHECK(passenger_class IN ('U', 'M', 'L')) NOT NULL -- U: Upper, M: Middle, L: Lower
);

CREATE SEQUENCE passenger_dim_id_seq;

CREATE
OR REPLACE TRIGGER passenger_dim_on_insert BEFORE
INSERT
    ON passenger_dimension FOR EACH ROW BEGIN
SELECT
    passenger_dim_id_seq.NEXTVAL INTO :NEW.passenger_dim_id
FROM
    DUAL;

END;

CREATE TABLE Ticket_Dimension (
    ticket_dim_id INT PRIMARY KEY,
    ticket_id INT NOT NULL,
    -- middle level of granularity
    cruise_id INT NOT NULL,
    -- deepest level of granularity
    passenger_id INT NOT NULL,
    -- slowly changing dimension in case of price or category types change
    date_from DATE,
    date_to DATE,
    ticket_category VARCHAR(100) CHECK(ticket_category IN ('S', 'P', 'D')) NOT NULL,
    ticket_price DECIMAL(10, 2) NOT NULL,
    created_at DATE NOT NULL
);

CREATE SEQUENCE ticket_dim_id_seq;

CREATE
OR REPLACE TRIGGER ticket_dim_on_insert BEFORE
INSERT
    ON ticket_dimension FOR EACH ROW BEGIN
SELECT
    ticket_dim_id_seq.NEXTVAL INTO :NEW.ticket_dim_id
FROM
    DUAL;

END;

CREATE TABLE Date_Dimension (
    date_dim_id INT PRIMARY KEY,
    sales_date DATE NOT NULL,
    sales_day INT NOT NULL,
    sales_month INT NOT NULL,
    sales_quarter INT NOT NULL,
    sales_year INT NOT NULL
);

CREATE SEQUENCE date_dim_id_seq;

CREATE
OR REPLACE TRIGGER date_dim_on_insert BEFORE
INSERT
    ON date_dimension FOR EACH ROW BEGIN
SELECT
    date_dim_id_seq.NEXTVAL INTO :NEW.date_dim_id
FROM
    DUAL;

END;

CREATE TABLE Sales_Fact (
    fact_id INT PRIMARY KEY,
    date_dim_id INT NOT NULL,
    cruise_dim_id INT NOT NULL,
    passenger_dim_id INT NOT NULL,
    ticket_dim_id INT NOT NULL,
    ticket_revenue DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (date_dim_id) REFERENCES Date_Dimension(date_dim_id),
    FOREIGN KEY (cruise_dim_id) REFERENCES Cruise_Dimension(cruise_dim_id),
    FOREIGN KEY (passenger_dim_id) REFERENCES Passenger_Dimension(passenger_dim_id),
    FOREIGN KEY (ticket_dim_id) REFERENCES Ticket_Dimension(ticket_dim_id)
);

CREATE SEQUENCE sales_fact_id_seq;

CREATE
OR REPLACE TRIGGER sales_fact_on_insert BEFORE
INSERT
    ON sales_fact FOR EACH ROW BEGIN
SELECT
    sales_fact_id_seq.NEXTVAL INTO :NEW.fact_id
FROM
    DUAL;

END;