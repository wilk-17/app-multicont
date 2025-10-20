"""
Generate Secure Keys - Generador de claves secretas seguras
Genera JWT_SECRET_KEY y SECRET_KEY para configuración
"""
import secrets


def generate_secret_key():
    """
    Genera una clave secreta segura de 32 bytes (256 bits).
    URL-safe base64 encoded.
    """
    return secrets.token_urlsafe(32)


def generate_hex_key():
    """
    Genera una clave secreta en formato hexadecimal.
    """
    return secrets.token_hex(32)


if __name__ == "__main__":
    print("=" * 70)
    print(" GENERADOR DE CLAVES SECRETAS SEGURAS")
    print("=" * 70)
    print()
    print("Copiar estas claves al archivo .env:\n")
    
    print(f"JWT_SECRET_KEY={generate_secret_key()}")
    print(f"SECRET_KEY={generate_hex_key()}")
    
    print()
    print("=" * 70)
    print(" ⚠️  IMPORTANTE:")
    print(" - Nunca compartir estas claves")
    print(" - Nunca hacer commit de estas claves en Git")
    print(" - Usar claves diferentes para desarrollo y producción")
    print(" - Regenerar claves si se comprometen")
    print("=" * 70)
