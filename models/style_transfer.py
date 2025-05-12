import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from PIL import Image
import copy
from torchvision.models import VGG19_Weights

def load_image(image_path, max_size=512):
    image = Image.open(image_path).convert('RGB')

    size = min(max(image.size), max_size)
    in_transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x[:3, :, :]),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))
    ])

    image = in_transform(image).unsqueeze(0) 
    return image


def im_convert(tensor):
    """Zamienia tensor -> obraz PIL"""
    image = tensor.clone().detach().cpu().squeeze(0)
    image = image * torch.tensor([0.229, 0.224, 0.225]).view(3,1,1) + \
            torch.tensor([0.485, 0.456, 0.406]).view(3,1,1)
    image = image.clamp(0, 1)
    image = transforms.ToPILImage()(image)
    return image


def get_features(image, model, layers=None):
    if layers is None:
        layers = {
            '0': 'conv1_1',
            '5': 'conv2_1',
            '10': 'conv3_1',
            '19': 'conv4_1',
            '21': 'conv4_2',  
            '28': 'conv5_1'
        }

    features = {}
    x = image
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x
    return features


def gram_matrix(tensor):
    _, d, h, w = tensor.size()
    tensor = tensor.view(d, h * w)
    gram = torch.mm(tensor, tensor.t())
    return gram


def style_transfer(content_path, style_path, steps=300, style_weight=1e6, content_weight=1):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    content = load_image(content_path).to(device)
    
    
    style = load_image(style_path).to(device)

  

    vgg = models.vgg19(weights=VGG19_Weights.DEFAULT).features


    
    for param in vgg.parameters():
        param.requires_grad = False

    content_features = get_features(content, vgg)
    style_features = get_features(style, vgg)

    style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

    
    target = content.clone().requires_grad_(True).to(device)
    optimizer = optim.Adam([target], lr=0.003)

    for i in range(steps):
        target_features = get_features(target, vgg)

        content_loss = torch.mean((target_features['conv4_2'] - content_features['conv4_2'])**2)

        style_loss = 0
        for layer in style_grams:
            target_feature = target_features[layer]
            target_gram = gram_matrix(target_feature)
            style_gram = style_grams[layer]
            layer_loss = torch.mean((target_gram - style_gram)**2)
            b, c, h, w = target_feature.shape
            style_loss += layer_loss / (c * h * w)

        total_loss = content_weight * content_loss + style_weight * style_loss

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        if i % 50 == 0:
            print(f"🧠 Iteration {i}: total_loss = {total_loss.item():.2f}")


    return im_convert(target)
