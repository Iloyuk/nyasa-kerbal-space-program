CREATE DATABASE IF NOT EXISTS NYASA;
USE NYASA;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Galaxy;
DROP TABLE IF EXISTS StarSystem;
DROP TABLE IF EXISTS Star;
DROP TABLE IF EXISTS Constellation;
DROP TABLE IF EXISTS StarSystemMissions;
DROP TABLE IF EXISTS Mission;
DROP TABLE IF EXISTS MissionSpacecraft;
DROP TABLE IF EXISTS Spacecraft;
DROP TABLE IF EXISTS MissionAstronaut;
DROP TABLE IF EXISTS SpacecraftAstronaut;
DROP TABLE IF EXISTS Part;
DROP TABLE IF EXISTS MissionFinding;
DROP TABLE IF EXISTS Finding;
DROP TABLE IF EXISTS Planet;
DROP TABLE IF EXISTS Orbits;
DROP TABLE IF EXISTS Astronaut;

SET FOREIGN_KEY_CHECKS = 1;

/*
 Create tables
 */
CREATE TABLE IF NOT EXISTS Galaxy (
    GalaxyID INT PRIMARY KEY AUTO_INCREMENT,
    GalaxyName VARCHAR(100) UNIQUE,
    Redshift DOUBLE,
    YearDiscovered date NOT NULL,
    SolarMassTrillions DOUBLE,
    DominantElement VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS StarSystem (
    SystemID INT PRIMARY KEY AUTO_INCREMENT,
    GalaxyID INT NOT NULL,
    SystemName VARCHAR(100) UNIQUE,
    DistInLY INT NOT NULL,
    SystemType ENUM('Binary','Multiple') NOT NULL,
    NumStars INT NOT NULL,
    FOREIGN KEY (GalaxyID) REFERENCES Galaxy(GalaxyID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Constellation (
    ConstID INT PRIMARY KEY AUTO_INCREMENT,
    ConstName VARCHAR(100) UNIQUE,
    Abbreviation VARCHAR(20) UNIQUE,
    Hemisphere ENUM('North', 'South') NOT NULL,
    BrightestStar VARCHAR(100) NOT NULL,
    BestViewingMonth ENUM('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') NOT NULL,
    Notes VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS Finding (
    FindingID INT PRIMARY KEY AUTO_INCREMENT,
    Significance ENUM('Low', 'Medium', 'High') NOT NULL,
    FindingDate date NOT NULL,
    Notes VARCHAR(300) NOT NULL
);

CREATE TABLE IF NOT EXISTS Star (
    StarID INT PRIMARY KEY AUTO_INCREMENT,
    SystemID INT NOT NULL,
    ConstID INT NOT NULL,
    StarName VARCHAR(100) UNIQUE,
    Mass INT,
    Temperature INT,
    SpectralType VARCHAR(3) NOT NULL,
    FOREIGN KEY (SystemID) REFERENCES StarSystem(SystemID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (ConstID) REFERENCES Constellation(ConstID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Planet (
    PlanetID INT PRIMARY KEY AUTO_INCREMENT,
    PlanetName VARCHAR(100) UNIQUE,
    PlanetType VARCHAR(50) NOT NULL,
    Mass INT,
    NumMoons INT,
    Eccentricity DOUBLE,
    Inclination DOUBLE
);

CREATE TABLE IF NOT EXISTS Spacecraft (
    ShipID INT PRIMARY KEY AUTO_INCREMENT,
    ShipName VARCHAR(100) UNIQUE NOT NULL,
    Status ENUM('Under Construction', 'Operational', 'Decommissioned', 'Damaged') NOT NULL,
    Mass INT NOT NULL,
    Manufacturer VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Part (
    PartID INT PRIMARY KEY AUTO_INCREMENT,
    ShipID INT NOT NULL,
    PartName VARCHAR(75) NOT NULL,
    MassInTons INT NOT NULL,
    LengthInCM INT NOT NULL,
    PartUsage VARCHAR(100) NOT NULL,
    FOREIGN KEY (ShipID) REFERENCES Spacecraft(ShipID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Mission (
    MissionID INT PRIMARY KEY AUTO_INCREMENT,
    MissionName VARCHAR(100) NOT NULL,
    Agency VARCHAR(30) NOT NULL,
    Objective VARCHAR(200) NOT NULL,
    SuccessRating ENUM('Low', 'Medium', 'High') NOT NULL
);

CREATE TABLE IF NOT EXISTS Astronaut (
    AstroID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    YearsInSpace INT NOT NULL
);

CREATE TABLE IF NOT EXISTS MissionSpacecraft (
    MissionID INT,
    ShipID INT,
    MissionStatus ENUM('Planned', 'Ongoing', 'Complete') NOT NULL,
    PRIMARY KEY (MissionID, ShipID),
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (ShipID) REFERENCES Spacecraft(ShipID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MissionAstronaut (
    MissionID INT,
    AstroID INT,
    PRIMARY KEY (MissionID, AstroID),
    FOREIGN KEY(MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY(AstroID) REFERENCES Astronaut(AstroID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MissionFinding(
    MissionID INT,
    FindingID INT,
    PRIMARY KEY (MissionID, FindingID),
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (FindingID) REFERENCES Finding(FindingID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS StarSystemMissions (
    SystemID INT,
    MissionID INT,
    StartDate date NOT NULL,
    EndDate date,
    PRIMARY KEY (SystemID, MissionID),
    FOREIGN KEY (SystemID) REFERENCES StarSystem(SystemID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SpacecraftAstronaut (
    ShipID INT,
    AstroID INT,
    PRIMARY KEY (ShipID, AstroID),
    FOREIGN KEY(ShipID) REFERENCES Spacecraft(ShipID),
    FOREIGN KEY(AstroID) REFERENCES Astronaut(AstroID)
);

CREATE TABLE IF NOT EXISTS Orbits (
    PlanetID INT NOT NULL,
    StarID INT NOT NULL,
    OrbitalPeriod DOUBLE NOT NULL,
    SemiMajorAxis DOUBLE NOT NULL,
    PRIMARY KEY (PlanetID, StarID),
    FOREIGN KEY (PlanetID) REFERENCES Planet(PlanetID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (StarID) REFERENCES Star(StarID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


/*
 Insert data into tables
 */
-- GALAXY
INSERT INTO Galaxy (GalaxyName, Redshift, YearDiscovered, SolarMassTrillions, DominantElement)
VALUES 
('Milky Way', 0.0, '1610-01-01', 1.5, 'Hydrogen'),
('Andromeda', -0.001001, '0964-01-01', 1.23, 'Hydrogen'),
('Triangulum', 0.00096, '1764-01-01', 0.5, 'Helium');

-- STAR SYSTEM
INSERT INTO StarSystem (GalaxyID, SystemName, DistInLY, SystemType, NumStars)
VALUES
(1, 'Barnards Star System', 5, 'Binary', 1),
(1, 'Sirius System', 8, 'Binary', 2),
(2, 'M31 System Y', 2540001, 'Multiple', 3),
(3, 'M33-Kepler System', 2730000, 'Binary', 2);

-- CONSTELLATION
INSERT INTO Constellation (ConstName, Abbreviation, Hemisphere, BrightestStar, BestViewingMonth, Notes)
VALUES 
('Orion', 'Ori', 'North', 'Rigel', 'Jan', 'Contains the Orion Nebula'),
('Centaurus', 'Cen', 'South', 'Alpha Centauri', 'May', 'Home to the closest star system'),
('Cassiopeia', 'Cas', 'North', 'Schedar', 'Nov', 'Visible year-round in the Northern Hemisphere');

-- STAR
INSERT INTO Star (SystemID, ConstID, StarName, Mass, Temperature, SpectralType)
VALUES 
(1, 1, 'Sun', 1989000, 5778, 'G2V'),
(2, 2, 'Alpha Centauri A', 1100000, 5790, 'G2V'),
(2, 2, 'Alpha Centauri B', 907000, 5260, 'K1V'),
(2, 2, 'Proxima Centauri', 123000, 3042, 'M5V'),
(4, 2, 'Barnards Star', 144000, 3134, 'M4V'),
(5, 2, 'Sirius A', 2040000, 9940, 'A1V'),
(5, 2, 'Sirius B', 98000, 25200, 'DA2'),
(6, 3, 'M31-Y Alpha', 1800000, 7300, 'F5V'),
(6, 3, 'M31-Y Beta', 1600000, 6200, 'G0V'),
(6, 3, 'M31-Y Gamma', 1450000, 5900, 'G5V'),
(7, 1, 'Kepler-M33 A', 1200000, 5500, 'G2V'),
(7, 1, 'Kepler-M33 B', 1050000, 5100, 'K2V'),
(8, 3, 'M87-Core A', 3500000, 7000, 'F0V'),
(8, 3, 'M87-Core B', 3200000, 6500, 'F2V'),
(9, 1, 'Spiral Alpha', 2800000, 5900, 'G0V'),
(9, 1, 'Spiral Beta', 2600000, 5700, 'G5V'),
(9, 1, 'Spiral Gamma', 2400000, 5400, 'K0V'),
(10, 2, 'Sombrero-A', 3100000, 7700, 'A0V'),
(10, 2, 'Sombrero-B', 3000000, 7300, 'F5V');
-- PLANET
INSERT INTO Planet (PlanetName, PlanetType, Mass, NumMoons, Eccentricity, Inclination)
VALUES 
('Earth', 'Terrestrial', 5972, 1, 0.0167, 0.00005),
('Mars', 'Terrestrial', 641, 2, 0.0934, 1.850),
('Proxima b', 'Exoplanet', 1080, 0, 0.05, 0.0),
('Spiral-1b', 'Gas Giant', 19000, 16, 0.04, 2.3),
('Sombrero Prime', 'Rocky', 8500, 2, 0.08, 5.2),
('M87-ExoA', 'Ice Giant', 14800, 5, 0.1, 3.5);

-- ORBITS
INSERT INTO Orbits (PlanetID, StarID, OrbitalPeriod, SemiMajorAxis)
VALUES 
(1, 1, 365.25, 1.0),
(2, 1, 687, 1.52),
(3, 4, 11.2, 0.05),
(4, 6, 430, 0.9),
(5, 10, 380, 1.1),
(6, 7, 700, 2.2);

-- SPACECRAFT
INSERT INTO Spacecraft (ShipName, Status, Mass, Manufacturer, Capacity)
VALUES 
('Voyager I', 'Operational', 721, 'NASA', 0),
('Perseverance Rover', 'Operational', 1025, 'JPL', 0),
('Orion Crew Module', 'Operational', 26000, 'Lockheed Martin', 6),
('Kepler Explorer', 'Operational', 1400, 'NASA', 0),
('BlackHole Probe', 'Under Construction', 900, 'ESA', 0),
('Cosmic Cruiser', 'Operational', 34000, 'SpaceX', 8);

-- PART
INSERT INTO Part (ShipID, PartName, MassInTons, LengthInCM, PartUsage)
VALUES 
(1, 'Antenna Assembly', 0.3, 500, 'Deep Space Communication'),
(2, 'Sampling Arm', 0.1, 220, 'Soil Collection'),
(3, 'Life Support Module', 2, 800, 'Crew Sustenance'),
(4, 'Telescope Array', 0.2, 300, 'Exoplanet Observation'),
(5, 'Gravity Scanner', 0.5, 250, 'Black Hole Measurement'),
(6, 'Habitat Module', 5, 950, 'Crew Living Quarters');

-- MISSION
INSERT INTO Mission (MissionName, Agency, Objective, SuccessRating)
VALUES 
('Voyager Interstellar Mission', 'NASA', 'Study outer solar system and interstellar space', 'High'),
('Mars 2020', 'NASA', 'Search for signs of ancient life on Mars', 'High'),
('Artemis I', 'NASA', 'Uncrewed lunar orbit mission to test Orion', 'Medium'),
('Kepler-Deep Search', 'NASA', 'Detect Earth-like planets in distant systems', 'High'),
('EventHorizon Chase', 'ESA', 'Map regions near supermassive black holes', 'Medium'),
('Stellar Drift', 'SpaceX', 'Crewed deep space test of long-range ship', 'High');

-- ASTRONAUT
INSERT INTO Astronaut (Name, Country, YearsInSpace)
VALUES 
('Neil Armstrong', 'USA', 2),
('Yuri Gagarin', 'Russia', 1),
('Christina Koch', 'USA', 3),
('Mae Jemison', 'USA', 1),
('Valentina Tereshkova', 'Russia', 2),
('Luca Parmitano', 'Italy', 2);

-- MISSION SPACECRAFT
INSERT INTO MissionSpacecraft (MissionID, ShipID, MissionStatus)
VALUES 
(1, 1, 'Complete'),  -- Voyager I
(2, 2, 'Complete'),  -- Perseverance
(3, 3, 'Complete'),  -- Orion
(4, 4, 'Complete'),
(5, 5, 'Ongoing'),
(6, 6, 'Planned');

-- MISSION ASTRONAUT
INSERT INTO MissionAstronaut (MissionID, AstroID)
VALUES 
(1, 1),  -- Neil Armstrong
(2, 3),  -- Christina Koch
(3, 1),  -- Neil Armstrong
(3, 3),  -- Christina Koch
(6, 4),
(6, 6);

-- FINDINGS
INSERT INTO Finding (Significance, FindingDate, Notes)
VALUES 
('High', '1979-01-01', 'Discovered edge of heliosphere via Voyager I'),
('Medium', '2021-02-18', 'Confirmed signs of ancient habitable environment on Mars'),
('Medium', '2022-11-26', 'Orion capsule successfully returned from lunar orbit'),
('High', '2014-02-26', 'Discovered 715 new planets via Kepler'),
('High', '2019-04-10', 'Captured image of a black hole by Event Horizon Telescope'),
('Medium', '2025-03-01', 'Tested long-duration life support in deep space');

-- MISSION FINDING
INSERT INTO MissionFinding (MissionID, FindingID)
VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6);

-- STAR SYSTEM MISSIONS
INSERT INTO StarSystemMissions (SystemID, MissionID, StartDate, EndDate)
VALUES 
(1, 1, '1977-09-05', '2025-01-01'),
(1, 2, '2020-07-30', '2021-02-18'),
(1, 3, '2022-11-16', '2022-12-11'),
(7, 4, '2012-03-07', '2014-02-26'),
(8, 5, '2022-01-01', NULL),
(9, 6, '2025-01-01', NULL);

-- SPACECRAFT ASTRONAUT
INSERT INTO SpacecraftAstronaut (ShipID, AstroID)
VALUES 
(3, 1),  -- Orion: Neil Armstrong
(3, 3),  -- Orion: Christina Koch
(6, 4),
(6, 6);