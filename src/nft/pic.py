import io
from nftpics import NFTPics

pics = NFTPics()

image = None
with open('assets/trap.png', 'rb') as f:
    image = f.read()

image = pics.resize(image)

password = 'password'

with open('dat/pic.enc.png', 'wb') as f:
    f.write(pics.encrypt(image, password))

with open('dat/pic.blur.png', 'wb') as f:
    f.write(pics.blur(image))

# from PIL import Image
# with open('dat/pic.blur.png', 'rb') as f:
#     Image.open(f).show()

# with open('dat/pic.png.enc', 'rb') as f:
#     Image.open(f(decrypt((image), password))).show()
with open('dat/pic.enc.png', 'rb') as f:
    with open('dat/pic.dec.png', 'wb') as g:
        g.write(pics.decrypt(f.read(), password))

with open('dat/pic.blur.watermark.png', 'wb') as f:
    f.write(pics.watermark(pics.darken(pics.blur(image)), 'Доступно только\nдля пользователей VK NFT', font_size=53))
