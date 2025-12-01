import streamlit as st

# ==========================================
# 1. DATABASE S-BOX 44 (Tetap Pake yang Kuat dari Paper)
# ==========================================
# Sumber: Table 16 - Proposed S-box 44
sbox_44 = [
    99,
    205,
    85,
    71,
    25,
    113,
    127,
    63,
    219,
    244,
    109,
    159,
    11,
    228,
    94,
    214,
    77,
    177,
    201,
    78,
    5,
    29,
    48,
    30,
    87,
    96,
    193,
    80,
    156,
    200,
    216,
    86,
    116,
    143,
    10,
    14,
    54,
    169,
    148,
    68,
    49,
    75,
    171,
    157,
    92,
    114,
    188,
    194,
    121,
    220,
    131,
    210,
    83,
    135,
    250,
    149,
    253,
    72,
    182,
    33,
    190,
    141,
    249,
    82,
    232,
    50,
    21,
    84,
    215,
    242,
    180,
    198,
    168,
    167,
    103,
    122,
    152,
    162,
    145,
    184,
    43,
    237,
    119,
    183,
    7,
    12,
    125,
    55,
    252,
    206,
    235,
    160,
    140,
    133,
    179,
    192,
    110,
    176,
    221,
    134,
    19,
    6,
    187,
    59,
    26,
    129,
    112,
    73,
    175,
    45,
    24,
    218,
    44,
    66,
    151,
    32,
    137,
    31,
    35,
    147,
    236,
    247,
    117,
    132,
    79,
    136,
    154,
    105,
    199,
    101,
    203,
    52,
    57,
    4,
    153,
    197,
    88,
    76,
    202,
    174,
    233,
    62,
    208,
    91,
    231,
    53,
    1,
    124,
    0,
    28,
    142,
    170,
    158,
    51,
    226,
    65,
    123,
    186,
    239,
    246,
    38,
    56,
    36,
    108,
    8,
    126,
    9,
    189,
    81,
    234,
    212,
    224,
    13,
    3,
    40,
    64,
    172,
    74,
    181,
    118,
    39,
    227,
    130,
    89,
    245,
    166,
    16,
    61,
    106,
    196,
    211,
    107,
    229,
    195,
    138,
    18,
    93,
    207,
    240,
    95,
    58,
    255,
    209,
    217,
    15,
    111,
    46,
    173,
    223,
    42,
    115,
    238,
    139,
    243,
    23,
    98,
    100,
    178,
    37,
    97,
    191,
    213,
    222,
    155,
    165,
    2,
    146,
    204,
    120,
    241,
    163,
    128,
    22,
    90,
    60,
    185,
    67,
    34,
    27,
    248,
    164,
    69,
    41,
    230,
    104,
    47,
    144,
    251,
    20,
    17,
    150,
    225,
    254,
    161,
    102,
    70,
]

# Generate Inverse S-box otomatis buat Dekripsi
inv_sbox_44 = [0] * 256
for i, val in enumerate(sbox_44):
    inv_sbox_44[val] = i

# ==========================================
# 2. LOGIKA ENKRIPSI + KUNCI USER
# ==========================================


def encrypt_with_key(plaintext, key):
    """Enkripsi pake S-box 44 DITAMBAH Key User"""
    if not key:
        return "Error: Kunci/Password nggak boleh kosong!"

    encrypted_bytes = []
    key_len = len(key)

    for i, char in enumerate(plaintext):
        # 1. Ambil karakter input dan karakter kunci
        char_val = ord(char)
        key_char = key[i % key_len]  # Ulangi kunci kalau teks lebih panjang
        key_val = ord(key_char)

        # 2. OPERASI XOR: Gabungin Input sama Kunci
        # Ini bikin huruf 'A' + Kunci 'B' hasilnya beda sama 'A' + Kunci 'C'
        mixed_val = char_val ^ key_val

        # 3. Substitusi pake S-box 44 (Biar makin acak)
        # Pake modulo 256 jaga-jaga kalau hasil XOR > 255
        final_val = sbox_44[mixed_val % 256]

        encrypted_bytes.append(final_val)

    # Jadiin Hex biar gampang dicopy
    return "".join([f"{b:02x}" for b in encrypted_bytes])


