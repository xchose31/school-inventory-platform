import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv


load_dotenv()


def generate_qr_code(id):
    qr_dir = "qrcodes"
    os.makedirs(qr_dir, exist_ok=True)
    url = f"http://{os.getenv("FLASK_RUN_HOST")}:{os.getenv("FLASK_RUN_PORT")}/equipment/{id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.convert("RGB")
    qr_width, qr_height = qr_img.size
    text = f"Оборудование ID: {id}"
    font_size = 24
    padding_top = 30
    padding_bottom = 40
    padding_sides = 40
    font = None
    try:
        font_paths = [
            "arial.ttf",
            "arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/arialbd.ttf"
        ]
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
    except:
        pass
    if font is None:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    draw_temp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    text_bbox = draw_temp.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    total_width = max(qr_width, text_width) + 2 * padding_sides
    total_height = qr_height + text_height + padding_top + padding_bottom
    result_img = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(result_img)
    qr_x = (total_width - qr_width) // 2
    qr_y = padding_top
    result_img.paste(qr_img, (qr_x, qr_y, qr_x + qr_width, qr_y + qr_height))  # Явно указываем координаты
    text_x = (total_width - text_width) // 2
    text_y = qr_y + qr_height + padding_bottom - 10
    draw.text((text_x, text_y), text, font=font, fill='black')
    border_thickness = 2
    draw.rectangle(
        [(border_thickness, border_thickness),
         (total_width - border_thickness - 1, total_height - border_thickness - 1)],
        outline='gray',
        width=border_thickness
    )
    qr_path = os.path.join(qr_dir, f"qr_{id}.png")
    result_img.save(qr_path, quality=95)