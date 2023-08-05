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
    emails=['gmail.com','outlook.com','tutanota.com','gmx.com','yahoo.com','aol.com','mail.com','zoho.com','protonmail.com','mailerlite.com','ukr.net','mail.ru','yandex.ru']
    firstnames=open(os.path.join(os.path.dirname(__file__), 'normalnames.txt'),'r').read().split('\n')
    surnames=open(os.path.join(os.path.dirname(__file__), 'familii.txt'),'r').read().split('\n')
    fstnm=choice(firstnames)
    sndname=choice(surnames)
    streetsDict={}
    citiesDict={}
    address=''
    cities=[]
    street=[]
    
    separator=['.','-','_','']
    cletters=string.ascii_uppercase
    def __init__(self):
        self.cities=open(os.path.join(os.path.dirname(__file__), 'city.txt'),'r').read().split('\n')
        self.street=open(os.path.join(os.path.dirname(__file__), 'streets.txt'),'r').read().split('\n')
        fstnm=choice(self.firstnames)
        sndname=choice(self.surnames)
        self.fstnm=fstnm
        self.sndname=sndname
        for city in self.cities:
            elem=''
            ln=len(city.split(':'))
            if ln==3:
                elem=city.split(':')[1]+':'+city.split(':')[2]
            elif ln==2 :
                elem=city.split(':')[1]
            else:
                continue
            if city.split(':')[0] not in self.citiesDict:
                self.citiesDict[city.split(':')[0]]=[elem]
            else:
                self.citiesDict[city.split(':')[0]].append(elem)
                
        for strt in self.street:
            elem=''
            ln=len(strt.split(':'))
            if ln==3:
                elem=strt.split(':')[1]+':'+strt.split(':')[2]
            elif ln==2 :
                elem=strt.split(':')[1]
            else:
                continue
            if strt.split(':')[0] not in self.streetsDict:
                self.streetsDict[strt.split(':')[0]]=[elem]
            else:
                self.streetsDict[strt.split(':')[0]].append(elem)                
        
    
    @classmethod
    def get_firstname(cls):
        
        return choice(cls.firstnames)


    @classmethod
    def get_sndname(cls):
        return choice(cls.surnames)

    @classmethod    
    def generate_email(cls,firstname=None,secondname=None):
        """generate an email address

        Returns:
            str: string with email
        """        
        fullname=''
        username=''
        firstnames=cls.firstnames
        separator=cls.separator
        surnames=cls.surnames
        cletters=cls.cletters
        emails=cls.cletters
        emails=cls.emails
        for _ in range(randint(3,9)):
            username+=secrets.choice(string.ascii_lowercase)    
        typ=randint(1,9)
        if not firstname and not secondname:
            fstnm=choice(cls.firstnames)
            sndname=choice(cls.surnames)
            cls.fstnm=fstnm
            cls.sndname=sndname
        else:
            fstnm=firstname
            sndname=secondname
            cls.fstnm=fstnm
            cls.sndname=sndname
        if fstnm.endswith('a') and not ( sndname.endswith('a') or sndname.endswith('o')):
            sndname+='a'
        if not fstnm.endswith('a') and sndname.endswith('a'):
            sndname=sndname[:-1]
        if typ==1:
            fullname=fstnm+choice(separator)+sndname+'@'+choice(emails)
        elif typ==2:
            fullname=choice(cletters)+choice(separator)+sndname+'@'+choice(emails)
        elif typ==3:
            fullname=fstnm+choice(separator)+sndname+choice(separator)+ str(randint(1900,2030))+'@'+choice(emails)
        elif typ==4:
            fullname=fstnm+choice(separator)+ str(randint(1900,2030))+'@'+choice(emails)   
        elif typ==5:
            fullname=choice(cletters)+ sndname+choice(separator)+ str(randint(1960,2018)) +'@'+choice(emails) 
        elif typ==6:
            fullname=fstnm+choice(separator)+ username +'@'+choice(emails)
        elif typ==7:
            fullname=fstnm+ username +sndname +'@'+choice(emails)  
        elif typ==8:
            fullname=sndname+ choice(separator) + username +'@'+choice(emails) 
        else:
            fullname=username+ choice(separator) + fstnm  +'@'+choice(emails)
        if cls.prevemail!=fullname:
            cls.prevemail=fullname
            return fullname
        else:
            cls.prevemail=fullname
            return "admin"+username+choice(emails)  
        
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
    
    def generate_address(self):
        fstnm=choice(self.firstnames)
        sndname=choice(self.surnames)
        self.fstnm=fstnm
        self.sndname=sndname

        countries=list(self.citiesDict.keys())
        country=choice(countries)
        mycity=choice(list(self.citiesDict[country]))
        mystreet=choice(self.streetsDict[country])
        ln=len(mycity.split(':'))
        if ln==2:
            elem=mycity.split(':')[0]+', st.'+mycity.split(':')[1]
        elif ln==1 :
            elem=mycity.split(':')[0]
        address=country +' city.'+elem+' '+mystreet+' h.'+str(randint(1,300))+' ft.'+str(randint(1,300))
        if country=='Germany':
            tel='+49'+"".join([str(randint(1,10)) for i in range(1,randint(6,13+1))])
        elif country=='UnitedKingdom':
            tel='+44'+"".join([str(randint(1,10)) for i in range(1,randint(7,10+1))])
        elif country=='UnitedStates':
            tel='+1'+"".join([str(randint(1,10)) for i in range(1,10+1)])
        elif country=='Ukraine':
            tel='+380'+"".join([str(randint(1,10)) for i in range(1,9+1)]) 
        return address,tel
        

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