def decrypt_with_key(hex_string, key):
    """Dekripsi Hex balik ke teks asli, butuh Kunci yang SAMA"""
    if not key:
        return "Error: Kunci/Password nggak boleh kosong!"

    try:
        decrypted_chars = []
        key_len = len(key)

        # Proses Hex per 2 digit
        hex_index = 0
        for i in range(0, len(hex_string), 2):
            byte_hex = hex_string[i : i + 2]
            val = int(byte_hex, 16)

            # 1. Balikin substitusi S-box dulu (Inverse S-box)
            mixed_val = inv_sbox_44[val]

            # 2. Ambil karakter kunci yang sesuai urutan
            key_char = key[hex_index % key_len]
            key_val = ord(key_char)

            # 3. OPERASI XOR BALIKAN: Pisahin hasil S-box dari Kunci
            original_val = mixed_val ^ key_val

            decrypted_chars.append(chr(original_val))
            hex_index += 1

        return "".join(decrypted_chars)
    except Exception as e:
        return "Error: Format Hex salah atau Kunci nggak cocok!"


# ==========================================
# 3. TAMPILAN WEB (Streamlit)
# ==========================================

st.set_page_config(page_title="S-box 44 + User Key", page_icon="🔐")

st.title("🔐 Super S-box 44 Encryptor")
st.markdown(
    """
Aplikasi ini menggabungkan kekuatan **S-box 44** (dari paper riset) 
dengan **Kunci Rahasia (Password)** pilihanmu sendiri.
"""
)

# Input Kunci Rahasia (Global buat Encrypt & Decrypt)
st.sidebar.header("🔑 Pengaturan Kunci")
user_key = st.sidebar.text_input(
    "Masukin Password Rahasia:",
    type="password",
    help="Kunci ini wajib diingat buat buka pesan nanti!",
)

tab1, tab2 = st.tabs(["🔒 Enkripsi Pesan", "🔓 Dekripsi Pesan"])

with tab1:
    st.subheader("Buat Pesan Rahasia")
    plain_text = st.text_area("Tulis pesan lu di sini:")

    if st.button("Kunci Pesan Ini! 🔒"):
        if plain_text and user_key:
            cipher_result = encrypt_with_key(plain_text, user_key)
            st.success("Pesan berhasil diamankan!")
            st.code(cipher_result, language="text")
            st.info("Copy kode di atas. Orang lain gak bisa baca tanpa password lu.")
        elif not user_key:
            st.error("Woi, password-nya diisi dulu di menu sebelah kiri! 👈")
        else:
            st.warning("Tulis dulu pesannya, Bro.")

with tab2:
    st.subheader("Buka Pesan Rahasia")
    cipher_input = st.text_area("Tempel kode aneh (Hex) di sini:")

    if st.button("Buka Kunci! 🔓"):
        if cipher_input and user_key:
            # Hapus spasi iseng
            clean_hex = cipher_input.replace(" ", "").strip()
            decrypted_result = decrypt_with_key(clean_hex, user_key)

            if "Error" in decrypted_result:
                st.error(decrypted_result)
            else:
                st.success("Pesan Terbuka:")
                st.balloons()  # Efek asik
                st.write(f"Isi Pesan: **{decrypted_result}**")
        elif not user_key:
            st.error("Password-nya mana? Isi di sidebar kiri dulu! 👈")
        else:
            st.warning("Masukin dulu kode enkripsinya.")

st.markdown("---")
st.caption(
    "Implementation based on Modified AES S-box 44  combined with XOR Key Mixing."
)
