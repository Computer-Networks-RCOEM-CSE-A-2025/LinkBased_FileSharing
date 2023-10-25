CREATE DATABASE IF NOT EXISTS college;
USE college;

CREATE TABLE city (
    id INT PRIMARY KEY,
    name VARCHAR(80) DEFAULT "nagpur"
);

INSERT INTO city VALUES (1, "nagpur");
INSERT INTO city VALUES (2, "vardha");
INSERT INTO city VALUES (3, "koradi");

CREATE TABLE student (
    rollNo INT UNSIGNED PRIMARY KEY,
    name VARCHAR(100),
    gender CHAR(1),
    sem TINYINT UNSIGNED,
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES city(id)
);

INSERT INTO student VALUES (11, "Rashmi Kanharkar", "F", 5, 3);
INSERT INTO student VALUES (60, "Saurabh Wagh", "M", 5, 1);
INSERT INTO student VALUES (61, "Shreyansh Teldandhe", "M", 5, 1);
INSERT INTO student VALUES (4, "Jaya Singh", "F", 5, 2);

SELECT * FROM student;
select id from city where name="nagpur";
SELECT rollNo, name FROM student WHERE city_id=2;
