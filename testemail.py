import smtplib
import ssl

print("Testing Gmail SMTP connection on port 465...")
try:
    # Create SSL context
    context = ssl.create_default_context()

    # Try to connect to Gmail on port 465 (SSL)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5, context=context)
    print("✅ Connected to smtp.gmail.com:465 (SSL)")

    # Try login
    server.login("optimalsesleads@gmail.com", "amll cael qbbk zfdw")
    print("✅ Login successful!")

    server.quit()
    print("✅ All tests passed!")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
