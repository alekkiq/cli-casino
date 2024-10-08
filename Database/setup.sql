DROP DATABASE IF EXISTS `cli_casino`;
CREATE DATABASE `cli_casino` CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;
USE `cli_casino`;

-- Tables
CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(25) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

CREATE TABLE `user_statistics` (
  `user_id` INTEGER PRIMARY KEY,
  `balance` INTEGER DEFAULT 1000,
  `total_winnings` INTEGER DEFAULT 0,
  `games_played` INTEGER DEFAULT 0,
  `games_won` INTEGER DEFAULT 0,
  `games_lost` INTEGER DEFAULT 0,
  `is_banned` BOOLEAN DEFAULT 0,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

CREATE TABLE `game_types` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  `name_en` VARCHAR(50) NOT NULL UNIQUE,
  `rules` TEXT
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

CREATE TABLE `game_history` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `bet` INTEGER,
  `win_amount` INTEGER,
  `played_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id` INTEGER NOT NULL,
  `game_type_id` INTEGER NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`game_type_id`) REFERENCES `game_types` (`id`)
) ENGINE=InnoDB DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

-- Indexes
CREATE INDEX idx_user_id_history ON `game_history` (`user_id`);
CREATE INDEX idx_game_id_history ON `game_history` (`game_type_id`);

-- Game types
INSERT INTO `game_types` 
  (`name`, `name_en`, `rules`)
VALUES
  ('nopanheitto', 'dice', 'Pelaaja valitsee itse, kuinka suurta noppaa heittää. Pelaajan tulee sitten arvata nopan oikea silmäluku.\n\n- Voittokerroin on silmälukujen lukumäärä'),
  ('ruletti', 'roulette', 'Pelaaja arvaa värin sekä halutessaan kahta numeroa. Pelaaja asettaa jokaiselle arvaukselle (väri sekä numerot) oman erillisen panoksensa.\n\n- Numeroarvauksen voittokerroin = 36x\n- Väriarvauksen = 2x'),
  ('ventti', 'twentyone', 'Pelaaja saa kaksi korttia, joista toinen on piilotettu. Pelaaja voi joko jäädä tai ottaa lisää kortteja. Tavoitteena on saada korttien summa mahdollisimman lähelle 21:ä, mutta ei yli. Pelaaja voittaa, jos hänen korttiensa summa on suurempi kuin jakajan korttien summa, mutta ei yli 21:ä.\n\n- Voittokerroin = 2x'),
  ('hedelmäpeli', 'slots', 'Pelaaja asettaa panoksen ja painaa pelinappia. Pelissä on 4 rullaa, joissa on erilaisia symboleja. Jos rullat pysähtyvät samoihin symboleihin, pelaaja voittaa.\n\nVoittokertoimet:\n- 2 vierekkäistä symbolia = 1.5x\n- 3 vierekkäistä symbolia = 4x\n- 4 vierekkäistä symbolia = 16x')
  ('kolikonheitto', 'coinflip', 'Pelaaja valitsee joko kruunan tai klaavan. Jos pelaaja arvaa oikein, hän voittaa.\n\n- Voittokerroin = 2x');

-- Test data TODO remove
-- Insert test data into `users` table
INSERT INTO `users` (`username`, `password`)
VALUES
-- password is 'password' in sha256
('admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
('john_doe', 'P@ssw0rd123'),
('jane_smith', 'S3cur3P@ss'),
('alice_jones', 'Al1c3J0n3s!'),
('bob_brown', 'B0bBr0wn#'),
('charlie_davis', 'Ch@rl13D@v!s'),
('david_clark', 'D@v1dCl@rk$'),
('emily_miller', 'Em1lyM!ll3r'),
('frank_wilson', 'Fr@nkW1ls0n'),
('grace_lee', 'Gr@c3L33!'),
('henry_moore', 'H3nryM00r3'),
('isabella_taylor', 'Is@b3ll@T@yl0r'),
('jack_anderson', 'J@ckAnd3rs0n'),
('karen_thomas', 'K@r3nTh0m@s'),
('larry_martin', 'L@rryM@rt1n'),
('maria_white', 'M@r1@Wh1t3'),
('nancy_harris', 'N@nc7H@rr1s'),
('oliver_clark', '0l1v3rCl@rk'),
('paula_roberts', 'P@ul@R0b3rts'),
('quentin_walker', 'Qu3nt1nW@lk3r'),
('testbanned', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- Insert test data into `user_statistics` table
INSERT INTO `user_statistics` (`user_id`, `balance`, `total_winnings`, `games_played`, `games_won`, `games_lost`, `is_banned`)
VALUES
(1, 9999999, 500, 10, 5, 5, 0),
(2, 2000, 1500, 20, 15, 5, 0),
(3, 3000, 2500, 30, 25, 5, 0),
(4, 4000, 3500, 40, 35, 5, 0),
(5, 5000, 4500, 50, 45, 5, 0),
(6, 6000, 5500, 60, 55, 5, 0),
(7, 7000, 6500, 70, 65, 5, 0),
(8, 8000, 7500, 80, 75, 5, 0),
(9, 9000, 8500, 90, 85, 5, 0),
(10, 10000, 9500, 100, 95, 5, 0),
(11, 11000, 10500, 110, 105, 5, 0),
(12, 12000, 11500, 120, 115, 5, 0),
(13, 13000, 12500, 130, 125, 5, 0),
(14, 14000, 13500, 140, 135, 5, 0),
(15, 15000, 14500, 150, 145, 5, 0),
(16, 16000, 15500, 160, 155, 5, 0),
(17, 17000, 16500, 170, 165, 5, 0),
(18, 18000, 17500, 180, 175, 5, 0),
(19, 19000, 18500, 190, 185, 5, 0),
(20, 20000, 19500, 200, 195, 5, 0),
(21, 16000, 25000, 100, 40, 20, 1);