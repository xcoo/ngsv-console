SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Table `ngsv`.`cnv`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`cnv` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`cnv` (
  `cnv_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `file_name` VARCHAR(1024) NOT NULL ,
  `created_date` BIGINT NOT NULL ,
  PRIMARY KEY (`cnv_id`) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `ngsv`.`cnv_fragment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ngsv`.`cnv_fragment` ;

CREATE  TABLE IF NOT EXISTS `ngsv`.`cnv_fragment` (
  `cnv_fragment_id` BIGINT NOT NULL AUTO_INCREMENT ,
  `cnv_id` BIGINT NOT NULL ,
  `chr_id` BIGINT NOT NULL ,
  `chr_start` BIGINT NOT NULL ,
  `chr_end` BIGINT NOT NULL ,
  `lengths` TEXT NOT NULL ,
  `state` VARCHAR(45) NOT NULL ,
  `copy_number` BIGINT NOT NULL ,
  `num_snp` BIGINT NOT NULL ,
  `snp_start` VARCHAR(45) NOT NULL ,
  `snp_end` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`cnv_fragment_id`) ,
  INDEX `fk_cnv_idx` (`cnv_id` ASC) ,
  INDEX `CHRSTARTENDINDEX` (`chr_start` ASC, `chr_end` ASC) ,
  INDEX `fk_cnv_chromosome_idx_idx` (`chr_id` ASC) )
ENGINE = MyISAM;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
