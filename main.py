import time

def ciclo ():
    cnt = 0
    while True:
        print (f"{cnt}: Ciclo de ejecucion...")
        cnt += 1
        time.sleep(1)

if __name__ == "__main__":
    ciclo