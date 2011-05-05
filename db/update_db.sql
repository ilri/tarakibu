CREATE TABLE IF NOT EXISTS place_infos (
       id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
       village VARCHAR(30) UNIQUE,
       province VARCHAR(30),
       district VARCHAR(30),
       district_code VARCHAR(10),
       division VARCHAR(10),
       location VARCHAR(30),
       sub_location VARCHAR(30)
       );

ALTER TABLE animals CHANGE sex sex ENUM('female', 'male', 'castrated');
ALTER TABLE animals CHANGE tag tag VARCHAR(50);
ALTER TABLE animal_measures CHANGE animal animal VARCHAR(50);
ALTER TABLE tag_reads CHANGE rfid rfid VARCHAR(50);


