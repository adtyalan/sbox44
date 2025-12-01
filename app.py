import streamlit as st

# ==========================================
# 1. DATABASE S-BOX 44 (Jantungnya nih!)
# ==========================================
# Data ini diambil mentah dari Table 16 di artikel (Proposed S-box 44)
# Ini adalah "peta" pengganti huruf biar jadi sandi.
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

# Generate Inverse S-box (Buat Dekripsi) secara otomatis
# Karena S-box itu bijective (unik), kita bisa balik logic-nya
inv_sbox_44 = [0] * 256
for i, val in enumerate(sbox_44):
    inv_sbox_44[val] = i

# ==========================================
# 2. FUNGSI LOGIKA (The Brain)
# ==========================================


def encrypt_text(plaintext):
    """Mengubah teks biasa jadi Hexadecimal pake S-box 44"""
    encrypted_bytes = []
    for char in plaintext:
        # 1. Ubah huruf ke angka ASCII (0-255)
        val = ord(char)
        # 2. Substitusi pake S-box 44
        # (Kalau val > 255 misal emoji, kita modulo 256 biar aman)
        sub_val = sbox_44[val % 256]
        encrypted_bytes.append(sub_val)

    # 3. Ubah jadi Hex biar kelihatan keren kayak 'A4 5F'
    return "".join([f"{b:02x}" for b in encrypted_bytes])


def decrypt_text(hex_string):
    """Mengubah Hexadecimal balik ke teks asli pake Inverse S-box 44"""
    try:
        decrypted_chars = []
        # 1. Potong string hex per 2 digit (misal: 'a45f' jadi 'a4', '5f')
        for i in range(0, len(hex_string), 2):
            byte_hex = hex_string[i : i + 2]
            val = int(byte_hex, 16)  # Ubah hex ke angka

            # 2. Balikin nilainya pake Inverse S-box
            orig_val = inv_sbox_44[val]

            # 3. Ubah angka balik ke huruf
            decrypted_chars.append(chr(orig_val))
        return "".join(decrypted_chars)
    except Exception as e:
        return "Error: Format Hex salah, Bro! Cek lagi inputnya."


# ==========================================
# 3. TAMPILAN WEB (Streamlit UI)
# ==========================================

st.set_page_config(page_title="S-box 44 Cipher", page_icon="🔐")

st.title("🔐 S-box 44 Encryption App")
st.write(
    "Web app simpel buat **Enkripsi & Dekripsi** pake algoritma **S-box 44** dari paper penelitian terbaru."
)
st.caption("Based on 'AES S-box modification uses affine matrices exploration' [2025].")

# Bikin Tab biar rapi
tab1, tab2 = st.tabs(["🔒 Enkripsi", "🔓 Dekripsi"])

with tab1:
    st.header("Enkripsi Data")
    text_input = st.text_area("Masukin Pesan Rahasia Lu:", "Halo Dunia")

    if st.button("Enkripsi Sekarang! 🚀"):
        if text_input:
            result = encrypt_text(text_input)
            st.success("Berhasil Dienkripsi!")
            st.code(result, language="text")
            st.write("Simpen kode di atas, itu pesan rahasia lu.")
        else:
            st.warning("Isi dulu pesannya dong.")

with tab2:
    st.header("Dekripsi Data")
    hex_input = st.text_area("Masukin Kode Hex (Hasil Enkripsi):")

    if st.button("Buka Pesan! 🔓"):
        if hex_input:
            # Bersihin spasi kalau user iseng masukin spasi
            clean_hex = hex_input.replace(" ", "")
            result = decrypt_text(clean_hex)

            if "Error" in result:
                st.error(result)
            else:
                st.success("Pesan Terbuka:")
                st.balloons()
                st.write(f"**{result}**")
        else:
            st.warning("Masukin dulu kodenya, Bro.")

st.markdown("---")
st.write(
    "Dibuat dengan 💻 & ☕ | S-box 44 Strength Value: **16.0031** (Lebih kuat dari AES standar!)"
)
