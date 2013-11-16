BEGIN;
CREATE TABLE `Client_clientinfo` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `create_time` datetime NOT NULL,
    `lastname` varchar(200) NOT NULL,
    `firstname` varchar(200) NOT NULL,
    `cellnumber` varchar(200) NOT NULL,
    `cellmessage` varchar(200) NOT NULL,
    `homenumber` varchar(200) NOT NULL,
    `homemessage` varchar(200) NOT NULL,
    `worknumber` varchar(200) NOT NULL,
    `workmessage` varchar(200) NOT NULL,
    `emailaddress` varchar(200) NOT NULL,
    `address` varchar(200) NOT NULL,
    `address2` varchar(200) NOT NULL,
    `city` varchar(200) NOT NULL,
    `state` varchar(200) NOT NULL,
    `zipcode` varchar(200) NOT NULL,
    `dob_month` varchar(200) NOT NULL,
    `dob_day` varchar(200) NOT NULL,
    `dob_year` varchar(200) NOT NULL,
    `referrer` varchar(200) NOT NULL,
    `client_status` varchar(200) NOT NULL
)
;
CREATE TABLE `Client_dos` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `clientinfo_id` integer NOT NULL,
    `session_type` varchar(200) NOT NULL,
    `session_result` varchar(200) NOT NULL,
    `dsm_code` varchar(200) NOT NULL,
    `type_pay` varchar(200) NOT NULL,
    `amt_due` varchar(200) NOT NULL,
    `amt_paid` varchar(200) NOT NULL,
    `note` varchar(200) NOT NULL,
    `dos_datetime` datetime,
    `dos_duration` varchar(200) NOT NULL,
    `dos_repeat` varchar(200) NOT NULL
)
;
ALTER TABLE `Client_dos` ADD CONSTRAINT `clientinfo_id_refs_id_61277225` FOREIGN KEY (`clientinfo_id`) REFERENCES `Client_clientinfo` (`id`);
CREATE TABLE `Client_dosrecurr` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `dos_base_id` integer NOT NULL,
    `dos_recurr_datetime` datetime UNIQUE,
    `dos_cancel` varchar(200) NOT NULL
)
;
ALTER TABLE `Client_dosrecurr` ADD CONSTRAINT `dos_base_id_refs_id_513cb996` FOREIGN KEY (`dos_base_id`) REFERENCES `Client_dos` (`id`);
CREATE TABLE `Client_invoice` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `clientinfo_id` integer NOT NULL,
    `invoice_date` date NOT NULL,
    `start_date` date NOT NULL,
    `end_date` date NOT NULL
)
;
ALTER TABLE `Client_invoice` ADD CONSTRAINT `clientinfo_id_refs_id_307b8ab4` FOREIGN KEY (`clientinfo_id`) REFERENCES `Client_clientinfo` (`id`);
COMMIT;
