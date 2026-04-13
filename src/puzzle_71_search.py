import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
import requests

# Введите ваш API-ключ Pushbullet
PUSHBULLET_API_KEY = '?????????????'  # замените на ваш ключ


# Функция для отправки Pushbullet уведомления
def send_pushbullet_message(api_key, title, message):
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {
        'Access-Token': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'note',
        'title': title,
        'body': message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Уведомление успешно отправлено!")
    else:
        print("Ошибка отправки уведомления:", response.text)


# Ввод диапазона начального и конечного приватных ключей в hex
start_hex = input("начало(hex): ").strip()
end_hex = input("конец(hex): ").strip()

start_int = int(start_hex, 16)
end_int = int(end_hex, 16)

# Ввод искомого адреса
target_address = '1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU'
total_keys = end_int - start_int + 1


# Функция для получения WIF
def privkey_to_wif(priv_key_bytes):
    versioned_payload = b'\x80' + priv_key_bytes
    compressed_payload = versioned_payload + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(compressed_payload).digest()).digest()[:4]
    full_payload = compressed_payload + checksum
    return base58.b58encode(full_payload).decode()


# Функция для получения биткоин-адрес из приватного ключа
def privkey_to_address(priv_key_bytes):
    sk = SigningKey.from_string(priv_key_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()

    x_bytes = vk.pubkey.point.x().to_bytes(32, 'big')
    y = vk.pubkey.point.y()
    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    compressed_public_key = prefix + x_bytes

    sha256_pk = hashlib.sha256(compressed_public_key).digest()
    ripemd160 = hashlib.new('ripemd160', sha256_pk).digest()

    payload = b'\x00' + ripemd160  # 0x00 — mainnet адрес
    checksum_addr = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address_bytes = payload + checksum_addr
    address = base58.b58encode(address_bytes).decode()
    return address


found = False  # флаг для определения, найден ли адрес

# Открываем файл для записи результата (если найден)
with open('result.txt', 'w') as result_file:
    # Перебираем диапазон ключей
    for idx, priv_int in enumerate(range(start_int, end_int + 1), 1):
        priv_bytes = priv_int.to_bytes(32, 'big')
        address = privkey_to_address(priv_bytes)

        if address == target_address:
            wif = privkey_to_wif(priv_bytes)
            print(f"Адрес найден: {address}")
            print(f"Приватный ключ (WIF): {wif}")
            # Записываем WIF в файл
            result_file.write(f'Address: {address}\nWIF: {wif}\n')
            # Отправляем уведомление через Pushbullet
            send_pushbullet_message(PUSHBULLET_API_KEY, 'Мы что-то нашли!', f'Адрес: {address}')
            found = True
            break

        # Показываем прогресс каждые 100 итераций
        if idx % 100 == 0 or idx == total_keys:
            percent = (idx / total_keys) * 100
            print(f"Прогресс: {percent:.2f}% ({idx} из {total_keys})")

    if not found:
        print("Адрес в диапазоне не найден.")
        # Также можно записать в файл, что ничего не найдено
        result_file.write("Адрес в диапазоне не найден.\n")
        # Можно тоже отправить уведомление
        send_pushbullet_message(PUSHBULLET_API_KEY, 'Bitcoin скрипт', 'Адрес не найден в диапазоне.')