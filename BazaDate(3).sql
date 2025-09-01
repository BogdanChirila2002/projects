--schema curenta 
alter session set current_schema=prof;

drop table prof.emp cascade constraints;
--truncate table prof.emp;
create table prof.emp  --contine angajatii unei firme 
                     (empno    number(6,0)  constraint emp_empno_pk primary key,                      
                      firstname    varchar2(25), --prenume
                      lastname    varchar2(25) constraint emp_lastname_nn not null, --numne familie
                      cnp      varchar(13),
                      --gender   char(1)      constraint emp_gender_chk check(upper(gender) in ('m','f')),
                      --datan    date,
                      phone      varchar2(20),
                      email    char(50) constraint emp_email_nn not null,
                      adr      varchar2(60) default 'necunoscuta',
                      jobid    varchar2(10)  constraint emp_jobid_nn not null,
                      hiredate date         constraint emp_hiredate_nn not null,  --data angajarii pe postul actual
                      mgr      number(6,0), --cod manager
                      sal	     number(9,2), --check(sal>0)
                      comm     number(9,2), --comision
                      deptno   number(4,0)  --constraint	 emp_deptno_fk  --cheie straina
                                              --references prof.dept (deptno) --on delete cascade                      
                      --constraint emp_empno_pk primary key(empno),
                      --constraint emp_deptno_fk foreign key (deptno) references prof.dept(deptno)
                      );

--vizualizarea campurilor
describe prof.emp;


drop table prof.regions cascade constraints;
--truncate table prof.regions;
create table prof.regions 
                     (regionid number(4,0)   constraint regions_regionid_pk primary key,
                      region  varchar2(40) --denumirea regiunii
                      );

describe prof.regions;


drop table prof.countries cascade constraints;
--truncate table prof.countries;
create table prof.countries 
                     (countryid char(3)   constraint countries_countryid_pk primary key,
                      country  varchar2(40), --denumire
                      regionid   number(3,0)  constraint	 countries_regionid_fk  --cheie straina
                                              references prof.regions (regionid)
                      );


describe prof.countries;

drop table prof.locations cascade constraints;
--truncate table prof.locations;
create table prof.locations 
                     (locid             number(4,0)   constraint locations_locid_pk primary key,
                      street            varchar2(40),
                      postalcode       varchar2 (12),
                      city              varchar2(20)   constraint locations_city_nn not null,
                      stateprovince     varchar2(25) default 'bucharest', --judetul
                      countryid         char(3)  constraint	 locations_countryid_fk  --cheie straina
                                              references prof.countries (countryid)
                      );


describe prof.locations;

drop table prof.dept cascade constraints;
--truncate table prof.dept;
create table prof.dept --descrie departamentele din care fac parte angaja?ii
                     (deptno number(4,0)   constraint dept_deptno_pk primary key,
                      dname  varchar2(40)  constraint dept_dname_uk unique,                     
                      locid  number(4,0)  constraint	 dept_locid_fk  --cheie straina
                                              references prof.locations(locid) --on delete cascade 
                      --,constraint dept_deptno_pk primary key(deptno)
                      );

--vizualizarea campurilor
describe prof.dept;



drop table prof.jobs cascade constraints;
--truncate table prof.jobs;
create table prof.jobs 
                     (jobid varchar2(10)  constraint jobs_jobid_pk primary key,
                      job  varchar2(40) constraint jobs_job_nn not null, --denumire job
                      minsal   number(9,2),
                      maxsal   number(9,2)   
                      );


describe prof.jobs;


drop table prof.jobgrades;
--truncate table prof.jobgrades;
create table prof.jobgrades 
                     (gradelevel varchar2(3),
                      lowestsal  number(9,2),
                      highestsal  number(9,2)
                      );


describe prof.jobgrades;


