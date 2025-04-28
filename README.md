```markdown
# NAT Reverse Calculator

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

Этот инструмент позволяет определить возможные внутренние (серые) IP-адреса на основе предоставленного внешнего (белого) адреса, зная параметры NAT-пулов.

## 📦 Установка

```bash
git clone https://github.com/Phoenix1833/anat_calc.git
cd anat_calc
```

## 🚀 Использование

```bash
python calc.py <external_ip>
```

**Пример:**

```bash
python calc.py 178.110.1.100
```

## ⚙️ Настройка NAT-пулов

Редактируйте файл `calc.py`, чтобы добавить свои NAT-пулы:

```python
pools = [
    NatPool(
        "10.0.0.1",         # Начало внутреннего диапазона
        "10.0.255.254",     # Конец внутреннего диапазона
        "178.110.1.0",      # Начало внешнего диапазона
        "178.110.1.255",    # Конец внешнего диапазона
        hashtype=0,         # 0 - линейный NAT, 1 - хешированный
        exclude=3           # Битовая маска (1 - исключить .0, 2 - исключить .255)
    ),
    # Добавьте дополнительные пулы здесь
]
```

## 🔍 Поддерживаемые алгоритмы NAT

### Линейный NAT (`hashtype=0`)

```python
base = ((internal_ip - internal_start) * external_range) / internal_range
external_ip = external_start + base
```

### Хешированный NAT (`hashtype=1`)

```python
hashed = jhash_1word(internal_ip)
external_ip = external_start + reciprocal_scale(hashed, range_size)
```

## 📝 Пример вывода

```plaintext
Найдено в пуле 10.0.192.0 - 10.0.255.255:
LAN IP: 10.0.200.42
LAN IP: 10.0.210.128

Найдено в пуле 192.168.0.1 - 192.168.10.255:
LAN IP: 192.168.5.33
```

## ⚠️ Ограничения

- Поддерживается только IPv4
- NAT-пулы должны быть заданы в коде
- Требуется Python 3.6 или новее

## 📜 Лицензия

Этот проект распространяется под лицензией MIT.
``` 