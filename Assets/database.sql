-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema game
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema game
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `game` DEFAULT CHARACTER SET utf8 ;
USE `game` ;

-- -----------------------------------------------------
-- Table `game`.`paladin_abilities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`paladin_abilities` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game`.`paladin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`paladin` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `attack` INT NULL,
  `defense` INT NULL,
  `hp` INT NULL,
  `sword` INT NULL,
  `shield` INT NULL,
  `armor` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `paladin_ability_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_paladin_paladin_abilities1_idx` (`paladin_ability_id` ASC) VISIBLE,
  CONSTRAINT `fk_paladin_paladin_abilities1`
    FOREIGN KEY (`paladin_ability_id`)
    REFERENCES `game`.`paladin_abilities` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL,
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  INDEX `fk_users_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game`.`items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `description` TEXT NULL,
  `effect` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_items_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game`.`currency`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`currency` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_currency_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_currency_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `game`.`paladin_upgrades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `game`.`paladin_upgrades` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `item_class` VARCHAR(255) NULL,
  `attack` INT NULL,
  `defense` INT NULL,
  `description` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `paladin_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_paladin_upgrades_paladin1_idx` (`paladin_id` ASC) VISIBLE,
  CONSTRAINT `fk_paladin_upgrades_paladin1`
    FOREIGN KEY (`paladin_id`)
    REFERENCES `game`.`paladin` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
