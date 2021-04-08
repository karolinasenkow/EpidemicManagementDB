CREATE DATABASE EpidemicManagementSystem;
create table patient(
        fname             varchar(15)         not null,
        lname             varchar(15)         not null,
        ssn               char(9)             not null,
        dob               DATE                not null,
        address           varchar(30), 
        sex               char, 
    primary key (ssn)
) ;

create table laboratory(
        id                char(9)         not null,
        name              varchar(15)     not null,
        location          varchar(30)     not null,
    primary key (id)
) ;

create table test(
        id                char(9)             not null,
        date              DATE                not null,
        result            varchar(10)         not null,
        p_ssn             char(9)             not null,
        lab_id            char(9)             not null,
    primary key (id),
    foreign key (p_ssn) references patient(ssn),
    foreign key (lab_id) references laboratory(id)
) ;

create table strain(
        strain_id                char(9)         not null,
        strainname               varchar(30)     not null,
    primary key (strain_id)
) ;

create table had(
        strainid                char(9)             not null,
        patientid               char(9)             not null,
    	duration		varchar(10)	    not null,
    	dateofdiseasestart	DATE		    not null,
    foreign key (strainid) REFERENCES strain(strain_id),
    foreign key (patientid) REFERENCES patient(ssn)
) ;

INSERT INTO patient
(fname, lname, ssn, dob, address, sex)
values
('James','Borg', '888665555', '1937-11-10', '450 Stone, Houston TX', 'M'),
('John', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston TX', 'M'),
('Franklin', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston TX', 'M'),
('Alicia', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring TX', 'F'),
('Jennifer', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire TX', 'F'),
('Ramesh', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble TX', 'M'),
('Joyce', 'English', '453453453', '1972-07-31', '5631 Rice, Houston TX', 'F'),
('Ahmad', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston TX', 'M');

INSERT INTO laboratory
(id, name, location)
values
('365196362', 'BioLab', 'Chicago, IL'),
('532930356', 'GenTech', 'New York City, NY'),
('543289700', 'TestCenter', 'San Francisco, CA');

INSERT INTO test
(id, date, result, p_ssn, lab_id)
values
('409585845', '2020-04-05', 'positive', '888665555', '365196362'),
('318372437', '2020-10-25', 'positive', '333445555', '532930356'),
('314123624', '2020-05-03', 'negative', '123456789', '365196362'),
('660644747', '2020-02-28', 'positive', '888665555', '543289700'),
('850846702', '2020-01-04', 'negative', '987654321', '543289700'),
('783472635', '2020-12-30', 'negative', '453453453', '365196362'),
('337518761', '2020-05-05', 'negative', '666884444', '532930356');

INSERT INTO strain
(strain_id, strainname)
values
('836495021', 'SARS-CoV-2'),
('643281380', 'SARS-CoV'),
('928471742', 'MERS-CoV');


INSERT INTO had
(strainid, patientid, duration, dateofdiseasestart)
values
('836495021', '888665555', '3 days', '03/29/2021'),
('643281380','333445555',  '5 days', '03/27/2021'), 
('928471742', '888665555', '3 days', '03/29/2021');
