SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `ngsv` ;
CREATE SCHEMA IF NOT EXISTS `ngsv` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `ngsv` ;

-- -----------------------------------------------------
-- Table `ngsv`.`sam`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`sam` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`sam` (
  `sam_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `file_name` VARCHAR(1024) NOT NULL ,
  `created_date` BIGINT NOT NULL ,
  `header` TEXT NOT NULL ,
  `lengths` TEXT NOT NULL ,
  `mapped` INT NOT NULL ,
  `number_of_chromosomes` INT NOT NULL ,
  `chromosomes` TEXT NOT NULL ,
  PRIMARY KEY (`sam_id`) ,
  INDEX `FILENAMEINDEX` (`file_name` ASC) ,
  INDEX `CREATEDDATEINDEX` (`created_date` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `ngsv`.`chromosome`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`chromosome` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`chromosome` (
  `chr_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `chromosome` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`chr_id`) ,
  UNIQUE INDEX `chromosome_UNIQUE` (`chromosome` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`sam_histogram`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`sam_histogram` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`sam_histogram` (
  `sam_id` BIGINT NOT NULL ,
  `binsize` BIGINT NOT NULL ,
  `created_date` BIGINT NOT NULL ,
  `sam_histogram_id` BIGINT NOT NULL AUTO_INCREMENT ,
  INDEX `fk_histogram_sam1_idx` (`sam_id` ASC) ,
  PRIMARY KEY (`sam_histogram_id`) ,
  INDEX `CREATEDDATEINDEX` (`created_date` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`histogram_bin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`histogram_bin` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`histogram_bin` (
  `sam_histogram_id` BIGINT NOT NULL ,
  `value` BIGINT NOT NULL ,
  `position` BIGINT NOT NULL ,
  `histogram_bin_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `chr_id` BIGINT NOT NULL ,
  INDEX `fk_histogramBin_samHistogram1_idx` (`sam_histogram_id` ASC) ,
  PRIMARY KEY (`histogram_bin_id`) ,
  INDEX `POSITIONINDEX` (`position` ASC) ,
  INDEX `fk_histogramBin_chromosome1_idx` (`chr_id` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`bed`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`bed` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`bed` (
  `bed_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `file_name` VARCHAR(1024) NOT NULL ,
  `created_date` BIGINT NOT NULL ,
  `track_name` TEXT NOT NULL ,
  `description` TEXT NOT NULL ,
  `visibility` INT NOT NULL ,
  `item_rgb` INT NOT NULL ,
  PRIMARY KEY (`bed_id`) ,
  INDEX `BEDFILENAMEINDEX` (`file_name` ASC) ,
  INDEX `BEDCREATEDDATEINDEX` (`created_date` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`bed_fragment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`bed_fragment` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`bed_fragment` (
  `bed_fragment_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `chr_id` BIGINT NOT NULL ,
  `chr_start` BIGINT NOT NULL ,
  `chr_end` BIGINT NOT NULL ,
  `name` TEXT NOT NULL ,
  `score` INT NOT NULL ,
  `strand` INT NOT NULL ,
  `thick_start` BIGINT NOT NULL ,
  `thick_end` BIGINT NOT NULL ,
  `item_r` INT NOT NULL ,
  `item_g` INT NOT NULL ,
  `item_b` INT NOT NULL ,
  `block_count` BIGINT NOT NULL ,
  `block_sizes` TEXT NOT NULL ,
  `block_starts` TEXT NOT NULL ,
  `bed_id` BIGINT NOT NULL ,
  PRIMARY KEY (`bed_fragment_id`) ,
  INDEX `fk_bedData_bed1_idx` (`bed_id` ASC) ,
  INDEX `CHRSTARTENDINDEX` (`chr_start` ASC, `chr_end` ASC) ,
  INDEX `fk_bedData_chromosome1_idx` (`chr_id` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`cytoband`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`cytoband` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`cytoband` (
  `cytoband_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `chr_id` BIGINT NOT NULL ,
  `chr_start` BIGINT NOT NULL ,
  `chr_end` BIGINT NOT NULL ,
  `name` TEXT NOT NULL ,
  `gie_stain` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`cytoband_id`) ,
  INDEX `fk_cytoBand_chromosome1_idx` (`chr_id` ASC) ,
  INDEX `CYTOBANDCHRINDEX` (`chr_id` ASC) ,
  INDEX `CYTOBANDPOSITIONINDEX` (`chr_start` ASC, `chr_end` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`ref_gene`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`ref_gene` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`ref_gene` (
  `ref_gene_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `bin` INT NOT NULL ,
  `name` TEXT NOT NULL ,
  `chr_id` BIGINT NOT NULL ,
  `strand` INT NOT NULL ,
  `tx_start` BIGINT NOT NULL ,
  `tx_end` BIGINT NOT NULL ,
  `cds_start` BIGINT NOT NULL ,
  `cds_end` BIGINT NOT NULL ,
  `exon_count` BIGINT NOT NULL ,
  `exon_starts` TEXT NOT NULL ,
  `exon_ends` TEXT NOT NULL ,
  `score` BIGINT NOT NULL ,
  `gene_name` VARCHAR(255) NOT NULL ,
  `cds_start_stat` INT NOT NULL ,
  `cds_end_stat` INT NOT NULL ,
  `exon_frames` TEXT NOT NULL ,
  PRIMARY KEY (`ref_gene_id`) ,
  INDEX `fk_refGene_chromosome1_idx` (`chr_id` ASC) ,
  INDEX `REFGENENAMEINDEX` (`gene_name` ASC) ,
  INDEX `REFGENECHRINDEX` (`chr_id` ASC) ,
  INDEX `REFGENETXPOSINDEX` (`tx_start` ASC, `tx_end` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`tag` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`tag` (
  `tag_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(255) NOT NULL ,
  `created_at` DATETIME NOT NULL ,
  `updated_at` DATETIME NOT NULL ,
  PRIMARY KEY (`tag_id`) ,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`sam_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`sam_tag` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`sam_tag` (
  `tag_id` BIGINT NOT NULL ,
  `sam_id` BIGINT NOT NULL ,
  INDEX `fk_tag_id_idx` (`tag_id` ASC) ,
  INDEX `fk_sam_id_idx` (`sam_id` ASC) ,
  PRIMARY KEY (`tag_id`, `sam_id`) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`bed_tag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`bed_tag` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`bed_tag` (
  `tag_id` BIGINT NOT NULL ,
  `bed_id` BIGINT NOT NULL ,
  INDEX `fk_tag_id_idx` (`tag_id` ASC) ,
  INDEX `fk_bed_id_idx` (`bed_id` ASC) ,
  PRIMARY KEY (`tag_id`, `bed_id`) )
ENGINE = MyISAM;

USE `ngsv` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
