from statistic import Stat

message = '''
This file exist for resetting statistics
Your last scores will deleted
Are you sure that you need to reset it? 
Write "Yes" if you need or "Not" if not 
>>>> '''
stat = Stat()
agreement = input(message)
if agreement.lower() == 'yes':
    stat.rewrite_file(True)
    print('Statistic resetting successful !')
else: print('You cancelled resetting...')