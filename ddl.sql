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

create table treatment(
        s_id              char(9)         not null,
        t_name            varchar(15)     not null,
        p_ssn             char(9)         not null,
    foreign key (p_ssn) references patient(ssn),
    foreign key (s_id) references symptom(s_id)
) ;

create table symptom(
        s_id              char(9)             not null,
        s_name            char(9)             not null,

    primary key (id)

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

INSERT INTO symptom
(s_id, s_name)
values
('3324989', 'fever')
('1112894', 'cough')
('2910392', 'loss of smell')
('2103921', 'shortness of breath')
('3920493', 'bodyaches')
('3004583', 'runny nose')
('6549304', 'congestion')

INSERT INTO treatment
(s_id, t_name, p_ssn)
values
('3324989', 'tylenol', '888665555')
('1112894', 'cough syrup', '123456789')
('2910392', 'N/A', '453453453')
('2103921', 'inhaler', '453453453')
('3920493', 'advil', '666884444')
('3004583', 'nyquil', '987654321')
('6549304', 'musinex','888665555' )


