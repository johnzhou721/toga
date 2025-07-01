from __future__ import annotations
from io import BytesIO
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from toga.images import BytesLikeT
try:
    import PIL.Image
    PIL_imported = True
except ImportError:
    PIL_imported = False
else:
    pass


class PILConverter:
    image_class = PIL.Image.Image if PIL_imported else None

    @staticmethod
    def convert_from_format(image_in_format: PIL.Image.Image) ->bytes:
        buffer = BytesIO()
        image_in_format.save(buffer, format='png', compress_level=0)
        return buffer.getvalue()

    @staticmethod
    def convert_to_format(data: BytesLikeT, image_class: type[PIL.Image.Image]
        ) ->PIL.Image.Image:
        buffer = BytesIO(data)
        with PIL.Image.open(buffer) as pil_image:
            pil_image.load()
        return pil_image
