import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile

import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

TOKEN = 'YOUR-TOKEN'


def generate_image_with_text(image_path: str, text: str) -> str:
    IMAGE_TARGET_WIDTH = 320
    IMAGE_TARGET_HEIGHT = 180

    NEW_IMAGE_WIDTH = IMAGE_TARGET_WIDTH
    NEW_IMAGE_HEIGHT = IMAGE_TARGET_HEIGHT + 50

    image = Image.open(image_path)

    image = image.resize((IMAGE_TARGET_WIDTH * 10, IMAGE_TARGET_HEIGHT * 10))

    font = ImageFont.truetype("VKSansDisplay-Bold.ttf", 200, encoding="unic")

    # Create a new image with the same width and height as the original image
    new_image = Image.new('RGB', (NEW_IMAGE_WIDTH * 10, NEW_IMAGE_HEIGHT * 10), (0, 0, 0))

    # Paste the original image onto the new image
    new_image.paste(image)

    # Create a drawing object
    draw = ImageDraw.Draw(new_image)

    # Draw text on the image
    draw.text((100, IMAGE_TARGET_HEIGHT * 10 + 50), text, (101, 142, 204), font=font)

    # Add ellipse
    draw.ellipse((
        IMAGE_TARGET_WIDTH * 10 - 1000, IMAGE_TARGET_HEIGHT * 10 - 500, IMAGE_TARGET_WIDTH * 10 - 100,
        IMAGE_TARGET_HEIGHT * 10 - 50
    ), fill=(0, 0, 0))

    # write 18+ in the ellipse
    font = ImageFont.truetype("VKSansDisplay-Bold.ttf", 250, encoding="unic")
    draw.text((IMAGE_TARGET_WIDTH * 10 - 750, IMAGE_TARGET_HEIGHT * 10 - 450), "18+", (255, 255, 255), font=font)

    new_image = new_image.filter(ImageFilter.GaussianBlur(10))

    new_image = new_image.resize((NEW_IMAGE_WIDTH, NEW_IMAGE_HEIGHT))

    # Save the new image
    new_image_path = f'generated_{os.path.basename(image_path)}'
    new_image.save(new_image_path)

    return new_image_path


bot = Bot(token=TOKEN)
dp = Dispatcher()


# If bot receives a photo with a caption, it will generate a new image with the caption
@dp.message(F.photo)
async def process_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file_name = f"photo_{message.photo[-1].file_id}.jpg"
    text = message.caption if message.caption else ""

    await message.bot.download(file=file_id, destination=file_name)

    new_image_path = generate_image_with_text(file_name, text)

    await message.reply_photo(FSInputFile(new_image_path), filename="new_image.jpg")

    os.remove(file_name)
    os.remove(new_image_path)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
