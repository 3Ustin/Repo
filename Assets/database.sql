-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Game
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Game
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Game` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema game
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema game
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `game` DEFAULT CHARACTER SET utf8 ;
USE `Game` ;

-- -----------------------------------------------------
-- Table `Game`.`players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Game`.`players` (
  `id` INT NOT NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Game`.`Paladin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Game`.`Paladin` (
  `hp` INT NOT NULL,
  `Paladincol` VARCHAR(45) NULL,
  PRIMARY KEY (`hp`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Game`.`enemies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Game`.`enemies` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `attack` INT NULL,
  `defense` INT NULL,
  `hp` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

USE `game` ;

-- -----------------------------------------------------
-- Table `game`.`paladin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`paladin` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `attack` INT NULL DEFAULT NULL,
  `defense` INT NULL DEFAULT NULL,
  `hp` INT NULL DEFAULT NULL,
  `sword` INT NULL DEFAULT NULL,
  `shield` INT NULL DEFAULT NULL,
  `armor` INT NULL DEFAULT NULL,
  `currency` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `game`.`items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `effect` INT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_items_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `game`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_users_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
