import random
from random import choice
from random import randint
import string
import secrets
import colorama
import os
import sys
from colorama import init, Fore, Back, Style

# essential for Windows environment
init()
# all available foreground colors
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
# all available background colors
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
# brightness values
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

class GET_EMAIL:
    prevemail='z'
    fstnm=''
    sndname=''
    emails=['gmail.com','outlook.com','tutanota.com','gmx.com','yahoo.com','aol.com','mail.com','zoho.com','protonmail.com','mailerlite.com','ukr.net','mail.ru','yandex.ru']
    firstnames=open(os.path.join(os.path.dirname(__file__), 'normalnames.txt'),'r').read().split('\n')
    surnames=open(os.path.join(os.path.dirname(__file__), 'familii.txt'),'r').read().split('\n')

    separator=['.','-','_','']
    cletters=string.ascii_uppercase
    def __init__(self):
        pass
      
    
    @classmethod
    def get_firstname(cls):
        return cls.fstnm


    @classmethod
    def get_sndname(cls):
        return cls.sndname

    @classmethod    
    def generate_email(cls):
        """generate an email address

        Returns:
            str: string with email
        """        
        fullname=''
        username=''
        fstnm=''
        sndname=''
        firstnames=cls.firstnames
        separator=cls.separator
        surnames=cls.surnames
        cletters=cls.cletters
        emails=cls.cletters
        emails=cls.emails
        for _ in range(randint(3,9)):
            username+=secrets.choice(string.ascii_lowercase)    
        typ=randint(1,9)
        fstnm=choice(cls.firstnames)
        sndname=choice(cls.surnames)
        cls.fstnm=fstnm
        cls.sndname=sndname
        if fstnm.endswith('a') and not ( sndname.endswith('a') or sndname.endswith('o')):
            sndname+='a'
        if not fstnm.endswith('a') and sndname.endswith('a'):
            sndname=sndname[:-1]
        if typ==1:
            fullname=fstnm+choice(separator)+sndname+'@'+choice(emails)
        elif typ==2:
            fullname=choice(cletters)+choice(separator)+choice(surnames)+'@'+choice(emails)
        elif typ==3:
            fullname=fstnm+choice(separator)+sndname+choice(separator)+ str(randint(1900,2030))+'@'+choice(emails)
        elif typ==4:
            fullname=fstnm+choice(separator)+ str(randint(1900,2030))+'@'+choice(emails)   
        elif typ==5:
            fullname=choice(cletters)+ choice(surnames)+choice(separator)+ str(randint(1960,2018)) +'@'+choice(emails) 
        elif typ==6:
            fullname=choice(firstnames)+choice(separator)+ username +'@'+choice(emails)
        elif typ==7:
            fullname=fstnm+username+ sndname +'@'+choice(emails)  
        elif typ==8:
            fullname=choice(surnames)+ choice(separator) + username +'@'+choice(emails)    
        if cls.prevemail!=fullname:
            cls.prevemail=fullname
            return fullname
        else:
            cls.prevemail=fullname
            return None
        
    @classmethod
    def generate_emails(cls,num):
        """Generate string with defined number of emails
        

        Args:
            num (int): number of emails

        Returns:
            string: string with email
        """        
        emails=[ GET_EMAIL.generate_email() for i in range(1,num+1)]
        emails = [mail for mail in emails if mail]
        sender=", ".join(emails)
        return sender        

def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)

generate_emails=GET_EMAIL.generate_emails

def main():
    cnt=0
    # num=input('Введіть кількість емейлів:')
    num=int(sys.argv[1])
    print('')
    print('*'*80)
    print('')
    while cnt<num:
        email=GET_EMAIL.generate_email()
        if email:
            print_with_color(email, color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
            cnt+=1
    print('')
    print('*'*80)
    print('') 
   
if __name__ == '__main__':
    main()