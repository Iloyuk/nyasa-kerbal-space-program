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
    GalaxyID INT PRIMARY KEY,
    GalaxyName VARCHAR(100) UNIQUE,
    Redshift DOUBLE,
    YearDiscovered date NOT NULL,
    SolarMassTrillions DOUBLE,
    DominantElement VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS StarSystem (
    SystemID INT PRIMARY KEY,
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
    ConstID INT PRIMARY KEY,
    ConstName VARCHAR(100) UNIQUE,
    Abbreviation VARCHAR(20) UNIQUE,
    Hemisphere ENUM('North', 'South') NOT NULL,
    BrightestStar VARCHAR(100) NOT NULL,
    BestViewingMonth ENUM('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') NOT NULL,
    Notes VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS Finding (
    FindingID INT PRIMARY KEY,
    Significance ENUM('Low', 'Medium', 'High') NOT NULL,
    FindingDate date NOT NULL,
    Notes VARCHAR(300) NOT NULL
);

CREATE TABLE IF NOT EXISTS Star (
    StarID INT PRIMARY KEY,
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
    PlanetID INT PRIMARY KEY,
    PlanetName VARCHAR(100) UNIQUE,
    PlanetType VARCHAR(50) NOT NULL,
    Mass INT,
    NumMoons INT,
    Eccentricity DOUBLE,
    Inclination DOUBLE
);

CREATE TABLE IF NOT EXISTS Spacecraft (
    ShipID INT PRIMARY KEY,
    ShipName VARCHAR(100) UNIQUE NOT NULL,
    Status ENUM('Under Construction', 'Operational', 'Decommissioned', 'Damaged') NOT NULL,
    Mass INT NOT NULL,
    Manufacturer VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Part (
    PartID INT PRIMARY KEY,
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
    MissionID INT PRIMARY KEY,
    MissionName VARCHAR(100) NOT NULL,
    Agency VARCHAR(30) NOT NULL,
    Objective VARCHAR(200) NOT NULL,
    SuccessRating ENUM('Low', 'Medium', 'High') NOT NULL
);

CREATE TABLE IF NOT EXISTS Astronaut (
    AstroID INT PRIMARY KEY,
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
INSERT INTO Galaxy (GalaxyID, GalaxyName, Redshift, YearDiscovered, SolarMassTrillions, DominantElement)
VALUES
(1, 'Milky Way', 0.0, '0001-01-01', 1, 'Hydrogen'),
(2, 'Andromeda', 0.001, '1923-10-05', 1, 'Hydrogen'),
(3, 'Triangulum', 0.0027, '1764-08-01', 0.5, 'Helium'),
(4, 'Whirlpool', 0.0016, '1773-03-13', 1, 'Hydrogen');

INSERT INTO Constellation (ConstID, ConstName, Abbreviation, Hemisphere, BrightestStar, BestViewingMonth, Notes)
VALUES
(1, 'Orion', 'Ori', 'South', 'Rigel', 'Jan', 'Features Orions Belt'),
(2, 'Cassiopeia', 'Cas', 'North', 'Schedar', 'Nov', 'W-shaped constellation'),
(3, 'Lyra', 'Lyr', 'North', 'Vega', 'Jul', 'Hosts Ring Nebula'),
(4, 'Crux', 'Cru', 'South', 'Acrux', 'May', 'Southern Cross'),
(5, 'Scorpius', 'Sco', 'South', 'Antares', 'Jul', 'Curved shape like a scorpion'),
(6, 'Ursa Major', 'UMa', 'North', 'Alioth', 'Apr', 'Includes the Big Dipper asterism'),
(7, 'Canis Major', 'CMa', 'South', 'Sirius', 'Feb', 'Home to the brightest star in the night sky'),
(8, 'Cygnus', 'Cyg', 'North', 'Deneb', 'Sep', 'Known as the Northern Cross'),
(9, 'Taurus', 'Tau', 'North', 'Aldebaran', 'Dec', 'Contains the Pleiades and Hyades clusters'),
(10, 'Leo', 'Leo', 'North', 'Regulus', 'Mar', 'Recognizable by a sickle-shaped head');

INSERT INTO StarSystem (SystemID, GalaxyID, SystemName, DistInLY, SystemType, NumStars)
VALUES
(1, 1, 'Alpha Centauri', 4, 'Multiple', 3),
(2, 2, 'Almach System', 350, 'Binary', 2),
(3, 3, 'M33-A1', 3000000, 'Binary', 2),
(4, 1, 'Solar System', 0, 'Multiple', 1),
(5, 1, 'Vega System', 25, 'Binary', 2),
(6, 1, 'Deneb System', 2600, 'Multiple', 3),
(7, 1, 'Altair System', 17, 'Binary', 2),
(8, 1, 'Sirius System', 8, 'Binary', 2),
(9, 1, 'Rigel System', 860, 'Multiple', 3),
(10, 1, 'Antares System', 550, 'Multiple', 2),
(11, 1, 'Pollux System', 34, 'Binary', 2);

INSERT INTO Star (StarID, SystemID, ConstID, StarName, Mass, Temperature, SpectralType)
VALUES
(1, 1, 1, 'Proxima Centauri', 123, 3042, 'M5'),
(2, 1, 1, 'Alpha Centauri A', 200, 5790, 'G2'),
(3, 2, 2, 'Almach A', 300, 8000, 'B9'),
(4, 4, 3, 'Sun', 1989000, 5778, 'G2'),
(5, 3, 4, 'Betelgeuse', 11800, 3500, 'M1'),
(6, 3, 4, 'Bellatrix', 8700, 22000, 'B2'),
(7, 5, 5, 'Vega', 2200, 9600, 'A0'),
(8, 6, 7, 'Deneb', 19000, 8525, 'A2'),
(9, 7, 7, 'Altair', 1800, 7550, 'A7'),
(10, 8, 8, 'Sirius A', 2040, 9940, 'A1'),
(11, 8, 8, 'Sirius B', 1020, 25200, 'DA'),
(12, 9, 1, 'Rigel', 21000, 12100, 'B8'),
(14, 11, 10, 'Pollux', 1900, 4865, 'K0'),
(21, 4, 2, 'Alioth', 6500, 9000, 'A1'),
(22, 10, 3, 'Antares', 15000, 3500, 'M1'),
(23, 4, 4, 'Schedar', 5000, 4500, 'K0'),
(24, 1, 5, 'Acrux', 18000, 25000, 'B0'),
(25, 6, 6, 'Regulus', 3200, 12460, 'B7'),
(26, 3, 8, 'Kaus Australis', 4200, 9440, 'B9'),
(27, 8, 9, 'Aldebaran', 1900, 3910, 'K5'),
(28, 1, 10, 'Alpha Centauri', 1100, 5790, 'G2');

INSERT INTO Planet (PlanetID, PlanetName, PlanetType, Mass, NumMoons, Eccentricity, Inclination)
VALUES
(1, 'Proxima b', 'Terrestrial', 1, 0, 0.05, 1.0),
(2, 'Alpha C b', 'Gas Giant', 317, 12, 0.04, 2.1),
(3, 'Earth', 'Terrestrial', 1, 1, 0.017, 0.0),
(4, 'Almach X1', 'Ice Giant', 100, 4, 0.07, 1.8);


INSERT INTO Orbits (PlanetID, StarID, OrbitalPeriod, SemiMajorAxis)
VALUES
(1, 1, 11.2, 0.05),
(2, 2, 370, 1.5),
(3, 4, 365.25, 1.0),
(4, 3, 800, 3.2);

INSERT INTO Spacecraft (ShipID, ShipName, Status, Mass, Manufacturer, Capacity)
VALUES
(1, 'Voyager X', 'Operational', 12000, 'SpaceTech Industries', 6),
(2, 'Pioneer Nova', 'Decommissioned', 9500, 'NovaWorks', 4),
(3, 'Aurora-3', 'Operational', 15000, 'AstroForge', 8),
(4, 'Eventide', 'Damaged', 18000, 'DeepSky Labs', 10);

INSERT INTO Part (PartID, ShipID, PartName, MassInTons, LengthInCM, PartUsage)
VALUES
(1, 1, 'Ion Thruster', 2, 300, 'Propulsion'),
(2, 1, 'Navigation Module', 1, 150, 'Guidance'),
(3, 2, 'Life Support Unit', 3, 400, 'Crew Sustainability'),
(4, 3, 'Energy Core', 5, 500, 'Power Supply');

INSERT INTO Astronaut (AstroID, Name, Country, YearsInSpace)
VALUES
(1, 'Elena Torres', 'Spain', 5),
(2, 'Kenji Watanabe', 'Japan', 8),
(3, 'Liam Chen', 'Canada', 6),
(4, 'Ava Singh', 'India', 7);

INSERT INTO SpacecraftAstronaut (ShipID, AstroID)
VALUES
(1, 1),
(1, 2),
(3, 3),
(4, 4);

INSERT INTO Mission (MissionID, MissionName, Agency, Objective, SuccessRating)
VALUES
(1, 'Centauri Scout', 'ESA', 'Survey Alpha Centauri', 'High'),
(2, 'Andromeda Path', 'NASA', 'Andromeda flyby', 'Medium'),
(3, 'Solar Flare Study', 'ISRO', 'Monitor solar storms', 'High'),
(4, 'Deep Dive', 'CSA', 'Explore Triangulum core', 'Low');

INSERT INTO MissionSpacecraft (MissionID, ShipID, MissionStatus)
VALUES
(1, 1, 'Complete'),
(2, 2, 'Planned'),
(3, 3, 'Ongoing'),
(4, 4, 'Planned');

INSERT INTO MissionAstronaut (MissionID, AstroID)
VALUES
(1, 1),
(1, 2),
(3, 3),
(4, 4);

INSERT INTO StarSystemMissions (SystemID, MissionID, StartDate, EndDate)
VALUES
(1, 1, '2021-04-01', '2022-12-20'),
(2, 2, '2025-01-01', NULL),
(4, 3, '2024-06-15', NULL),
(3, 4, '2025-02-20', NULL);

INSERT INTO Finding (FindingID, Significance, FindingDate, Notes)
VALUES
(1, 'High', '2022-11-01', 'Detected water vapor on Proxima b'),
(2, 'Medium', '2023-02-15', 'Radiation spikes near Almach A'),
(3, 'Low', '2024-01-03', 'Stable magnetic fields observed'),
(4, 'High', '2025-03-22', 'Possible microbial biosignatures on Almach X1');

INSERT INTO MissionFinding (MissionID, FindingID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);