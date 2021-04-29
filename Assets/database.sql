-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema game
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema game
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `game` DEFAULT CHARACTER SET utf8 ;
USE `game` ;

-- -----------------------------------------------------
-- Table `game`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `game`.`enemies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`enemies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `attack` INT NULL DEFAULT NULL,
  `defense` INT NULL DEFAULT NULL,
  `hp` INT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `user_id` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_paladin_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_enemies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `game`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 147
DEFAULT CHARACTER SET = utf8;


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
  `gold` INT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_paladin_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_paladin_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `game`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 23
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `game`.`inventory`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`inventory` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `inventorycol` VARCHAR(45) NULL DEFAULT NULL,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `effect` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_inventory_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_inventory_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`))
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
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `game`.`items_shop`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`items_shop` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `effect` INT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
