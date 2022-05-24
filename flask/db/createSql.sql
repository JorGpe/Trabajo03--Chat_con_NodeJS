CREATE TABLE IF NOT EXISTS `mydb`.`people` (
  `idpeople` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(70) NULL DEFAULT 'anonimo',
  `edad` INT NULL,
  `colorFav` VARCHAR(20) ,
  `genero` VARCHAR(50) ,
  `email` VARCHAR(50) ,
  `pronombre` ENUM('el', 'ella', ' ') NOT NULL,
  PRIMARY KEY (`idpeople`),
  UNIQUE INDEX `idpeople_UNIQUE` (`idpeople` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  INDEX `fk_people_mail_idx` (`email` ASC) VISIBLE
    )
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `mydb`.`questionnaire` (
  `idquestionnaire` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(70) ,
  `descripcion` VARCHAR(150) ,
  PRIMARY KEY (`idquestionnaire`)
    )
ENGINE = InnoDB;

INSERT INTO `mydb`.`questionnaire` (`nombre`,`descripcion`) values ('HEALTHY MIND', 'Test para la depresión') ;

CREATE TABLE IF NOT EXISTS `mydb`.`result` (
  `idresultado` INT NOT NULL AUTO_INCREMENT,
  `idpeople` INT NOT NULL,
  `idquestionnaire` INT NOT NULL,
  `testResultado` VARCHAR(100) NULL DEFAULT 'incompleto',
  PRIMARY KEY (`idresultado`,`idpeople`,`idquestionnaire`),
  CONSTRAINT `fk_result_people`
    FOREIGN KEY (`idpeople`)
    REFERENCES `mydb`.`people` (`idpeople`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_result_questionnaire`
    FOREIGN KEY (`idquestionnaire`)
    REFERENCES `mydb`.`questionnaire` (`idquestionnaire`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
  )
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `mydb`.`response` (
  `idpeople` INT NOT NULL,
  `idquestionnaire` INT NOT NULL,
  `idresultado` INT NOT NULL,
  `idrespuesta` INT NOT NULL,
  `respuesta` VARCHAR(45) NULL,
  PRIMARY KEY (`idresultado`,`idpeople`,`idquestionnaire`, `idrespuesta`),
  CONSTRAINT `fk_response_people`
    FOREIGN KEY (`idpeople`)
    REFERENCES `mydb`.`people` (`idpeople`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_response_questionnaire`
    FOREIGN KEY (`idquestionnaire`)
    REFERENCES `mydb`.`questionnaire` (`idquestionnaire`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_response_response`
    FOREIGN KEY (`idresultado`)
    REFERENCES `mydb`.`result` (`idresultado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
  )
ENGINE = InnoDB;