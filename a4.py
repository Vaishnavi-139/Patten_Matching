
import random
import math


# To generate random prime less than N
def randPrime(N):
    primes = []
    for q in range(2, N + 1):
        if isPrime(q):
            primes.append(q)
    return primes[random.randint(0, len(primes) - 1)]


# To check if a number is prime
def isPrime(q):
    if q > 1:
        for i in range(2, int(math.sqrt(q)) + 1):
            if q % i == 0:
                return False
        return True
    else:
        return False


# pattern matching
def randPatternMatch(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatch(q, p, x)


# pattern matching with wildcard
def randPatternMatchWildcard(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q, p, x)


# return appropriate N that satisfies the error bounds
def findN(eps, m):
    k = eps / (2 * m * math.log2(26))  # assuming the relation that root(n)> log(n)
    return int(math.e ** 1 / k)


# Return sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):
    m = len(p)
    n = len(x)
    list4 = []
    equalitysum = calculateHash(p)
    equality = equalitysum % q  # Hash for q
    Hashsum = calculateHash(x[0:m])  # Hash for the first m letters from x. First case to compare
    Hash = Hashsum % q
    if Hash == equality:  # passing case
        list4.append(0)
    for i in range(1, n - m + 1):
        Hashsum -= (Numeral(x[i - 1]) * (26 ** (m - 1)))  # removing the contribution of the first no from the hash
        Hashsum = (
                Hashsum * 26)  # since we are shifting all the numbers foreward in the function, we have to multiply
        # all of them by 26. This in turn increase their reminder by a factor of 26
        Hashsum += Numeral(x[i + m - 1])
        Hash = Hashsum % q
        if Hash == equality:
            list4.append(i)
    return list4


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q, p, x):
    m = len(p)
    n = len(x)
    list5 = []
    pDash = list(p)
    if not (
            '?' in pDash):  # since the question said that the input in modPatternMatchWildcard will be a subset of
        # the alphabets union with '?', we can also have the case when there is no '?'
        # the cde for this case is same as modPatternMatch.
        equalitysum = calculateHash(p)  # f(q)
        equality = equalitysum % q  # Hash for q
        Hashsum = calculateHash(x[0:m])  # f(x[0:m])
        Hash = Hashsum % q  # Hash for the first m letters from x. First case to compare
        if Hash == equality:  # add to the list
            list5.append(0)
        for i in range(1, n - m + 1):
            Hashsum -= (Numeral(x[i - 1]) * (26 ** (m - 1)))  # removing the contribution of the first no from the hash
            Hashsum = (Hashsum * 26)  # since we are shifting all the numbers foreward in the function,
            # we have to multiply all the no.s i.e.multiply all of them by 26.
            Hashsum += Numeral(x[i + m - 1])  # adding the i+m th term
            Hash = Hashsum % q  # taking the mod
            if Hash == equality:  # add to the list
                list5.append(i)
    elif '?' in pDash:  # the wildcard case
        positionInQ = pDash.index('?')  # finding the index of '?' inn the test string q
        equalitysum = calHashList(pDash, positionInQ)  # f(q)- p[posiition_of_'?']*26**(n-position_of_'?'-1)
        equality = equalitysum % q  # Hash for q
        Hashsum = calHashList(list(x[0:m]),
                              positionInQ)  # f(x[0:m])- p[posiition_of_'?']*26**(n-position_of_'?'-1). the first
        # case to compare
        Hash = Hashsum % q  # Hash for the first m letters from x. First case to compare
        if Hash == equality:
            list5.append(0)  # add to the list
        for i in range(1, n - m + 1):
            Hashsum -= (Numeral(x[i - 1]) * (26 ** (m - 1)))  # removing the first digit's contribution
            Hashsum += (Numeral(x[i + positionInQ - 1]) * 26 ** (
                        m - positionInQ - 1))  # adding the contribution of the digit which was at position_of_'?'
            # for the earlier case; but is at a different position for this case
            Hashsum -= (Numeral(x[i + positionInQ]) * 26 ** (
                        m - positionInQ - 2))  # removing the contritbution of the '?' position digit
            Hashsum = (Hashsum * 26)  # since we are shifting all the numbers foreward in the function,
            Hashsum += Numeral(x[i + m - 1])  # adding the i+m th term
            Hash = Hashsum % q  # taking the mod
            if Hash == equality:
                list5.append(i)  # add to the list
    return list5


# returns the numeral alias of the alphabet input
def Numeral(x):
    list1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']
    list2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    for i in range(0, 26):
        if x == list1[i]:  # average case time complexity is O(13)
            return list2[i]


# this function doesn't return anything for any input other than these alphabets

# returns the hash(sum) of a  string the q.
def calculateHash(p):
    summ = 0
    list3 = list(p)
    n = len(list3)
    for i in range(0, n):
        summ += (26 ** (n - i - 1)) * (Numeral(list3[i]))  # summ = f(p)
    return summ


# returns the hash(sum) of a set of alphabets except one position given the q and position
def calHashList(p, position):
    sum1 = 0
    n = len(p)
    for i in range(0, n):
        if i != position:
            sum1 += (26 ** (n - i - 1)) * (Numeral(p[i]))  # sum1= f(p) - p[posiition]*26**(n-position-1)
    return sum1
# the time complexity is Order(m) where m is the length of the string to be searched
