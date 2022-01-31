import os
import sys
import pygame
import requests


def load_file(response_content):
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response_content)
    file.close()
    return map_file


def geocode_request(delta):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
                       "=Москва&format=json"
    geo_response = requests.get(geocoder_request)
    jsn = geo_response.json()

    longitude, latitude = jsn["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point'][
        'pos'].split()
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&spn={delta},{delta}&l=map"
    response = requests.get(map_request)
    return load_file(response.content)


delta = 0.1
pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))

screen.blit(pygame.image.load(geocode_request(delta)), (0, 0))
pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if delta > 0.001:
                    delta /= 2
            if event.key == pygame.K_PAGEDOWN:
                if delta < 51:
                    delta *= 2
            response_content = geocode_request(delta)
            screen.blit(pygame.image.load(geocode_request(delta)), (0, 0))
    pygame.display.flip()
pygame.quit()