create database pfi;
use pfi;
--  Utilizar esses cod no banco de dados 
create table usuarios (
    id int primary key auto_increment,
    nome varchar(255),
    email varchar(255) not null unique,
    senha varchar(255) not null,
    adm boolean,
    pontos int
);

CREATE TABLE escritoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nacionalidade VARCHAR(100),
    biografia TEXT,
    data_nascimento DATE,
    data_falecimento DATE,
    foto LONGBLOB,
    link VARCHAR(255)
);

CREATE TABLE questoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pergunta VARCHAR(500)
);


CREATE TABLE alternativas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto VARCHAR(100),
    correta BOOLEAN,
    pergunta_id INT
);