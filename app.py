import streamlit as st

# ==========================================
# 1. DATA S-BOX 44
# ==========================================
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

inv_sbox_44 = [0] * 256
for i, val in enumerate(sbox_44):
    inv_sbox_44[val] = i

# ==========================================
# 2. HELPER FUNCTIONS (128-bit Logic)
# ==========================================


def pad_text(text):
    """Bikin teks jadi kelipatan 16 byte (Blok AES)"""
    while len(text) % 16 != 0:
        text += " "  # Tambah spasi sampe pas bloknya
    return text


def fix_key_128bit(key):
    """
    MEMAKSA Kunci jadi 128 bit (16 Karakter).
    Sesuai diagram 'Kunci AES 128 bit'.
    """
    if len(key) > 16:
        return key[:16]  # Kalau kepanjangan, potong.
    while len(key) < 16:
        key += "#"  # Kalau kependekan, tambah karakter pagar '#'
    return key


# ==========================================
# 3. EMPAT FUNGSI UTAMA (Sub, Shift, Mix, Add)
# ==========================================


def sub_bytes(state, sbox):
    return [sbox[b] for b in state]


def shift_rows(state):
    # Simulasi geser baris
    new_state = state[:]
    # Swap simple simulasi shift matrix
    new_state[1], new_state[5], new_state[9], new_state[13] = (
        state[5],
        state[9],
        state[13],
        state[1],
    )
    return new_state


def inv_shift_rows(state):
    new_state = state[:]
    new_state[5], new_state[9], new_state[13], new_state[1] = (
        state[1],
        state[5],
        state[9],
        state[13],
    )
    return new_state


def simple_mix(state):
    # Simplified MixColumns (Reversible XOR Neighbor)
    new_s = state[:]
    for i in range(0, 16, 2):
        new_s[i] = new_s[i] ^ new_s[i + 1]
    return new_s


def inv_simple_mix(state):
    # Kebalikan dari simple_mix
    new_s = state[:]
    for i in range(0, 16, 2):
        new_s[i] = new_s[i] ^ new_s[i + 1]
    return new_s


def add_round_key(state, key_bytes):
    # XOR dengan kunci 128-bit
    return [b ^ key_bytes[i] for i, b in enumerate(state)]


# ==========================================
# 4. LOGIKA UTAMA (ENKRIPSI & DEKRIPSI)
# ==========================================


def encrypt_final(plaintext, key):
    # 1. Pastikan Kunci 128 bit (16 char)
    real_key = fix_key_128bit(key)
    key_bytes = [ord(k) for k in real_key]

    # 2. Siapkan Plaintext (Padding biar 16 byte)
    padded_text = pad_text(plaintext)
    state = [ord(c) for c in padded_text]

    # 3. Proses per Blok 16 byte (Kalo teks panjang)
    ciphertext_hex = ""

    # Loop per blok 16 byte
    for i in range(0, len(state), 16):
        block = state[i : i + 16]

        # --- INITIAL ROUND ---
        block = add_round_key(block, key_bytes)

        # --- 9 ROUNDS ---
        for _ in range(9):
            block = sub_bytes(block, sbox_44)
            block = shift_rows(block)
            block = simple_mix(block)
            block = add_round_key(block, key_bytes)

        # --- FINAL ROUND ---
        block = sub_bytes(block, sbox_44)
        block = shift_rows(block)
        block = add_round_key(block, key_bytes)

        # Gabung hasil hex
        ciphertext_hex += "".join([f"{b:02x}" for b in block])

    return ciphertext_hex


def decrypt_final(hex_string, key):
    try:
        real_key = fix_key_128bit(key)
        key_bytes = [ord(k) for k in real_key]

        state_all = [
            int(hex_string[i : i + 2], 16) for i in range(0, len(hex_string), 2)
        ]
        plaintext_res = ""

        # Loop per blok 16 byte
        for i in range(0, len(state_all), 16):
            block = state_all[i : i + 16]

            # --- INVERSE FINAL ROUND ---
            block = add_round_key(block, key_bytes)
            block = inv_shift_rows(block)
            block = sub_bytes(block, inv_sbox_44)

            # --- INVERSE 9 ROUNDS ---
            for _ in range(9):
                block = add_round_key(block, key_bytes)
                block = inv_simple_mix(block)
                block = inv_shift_rows(block)
                block = sub_bytes(block, inv_sbox_44)

            # --- INVERSE INITIAL ROUND ---
            block = add_round_key(block, key_bytes)

            plaintext_res += "".join([chr(b) for b in block])

        return plaintext_res.strip()  # Hapus spasi padding
    except:
        return "Error: Kunci salah atau Hex rusak!"


# ==========================================
# 5. UI STREAMLIT
# ==========================================
st.set_page_config(page_title="AES 128-bit Demo", page_icon="🔐")

st.title("🔐 AES-Like 128-bit Encryptor")
st.info(
    "Menggunakan S-box 44 dengan standar kunci 128-bit (16 Karakter) sesuai diagram AES."
)

# INPUT KEY
raw_key = st.text_input(
    "🔑 Masukkan Password:", type="password", help="Otomatis dijadikan 16 karakter."
)

# Tampilkan status kunci biar user tau
if raw_key:
    final_key = fix_key_128bit(raw_key)
    st.caption(
        f"Status Kunci: '{raw_key}' → Diubah jadi 128-bit: `{final_key}` (Panjang: {len(final_key)} char)"
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enkripsi")
    txt = st.text_input("Pesan:")
    if st.button("Enkripsi"):
        if txt and raw_key:
            res = encrypt_final(txt, raw_key)
            st.success("Ciphertext:")
            st.code(res)
        else:
            st.warning("Password wajib diisi!")

with col2:
    st.subheader("Dekripsi")
    hex_in = st.text_input("Ciphertext (Hex):")
    if st.button("Dekripsi"):
        if hex_in and raw_key:
            res = decrypt_final(hex_in, raw_key)
            st.success("Pesan Terbuka:")
            st.write(f"**{res}**")
        else:
            st.warning("Password wajib diisi!")
