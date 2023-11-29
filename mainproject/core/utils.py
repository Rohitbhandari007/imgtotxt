from .models import ImageHistory
from PIL import Image
import pytesseract
import requests
from io import BytesIO



class ConvertTextToImage:

    def get_text_from_image(self,request,id):
        imageObj = ImageHistory.objects.get(id=id)
        domain = f"{request.scheme}://{request.META['HTTP_HOST']}"

        image_url = domain+imageObj.image.url
        response = requests.get(image_url)
        response.raise_for_status()
        try:
            image = Image.open(BytesIO(response.content))
            text = pytesseract.image_to_string(image)

            imageObj.converted_text = text
            imageObj.is_converted= True
            imageObj.save()
            return text
        except Exception as e:
            return e