drop table prof.jobhistory cascade constraints;
--truncate table prof.jobhistory;
create table prof.jobhistory 
                     (empno number(6,0) constraint jobhistory_empno_fk 
                                        references prof.emp(empno) 
                                        constraint jobhistory_empno_nn not null,   
                      startdate  date constraint jobhistory_startdate_nn not null,
                      enddate   date constraint jobhistory_enddate_nn not null,
                      jobid   varchar2(10) constraint jobhistory_jobid_fk 
                                            references prof.jobs(jobid) 
                                            constraint jobhistory_jobid_nn not null,
                      deptno  number(4,0)  constraint jobhistory_deptno_fk 
                                            references prof.dept(deptno)
                      );


describe prof.jobhistory;


/*
alter table emp 
add constraint emp_mgr_fk foreign key(mgr) 
references prof.emp(empno);
*/

alter table emp 
add constraint emp_deptno_fk foreign key(deptno) 
references prof.dept(deptno);

alter table emp
add constraint emp_jobid_fk foreign key(jobid) 
references prof.jobs(jobid);

describe prof.emp;
/*
alter table emp disable constraint emp_deptno_fk cascade;
alter table emp disable constraint emp_jobid_fk cascade;

alter table emp enable constraint emp_deptno_fk ;
alter table emp enable constraint emp_jobid_fk;
*/
/*
create table bonus(
  ename varchar2(10),
  job   varchar2(9),
  sal   number,
  comm  number
);
 
create table salgrade(
  grade number,
  losal number,
  hisal number
);

*/


/*--inserarea datelor
insert into salgrade values (1, 700, 1200);
insert into salgrade values (2, 1201, 1400);
insert into salgrade values (3, 1401, 2000);
insert into salgrade values (4, 2001, 3000);
insert into salgrade values (5, 3001, 9999);
*/



--dml (data manipulation language): insert, update, delete
/* 
insert into nume_tabel_sau_vizualizare[(lista_de_coloane)]
values (lista_de_valori);

inserarea unui rand folosind randuri dintr-un alt tabel:
insert into nume_tabel/nume_view [(col1[, col2[,…]])]
values (expresia1[, expresia2[,…]]) / subcerere;


insert into dept (deptno,dname)
(select deptno,initcap(dname)
from old_dept);
*/

--job_grade data
insert into jobgrades values('a',1000,2999);
insert into jobgrades values('b',3000,5999);
insert into jobgrades values('c',6000,9999);
insert into jobgrades values('d',10000,14999);
insert into jobgrades values('e',15000,24999);
insert into jobgrades values('f',25000,40000);

--vizualizarea datelor din tabel
select * from jobgrades;

--job data
insert into jobs values('ad_pres' , 'president',2000,40000);
insert into jobs values('ad_vp' , 'adminstration vice president',15000,30000);
insert into jobs values('ad_asst' , 'adminstration assistant',3000,6000);
insert into jobs values('ac_mgr' , 'accounting manager',8200,16000);
insert into jobs values('ac_account', 'public accountant',4200,9000);
insert into jobs values('sa_man' , 'sales manager',10000,20000);
insert into jobs values('sa_rep' , 'sales representative',6000,12000);
insert into jobs values('st_man' , 'stock manager',5500,8500);
insert into jobs values('st_clerk' , 'stock clerk',2000,5000);
insert into jobs values('it_prog' , 'programmer',400,10000);
insert into jobs values('mk_man' , 'marketing manager',9000,15000);
insert into jobs values('mk_rep' , 'marketing representative',4000,9000);

--vizualizarea datelor din tabel
select * from jobs;


--region data
insert into regions values (1,'europe');
insert into regions values (2,'america');
insert into regions values (3,'asia');
insert into regions values (4,'middle east amd africa');

--vizualizarea datelor din tabel
select * from regions;

--countries data
insert into countries values('ca','canada',2);
insert into countries values('de','germany',1);
insert into countries values('uk','united kingdom',1);
insert into countries values('us','united states of america',2);
insert into countries values('ro','roumania',1);
--vizualizarea datelor din tabel
select * from countries;


