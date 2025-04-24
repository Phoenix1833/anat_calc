import ipaddress
import argparse
from typing import List

# Эмуляция jhash_1word (можно заменить настоящей реализацией при необходимости)
def jhash_1word(val, initval=0):
    val &= 0xFFFFFFFF
    val ^= initval
    val = (val + (val << 12)) & 0xFFFFFFFF
    val ^= (val >> 22)
    val = (val + (val << 4)) & 0xFFFFFFFF
    val ^= (val >> 9)
    val = (val + (val << 10)) & 0xFFFFFFFF
    val ^= (val >> 2)
    val = (val + (val << 7)) & 0xFFFFFFFF
    val ^= (val >> 12)
    return val & 0xFFFFFFFF

# reciprocal_scale на Python
def reciprocal_scale(val, n):
    return (val * n) >> 32

# Структура пула
class NatPool:
    def __init__(self, usr_start, usr_end, nat_start, nat_end, hashtype, exclude=0):
        self.usr_start = int(ipaddress.IPv4Address(usr_start))
        self.usr_end = int(ipaddress.IPv4Address(usr_end))
        self.nat_start = int(ipaddress.IPv4Address(nat_start))
        self.nat_end = int(ipaddress.IPv4Address(nat_end))
        self.hashtype = hashtype
        self.exclude = exclude

# Обратное вычисление для линейного NAT
def reverse_linear_nat(ext_ip: int, pool: NatPool) -> List[str]:
    results = []
    for i in range(pool.usr_start, pool.usr_end + 1):
        base = ((i - pool.usr_start) * (pool.nat_end + 1 - pool.nat_start)) // (pool.usr_end + 1 - pool.usr_start)
        nat_ip = pool.nat_start + base

        if (nat_ip % 256 == 0 and (pool.exclude & 1)):
            nat_ip += 1
        elif (nat_ip % 256 == 255 and (pool.exclude & 2)):
            nat_ip -= 1

        if nat_ip == ext_ip:
            results.append(str(ipaddress.IPv4Address(i)))
    return results

# Перебор для hash-схемы
def reverse_hash_nat(ext_ip: int, pool: NatPool) -> List[str]:
    results = []
    rng = pool.nat_end - pool.nat_start + 1
    for i in range(pool.usr_start, pool.usr_end + 1):
        hashed = jhash_1word(i)
        mapped = pool.nat_start + reciprocal_scale(hashed, rng)

        if (mapped % 256 == 0 and (pool.exclude & 1)):
            mapped += 1
        elif (mapped % 256 == 255 and (pool.exclude & 2)):
            mapped -= 1

        if mapped == ext_ip:
            results.append(str(ipaddress.IPv4Address(i)))
    return results

# Главная функция

def main():
    parser = argparse.ArgumentParser(description="NAT Reverse Calculator")
    parser.add_argument("ext_ip", help="Внешний IP-адрес NAT")
    args = parser.parse_args()

    ext_ip_int = int(ipaddress.IPv4Address(args.ext_ip))

    # Пример пулов (можно заменить чтением из файла или БД)
    pools = [
        NatPool("10.0.192.0", "10.0.255.255", "178.110.1.0", "178.110.1.255", hashtype=0, exclude=3),
        NatPool("192.168.0.1", "192.168.10.255", "178.110.1.0", "178.110.1.255", hashtype=0, exclude=3),
    ]

    all_results = []
    for pool in pools:
        if pool.hashtype == 0:
            res = reverse_linear_nat(ext_ip_int, pool)
        else:
            res = reverse_hash_nat(ext_ip_int, pool)

        if res:
            print(f"Найдено в пуле {ipaddress.IPv4Address(pool.usr_start)} - {ipaddress.IPv4Address(pool.usr_end)}:")
            for r in res:
                print(f"LAN IP: {r}")
            all_results.extend(res)

    if not all_results:
        print("Подходящие внутренние адреса не найдены.")

if __name__ == "__main__":
    main()
