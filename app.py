
import streamlit as st
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

st.set_page_config(
    page_title="Secure Text Encryption",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Secure Text Encryption")
st.write("Protect your messages using AES-256-GCM encryption.")
st.info("This application uses AES-256-GCM, a secure encryption algorithm, to protect text messages. Users can encrypt messages and decrypt them using the correct secret key.")

st.warning(
    "Keep your secret key private. Anyone with the key "
    "and encrypted message may decrypt your message."
)

st.header("1. Generate Security Key")
st.caption("Step 1: Generate and download your secret key. Keep it private because you will need it to decrypt your messages.")

if st.button("Generate Security Key"):
    key = AESGCM.generate_key(bit_length=256)
    encoded_key = base64.urlsafe_b64encode(key).decode()
    st.session_state["secret_key"] = encoded_key

if "secret_key" in st.session_state:
    st.success("Security key generated successfully!")
    st.download_button(
        "Download Secret Key",
        st.session_state["secret_key"],
        file_name="secret_key.txt"
    )

st.divider()

st.header("2. Encrypt Your Message")
st.caption("Step 2: Enter your message and click Encrypt Message to generate encrypted text.")

sample_message = "Welcome to our Secure Text Encryption System. This system protects messages using AES-256-GCM encryption."

message = st.text_area("Enter the message you want to encrypt", value=sample_message)

if st.button("Encrypt Message"):
    if "secret_key" not in st.session_state:
        st.error("Generate a security key first.")
    elif not message:
        st.error("Please enter a message.")
    else:
        try:
            key = base64.urlsafe_b64decode(
                st.session_state["secret_key"]
            )
            aes = AESGCM(key)
            nonce = os.urandom(12)

            encrypted = aes.encrypt(
                nonce, message.encode("utf-8"), None
            )

            result = base64.urlsafe_b64encode(
                nonce + encrypted
            ).decode()

            st.success("Message encrypted successfully!")
            st.code(result)
            st.download_button(
                "Download Encrypted Message",
                result,
                file_name="encrypted_message.txt"
            )
        except Exception as error:
            st.error(f"Encryption failed: {error}")

st.divider()

st.header("3. Decrypt Your Message")
st.caption("Step 3: Paste your encrypted message, enter the correct secret key, and click Decrypt Message to recover the original text.")

key_input = st.text_input(
    "Enter your secret key",
    type="password"
)

encrypted_input = st.text_area(
    "Paste your encrypted message"
)

if st.button("Decrypt Message"):
    try:
        key = base64.urlsafe_b64decode(key_input.strip())
        if len(key) != 32:
            raise ValueError("Invalid AES-256 key.")

        data = base64.urlsafe_b64decode(
            encrypted_input.strip()
        )

        nonce = data[:12]
        ciphertext = data[12:]

        aes = AESGCM(key)
        decrypted = aes.decrypt(nonce, ciphertext, None)

        st.success("Message decrypted successfully!")
        st.text_area(
            "Your Original Message",
            decrypted.decode("utf-8"),
            disabled=True
        )

    except Exception:
        st.error(
            "Decryption failed. Check your secret key "
            "and encrypted message."
        )

st.markdown("[View GitHub Repository](https://github.com/sserwaahagyei/BIT309-Assignment-3)")
st.caption("Information System Security - Assignment 3")