--location data
insert into locations values(1,'2014 jabberwocky rd','26192','southlake','texas','us');
insert into locations values(2,'2011 interiors blvd','99236','south san francisco','califorina','us');
insert into locations values(3,'2004 charade rd','99236','seattle','washington','us');
insert into locations values(4,'460 bloor st. w.','on m5s 1xb','toronto','ontario','ca');
insert into locations values(5,'magdalen center,the oxford science park','ox9 9zb','oxford','oxford','uk');
--sau
insert into prof.locations (locid,street,postalcode,city,stateprovince, countryid) values(7,'ghica 13','o71','bucharest','bucharest','ro');
--sau
insert into prof.locations (locid,street,postalcode,city, countryid) values(6,'fabricii 46g','o73','bucharest','ro');
describe prof.locations;

--vizualizarea datelor din tabel
select * from locations;

--departments data
insert into dept values(10,'adminstration',1);
insert into dept values(20,'marketing',2);
insert into dept values(30,'shipping',3);
insert into dept values(40,'it',1);
insert into dept values(50,'sales',4);
insert into dept values(60,'executive',5);
insert into dept values(70,'accouting',2);
insert into dept values(80,'contracting',4);

--vizualizarea datelor din tabel
select * from dept;
/*
--sau
insert into	dept(deptno, dname, locid) values (100,'financiar-contabil',1);          

-- sau
/*inserare de valori folosind variabile de substitutie - ampersand unic  (&)
enter value for department_id: 120
enter value for department_name: oracle
enter value for location: 1
insert into	dept(deptno, dname, locid) values (&department_id, '&department_name',&location);
*/

/*crearea unui script pentru manipularea datelor
prin intermediul comenzii sql*plus accept, mesajele afisate la cererea introducerii 
valorilor pot fi modificate. 
•	accept	- memoreaza valoarea intr-o variabila;
•	prompt	- afiseaza textul specificat.
*/

/*
accept deptno prompt 'introduceti codul departamentului:'
accept dname prompt 'introduceti denumirea departamentului:'
accept dname prompt 'introduceti codul localitatii:'
insert into dept (deptno, dname, locid) values (&deptno, '&dname', &locid);
select * from dept;

--sa se adauge in tabela dept datele pentru noul departament (cu date introduse de la tastatura). 
prompt sa se adauge in dept datele pentru: 
insert into dept (deptno, dname,locid) values(&deptno,'&dname',&locid); 
select* from dept;
*/


