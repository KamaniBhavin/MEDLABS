import io
import numpy as np
from PIL import Image
import torch
import os
from torchvision import models

def load_checkpoint(filepath):
    checkpoint = torch.load(filepath, map_location = torch.device("cpu"))
    
    model = models.densenet121(pretrained=True)
    for param in model.parameters():
        param.requires_grad = False
        
        
    model.class_to_idx = checkpoint['class_to_idx']
    
    model.classifier = checkpoint['classifier']
    
    model.load_state_dict(checkpoint['state_dict'])
    #print(model)
    return model

def preprocess_pipeline(image):
    #print(image.size)
    width, height = image.size
    
    if  width > height:
        image.thumbnail((width, 256))
    else:
        image.thumbnail((256, height))
    
    width, height = image.size

    #print(width, height)
    width, height = image.size
    left = (width - 224)/2
    bottom = (height - 224)/2
    right = left + 224
    top = bottom + 224

    crop_image=image.crop((left, bottom, right, top))
    #print(crop_image.size)
    np_image=np.array(crop_image)
    np_image=np_image.astype(np.float32)
    np_image=np_image/255
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225]) 
    new_image=(np_image-mean)/std
    
   
    pro_image=new_image.transpose((2,0,1))
    
    return pro_image

def prediction(image_bytes, topk=2):
    ab_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ab_path += "/account/checkpoint.pth"
    ab_path_checkpoint = ab_path
    model = load_checkpoint(ab_path_checkpoint)
    
    model.to('cpu')
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img=preprocess_pipeline(img)

    img = torch.from_numpy(img).type(torch.FloatTensor)
    img.unsqueeze_(0)
    output=model.forward(img)
    ps = torch.exp(output)


    probablity, index = torch.topk(ps, topk)
    index=index.numpy()
    index=index[0]
    probablity=probablity.detach().numpy()
    probablity=probablity[0]
    #print(probablity)
    #print(index)
    
    indices = {val: key for key, val in model.class_to_idx.items()}
    #print('indices', indices)
    top_labels = [indices[ind] for ind in index]
    #print(top_labels)
    #top_classes=[classes[key] for key in top_labels]
    #print(top_classes)

    return probablity, top_labels
