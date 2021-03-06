from Crypto.Util.number import getPrime, getRandomNBitInteger
from time import time

# lengths in bits
LENGTH_MACHINE_PRIVATE_KEY = 8
LENGTH_PUBLIC_GENERATOR = 4
LENGTH_PUBLIC_PRIME = 1024

# available in public domain - maybe stashed or generated in realtime
PUBLIC_GENERATOR = getRandomNBitInteger(LENGTH_PUBLIC_GENERATOR) #g
PUBLIC_PRIME = getPrime(LENGTH_PUBLIC_PRIME) #n
print("Public Generator: {g} \nPublic Prime: {n}".format(g=PUBLIC_GENERATOR, n=PUBLIC_PRIME))

def main():
  
  # to time the functions
  # merely to show difference in processing power required at different lengths of constants
  # no real life significance
  time_m1, time_m2 = 0, 0

  start_m1 = time()
  m1 = Machine() # Intializing simulation of first machine
  k1 = m1.getPublicKey(PUBLIC_GENERATOR, PUBLIC_PRIME) # obtaining public key generated by the first machine
  end_m1 = time()
  time_m1 = end_m1 - start_m1

  priv_k1 = m1.getPrivateKey() # obtaining private key of the first machine (only for demo)

  start_m2 = time()
  m2 = Machine() # Intializing simulation of second machine
  k2 = m2.getPublicKey(PUBLIC_GENERATOR, PUBLIC_PRIME)  # obtaining public key generated by the second machine
  end_m2 = time()
  time_m2 = end_m2 - start_m2

  priv_k2 = m2.getPrivateKey() # obtaining private key of the second machine (only for demo)

  start_m1 = time()
  dhk1 = m1.setDHKey(k2) # obtaining DHKey for the first machine. In real life this would just be stored on that machine locally
  end_m1 = time()
  time_m1 += end_m1 - start_m1

  start_m2 = time()
  dhk2 = m2.setDHKey(k1) # obtaining DHKey for the second machine. In real life this would just be stored on that machine locally
  end_m2 = time()
  time_m2 += end_m2 - start_m2

  print(f"Machine M1:\nPrivate Key (priv_k1): {priv_k1}\nPublic Key (k1): {k1}\nDH Key (dhk1): {dhk1}\nTime taken: {time_m1}\n\n")
  print(f"Machine M2:\nPrivate Key (priv_k2): {priv_k2}\nPublic Key (k2): {k2}\nDH Key (dhk2): {dhk2}\nTime taken: {time_m2}\n\n")

class Machine:
  def __init__(self):
    self.__private_key = getRandomNBitInteger(LENGTH_MACHINE_PRIVATE_KEY)
    self.__dh_key = 0
    self.__public_prime = None
  
  def getPublicKey(self, public_generator: int, public_prime: int) -> int:
    '''
    Returns public key after calculation of g^(a)mod(n) where 'a' is the private key of the machine

    :param int public_generator: generator 'g' from the public domain
    :param int public_prime: large prime number 'n' used as modulo
    :return: int public key
    '''
    self.__public_prime = public_prime
    return (pow(public_generator, self.__private_key)%self.__public_prime)

  def setDHKey(self, other_public_key: int) -> int:
    '''
    Sets the final DHKey after calculation of q^(a)mod(n) where 'q' is the public key of the other machine and 'a' is the private key of this machine
    Returns (only for demo) the final DHKey (this would just be stored in the local storage in real life)

    :param int other_public_key: public key generated by other machine (public key is the return value of Machine.getPublicKey()
    :return: int DHKey
    '''
    self.__dh_key = (pow(other_public_key, self.__private_key)%self.__public_prime)
    return self.__dh_key # do not transmit the dhkey in real life
  
  def getPrivateKey(self) -> int:
    '''
    Returns (only for demo) the private key of this machine. (This would never leave the machine in real life)
    '''
    return self.__private_key # do not transmit the private key in real life

main()