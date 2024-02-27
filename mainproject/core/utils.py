from .models import ImageHistory
from PIL import Image
import pytesseract
import requests
from io import BytesIO
# from io import Bytes
import matplotlib.pyplot as plt
import cv2
import numpy as np



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
            clean_text=self.format_text(text)
            self.save_image(imageObj, clean_text)
            return text
        except Exception as e:
            return e

    def get_box_from_image(self,request,id):
        imageObj = ImageHistory.objects.get(id=id)
        domain = f"{request.scheme}://{request.META['HTTP_HOST']}"

        image_url = domain+imageObj.image.url
        response = requests.get(image_url)
        response.raise_for_status()
        try:
            image = Image.open(BytesIO(response.content))
            
            gray_img=image.convert('L')
            np_img=np.array(gray_img)
            # plot the image
            
            boxes_data = pytesseract.image_to_boxes(image) 
            plt.figure(figsize=(10,10))
            plt.imshow(np_img)       
            for box in boxes_data.splitlines():
                  box = box.split()
                  x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
                  cv2.rectangle(np_img, (x, np_img.shape[0] - y), (w, np_img.shape[0] - h), (0, 255, 0), 2)

            plt.imshow(np_img)
            plt.axis('off')
            print("---------ploting---------")
            plt.show()
            plt.savefig('boxed.jpg');
   
            self.save_image(imageObj, boxes_data)
            return boxes_data
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
