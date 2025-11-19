import os
import qrcode


def generate_qr_code(id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qr_dir = os.path.join(base_dir, "qrcodes")
    os.makedirs(qr_dir, exist_ok=True)

    url = f"http://192.168.0.16:5000/equipment/{id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(qr_dir, f"qr_{id}.png")
    img.save(qr_path)
