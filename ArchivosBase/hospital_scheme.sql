CREATE DATABASE IF NOT EXISTS hospital;
USE hospital;
CREATE TABLE IF NOT EXISTS expediente (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre varchar(255) NOT NULL,
  diagnostico varchar(450) NOT NULL,
  tratamiento varchar(450) NOT NULL,
  passwordSalt varchar(25) NOT NULL,
  diag_nonce varchar(12) NOT NULL,
  treat_nonce varchar(12) NOT NULL
);
