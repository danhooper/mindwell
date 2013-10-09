import sys
#copy the backup of the DB here
client_list = (
 (1,'2010-03-15 14:25:25','test','test','','MsgNOK','','MsgNOK','','MsgNOK','test@test','','','','Maryland','','','','','','Active'),
 (2,'2010-03-15 14:30:13','inactive','inactive','','MsgNOK','','MsgNOK','','MsgNOK','','','','','Maryland','','','','','','Inactive'),
 (3,'2010-04-05 11:46:00','abc','abc','','MsgNOK','','MsgNOK','','MsgNOK','abc@abc','','','','Maryland','','','','','','Active')
)
client_column_order = ('key','create_time','lastname','firstname','cellnumber','cellmessage','homenumber','homemessage','worknumber','workmessage','emailaddress','address','address2','city','state','zipcode','dob','referrer','client_status', 'userinfo')

def output(val, comma=True):
    sys.stdout.write(str(val))
    if comma:
        sys.stdout.write(',')

def output_column_names(column_names):
    for i in range (0, len(column_names)):
        if i == (len(column_names) - 1):
            output(column_names[i], comma=False)
        else:
            output(column_names[i])
    output('\n', comma=False)
    
def output_month(val):
    if val == 'January':
        output('01')
    if val == 'February':
        output('02')
    if val == 'March':
        output('03')
    if val == 'April':
        output('04')
    if val == 'May':
        output('05')
    if val == 'June':
        output('06')
    if val == 'July':
        output('07')
    if val == 'August':
        output('08')
    if val == 'September':
        output('09')
    if val == 'October':
        output('10')
    if val == 'November':
        output('11')
    if val == 'December':
        output('12')
    else:
        output('01')
    
output_column_names(client_column_order)
    
for client in client_list:
    output(client[0]) # key
    output(client[1].partition(' ')[0], comma=False) #create time
    output('T', comma=False)
    output(client[1].partition(' ')[2])
    output(client[2]) # lastname
    output(client[3]) # firstname
    output(client[4]) # cellnumber
                                # cellmessage
    if client[5] == 'MsgNOK':
        output('Message Not OK')
    else:
        output('Message OK')
    output(client[6]) # homenumber
                                # homemessage
    if client[7] == 'MsgNOK':
        output('Message Not OK')
    else:
        output('Message OK')
    output(client[8]) # worknumber
                                # workmessage
    if client[9] == 'MsgNOK':
        output('Message Not OK')
    else:
        output('Message OK')
    output(client[10]) # emailaddress
    output(client[11]) # address
    output(client[12]) # address2
    output(client[13]) # city
    output(client[14]) # state
    output(client[15]) # zipcode
    if len(client[18]) > 0:
        output(client[18], comma=False) # format is YEAR-MONTH-DAYT00:00:00
        output('-', comma=False)
        output_month(client[17])
#        output(client[17], comma=False)
        output('-', comma=False)
        output(client[16], comma=False)
        output('T00:00:00')
    else:
        output('')
    output(client[19]) # referrer
    output(client[20]) # client_status
    output('EmailADDRHere', comma=False)
    output('\n', comma=False)
    
dos_list =  (
 (1,2,'90801',' ','','','','','','2010-01-01 01:00:00','45','No'),
 (2,1,' ',' ','','','','','','2010-03-16 08:00:00','45','No'),
 (3,1,' ','Scheduled','','','','','','2010-03-30 08:00:00','45','No'),
 (4,1,' ','Attended','','','','','','2010-03-31 08:00:00','45','No'),
 (5,1,' ','Scheduled','','','','','','2010-04-06 08:00:00','45','No'),
 (6,1,' ','Cancellation - Late','','','','','','2010-04-07 08:00:00','45','7'),
 (7,1,' ','Attended','','','','','','2010-04-21 08:00:00','45','No'),
 (8,3,' ','Scheduled','','','','','','2010-04-09 08:00:00','45','No')
)
dos_column_order = ('key','clientinfo','session_type','session_result','dsm_code','type_pay','amt_due','amt_paid','note','dos_datetime','dos_duration','dos_repeat','userinfo')
#clientinfo,session_result,dos_repeat,dos_duration,userinfo,key,dos_datetime
#(`id`,`clientinfo_id`,`session_type`,`session_result`,`dsm_code`,`type_pay`,`amt_due`,`amt_paid`,`note`,`dos_datetime`,`dos_duration`,`dos_repeat`)
#        ('No', 'No'),
#        ('7', 'One Week'),
#        ('14', 'Two Week'),
#        ('21', 'Three Weeks'),
#        ('28', 'Four Weeks'),
output_column_names(dos_column_order)

for dos in dos_list:
    output(dos[0]) # key
    output(dos[1]) # clientinfo
    if dos[2] == ' ':
        output('')
    else:
        output(dos[2]) # session_type
    if dos[3] == ' ':
        output('')
    else:
        output(dos[3]) # session_result
    output(dos[4]) # dsm_code
    output(dos[5]) # type_pay
    output(dos[6]) # amt_due
    output(dos[7]) # amt_paid
    output(dos[8]) # note
    output(dos[9].partition(' ')[0], comma=False) #create time
    output('T', comma=False)
    output(dos[9].partition(' ')[2])
    output(dos[10]) # dos_duration
    output(dos[11]) # dos_repeat
    output('EmailADDRHere', comma=False)
    output('\n', comma=False)
    
dos_recurr_order = ('key','dos_base','dos_recurr_datetime','userinfo')
output_column_names(dos_recurr_order)

dos_recurr_list = (
 (1,6,'2010-04-14 08:00:00',''),
 (2,6,'2010-05-05 08:00:00',''),
 (7,6,'2010-05-26 08:00:00',''),
 (4,6,'2010-05-12 08:00:00',''),
 (5,6,'2010-04-28 08:00:00',''),
 (6,6,'2010-05-19 08:00:00',''),
 (8,6,'2010-06-09 08:00:00',''),
 (9,6,'2010-06-02 08:00:00',''),
 (10,6,'2010-06-16 08:00:00',''),
 (11,6,'2010-06-23 08:00:00',''),
 (12,6,'2010-06-30 08:00:00',''),
 (13,6,'2010-07-07 08:00:00',''),
 (14,6,'2010-07-14 08:00:00',''),
 (15,6,'2010-07-21 08:00:00',''),
 (16,6,'2010-07-28 08:00:00',''),
 (17,6,'2010-08-04 08:00:00',''),
 (18,6,'2010-08-11 08:00:00',''),
 (19,6,'2010-08-18 08:00:00',''),
 (20,6,'2010-08-25 08:00:00',''),
 (21,6,'2010-09-01 08:00:00','')
)
for dos_recurr in dos_recurr_list:
    output(dos_recurr[0]) # key
    output(dos_recurr[1]) # dos_base
    output(dos_recurr[2].partition(' ')[0], comma=False) # dos_recurr_datetime
    output('T', comma=False)
    output(dos_recurr[2].partition(' ')[2])
    output('EmailADDRHere', comma=False)
    output('\n', comma=False)
    