--inserarea unor valori specifice de tip data calendaristica: to_date('3-02-1997','dd-mm-yyyy')
insert into emp values( 7839, 'kinga', 'r','1461110222233', '0757000000','n.iacob.mi@gmail.com','bucuresti', 'ad_pres',to_date('25-07-1998','dd-mm-yyyy'),null, 1500, 300, 10);
insert into emp values( 7698, 'blake', 'b', '1871121222283', '0757002000','defta.mi@spiruharet.ro','craiova','ad_vp',to_date('28-10-1993','dd-mm-yyyy'),null, 1585, null, 30);
insert into emp values( 7782, 'clark', 'b', '2501207222233', '0262000000','n.iacob.mi@spiruharet.ro','bucuresti','ad_asst', to_date('27-10-1993','dd-mm-yyyy'),null, 5450, 100, 40);
insert into emp values( 7566, 'jones','d', '1671111222233', '0757330000','iacob.mi@yahoo.com','bucuresti','ac_mgr',to_date('15-03-1997','dd-mm-yyyy'), null,  12850, null, 20);
insert into emp values( 7788, 'scott','m', '1930807222233', '0757009900','n.mi@spiruharet.ro','constanta','ac_account', to_date('15-03-1997','dd-mm-yyyy'),7566, 8000, null, 20);
insert into emp values( 7902, 'adams','a', '1881019222233',  '0757000000','n.iacob.mi@yahoo.com','craiova','sa_man', to_date('15-03-1997','dd-mm-yyyy'),7566, 75000, null, 20);
insert into emp values( 7369, 'smith','i', '1941107222233',  '0757000880','t.iacob@spiruharet.ro','bucuresti','sa_rep', to_date('31-12-1998','dd-mm-yyyy'),7782, 1400, null, 20);
insert into emp values( 7499, 'allen','a', '2921112222233', '0757000000','n.iacob.mi@gmail.com','constanta','st_man', to_date('31-12-1998','dd-mm-yyyy'),7698, 5600, 30, 30);
insert into emp values( 7521, 'james','m', '1860214222233',  '0757000050','l.defta.mi@spiruharet.ro','bucuresti','st_clerk',to_date('31-12-1999','dd-mm-yyyy'), 7698, 2250, 15, 30);
insert into emp values( 7654, 'martin','t','1991108222233',  '0262000000','m.iacob@spiruharet.ro','bucuresti','it_prog',to_date('18-06-1993','dd-mm-yyyy'), 7698, 9250, 10, 30);
insert into emp values( 7844, 'turner','v','2660117222233',  '0757000000','m.iacob.mi@yahoo.com','craiova','mk_man',to_date('17-06-1993','dd-mm-yyyy'), 7698, 9500, null, 30);
insert into emp values( 7876, 'adams','n', '1111218222233',  '0757001111','n.defta@gmail.com','constanta','mk_rep', to_date('31-12-1998','dd-mm-yyyy'),7788,  4800, null, 20);
insert into emp values( 7900, 'james','b', '1681117222233',  '0757022000','n.iacob@spiruharet.ro','bucuresti','mk_rep',to_date('30-12-1998','dd-mm-yyyy'), 7839,  8950, 2000, 30);
insert into emp values( 7934, 'miller','m', '2991212222233', '0262000000','iacob@yahoo.com','bucuresti', 'mk_rep', to_date('30-11-1998','dd-mm-yyyy'),7782,  8300, null, 40);

--vizualizarea datelor din tabel
select * from emp;


--job_history data
--to_date('21-11-1987','dd-mm-yyyy')
insert into jobhistory values (7839,to_date('13-01-1993','dd-mm-yyyy'),to_date('24-07-1998','dd-mm-yyyy'),'it_prog',10);
insert into jobhistory values (7698,to_date('21-09-1989','dd-mm-yyyy'),to_date('27-10-1993','dd-mm-yyyy'),'ac_account',30);
insert into jobhistory values (7566,to_date('28-10-1993','dd-mm-yyyy'),to_date('15-03-1997','dd-mm-yyyy'),'ac_mgr',10);
insert into jobhistory values (7934,to_date('17-02-1996','dd-mm-yyyy'),to_date('19-12-1999','dd-mm-yyyy'),'mk_rep',20);
insert into jobhistory values (7900,to_date('24-03-1998','dd-mm-yyyy'),to_date('30-12-1999','dd-mm-yyyy'),'st_clerk',50);
insert into jobhistory values (7521,to_date('01-01-1999','dd-mm-yyyy'),to_date('30-12-1999','dd-mm-yyyy'),'st_clerk',50);
insert into jobhistory values (7654,to_date('17-09-1987','dd-mm-yyyy'),to_date('17-06-1993','dd-mm-yyyy'),'ad_asst',20);
insert into jobhistory values (7499,to_date('24-03-1998','dd-mm-yyyy'),to_date('30-12-1998','dd-mm-yyyy'),'sa_rep',50);
insert into jobhistory values (7876,to_date('01-01-1999','dd-mm-yyyy'),to_date('30-12-1998','dd-mm-yyyy'),'sa_man',40);
insert into jobhistory values (7369,to_date('01-07-1994','dd-mm-yyyy'),to_date('30-12-1998','dd-mm-yyyy'),'ac_account',60);

--vizualizarea datelor din tabel
select * from jobhistory;