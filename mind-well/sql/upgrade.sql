ALTER TABLE `mindwell_django`.'client_clientinfo' ADD `emailaddress` varchar(200) NOT NULL AFTER `workmessage`;
ALTER TABLE `mindwell_django`.`client_dos` DROP INDEX `dos_datetime`;