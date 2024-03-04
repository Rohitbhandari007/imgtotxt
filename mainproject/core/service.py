from .models import ImageHistory
from PIL import Image
import requests
from io import BytesIO
# from io import Bytes
import matplotlib.pyplot as plt
import numpy as np
# from ...trained_model.script import useModal
import pytesseract



class ConvertTextToImage:

    def get_text_from_image(self,request,id):
        imageObj = ImageHistory.objects.get(id=id)
        domain = f"{request.scheme}://{request.META['HTTP_HOST']}"

        image_url = domain+imageObj.image.url
        response = requests.get(image_url)
        
        response.raise_for_status()
        try:
            image = Image.open(BytesIO(response.content))
            text = useModal(image)        
            clean_text=self.format_text(text)
            self.save_image(imageObj, clean_text)
            return text
        except Exception as e:
            return e

    def format_text(self, text):
        # Split the text into paragraphs
        formatted_text = [p.strip() for p in text.strip().split('\n\n')]
        # Join the paragraphs into a single string
        joined_text = ' '.join(formatted_text)
        # Split the joined text by commas and remove leading/trailing whitespace
        cleaned_list = [item.strip() for item in joined_text.split(',')]

        return cleaned_list

    
    def save_image(self,imageObj,clean_text):
        imageObj.converted_text = clean_text
        imageObj.is_converted= True
        imageObj.save()




























           
   