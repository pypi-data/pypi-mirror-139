
def lcm(*numbers):
    num=1
    while(1):
        l=[i for i in numbers if num%i==0]
        if (len(l)==len(numbers)):
            break
        num=num+1
    return num
def hcf(*numbers):
    a=numbers
    num=0
    a=list(a)
    a.sort()
    for i in range(1,a[0]+1):
        l=[j for j in a if j%i==0]
        if (len(a)==len(l)):
            num=i
    return num
def palidrome(number):
    n=number
    if (str(n)==str(n)[::-1]):
        return True
    else:
        return False
def reverse(number):
    n=number
    return int(str(n)[::-1])
def even(number):
    n=number
    return (n%2==0)
def odd(number):
    n=number
    return (n%2!=0)
def leap(number):
    n=number
    if (n % 4) == 0:
        if (n % 100) == 0:
            if (n % 400) == 0:
                return True
            else:
                return False
        else:
             return True
    else:
        return False
def swap(first,second):
    return second,first
def strong(number):
    n=number
    st=0
    for i in str(n):
        p=1
        for i in range(1,int(i)+1):
            p=p*i
        st=st+p
    if (st==n):
        return True
    else:
        return False
def armstrong(number):
    n=number
    return (sum([int(i)**len(str(n)) for i in str(n)])==n)
def perfect(number):
    n=number
    return (sum([i for i in range(1,n) if n//i==n/i])==n)
def prime(number):
    n=number
    return not(bool([1 for i in range(2,n) if n//i==n/i]))

def productofdigits(number):
    n=number
    p=1
    for i in str(n):
        p=p*int(i)
    return p
def sumofdigits(number):
    n=number
    return sum([int(i) for i in str(n)])
def fibonaci(number):
    n=number
    p=1
    for i in range(1,n+1):
        p=p*i
    return p
def count(number):
    n=number
    return len(str(n))
def swap_digit(List,first,second):
    n=List
    a=first
    b=second
    s=str(n)
    s=list(s)
    x=s[a-1]
    y=s[b-1]
    s[a-1]=y
    s[b-1]=x
    s=''.join(s)
    n=int(s)
    return n
def duplicate(List):
    l=List
    e=[]
    for i in l:
        if (l.count(i)>1):
            e.append(i)
    return e
def unique(List):
    l=List
    l=list(set(l))
    return l
def vowel(string):
    s=string
    v=['a','e','i','o','u']
    return sum([1 for i in s if i in v])
def consonent(string):
    s=string
    v=['a','e','i','o','u']
    return abs(len(s)-sum([1 for i in s if i in v]))
def anagram(string1,string2):
    return (sorted(string1)==sorted(string2))
def prime_range(start,end):
    a=start
    b=end
    e=[]
    for n in range(a,b+1):
        if (not(bool([1 for i in range(2,n) if n//i==n/i]))):
            e.append(n)
    return e
def armstrong_range(start,end):
    a=start
    b=end
    e=[]
    for n in range(a,b+1):
        if (sum([int(i)**len(str(n)) for i in str(n)])==n):
            e.append(n)
    return e
def perfect_range(start,end):
    a=start
    b=end
    e=[]
    for n in range(a,b+1):
        if (sum([i for i in range(1,n) if n//i==n/i])==n):
            e.append(n)
    return e
def strong_range(start,end):
    a=start
    b=end
    e=[]
    for n in range(a,b+1):
        st=0
        for i in str(n):
            p=1
            for i in range(1,int(i)+1):
                p=p*i
            st=st+p
        if (st==n):
            e.append(n)
    return e
def frequency(List):
    l=List
    e=[l.count(i) for i in l]
    return e
def calculate(expression):
    s=expression
    return eval(s)
        
def sumofrange(start,end,jump):
    a=start
    b=end
    k=jump
    s=0
    for i in range(a,b+1,k):
        s=s+i
    return(s)     
def nfibonaci(number):
    l=[]
    l.append(0)
    x=0
    y=1
    for _ in range(1,number):
        z=x+y
        x=y
        y=z
        l.append(z) 
    return l   