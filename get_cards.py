import json
from PIL import Image
import numpy as np
WHITE=400
CARD_POSITION=[380+71*x for x in range(14)]
ALL_CARDS=['1m','2m','3m','4m','5m','6m','7m','8m','9m','1p','2p','3p','4p','5p','6p','7p','8p','9p','1s','2s','3s','4s','5s','6s','7s','8s','9s','1z','2z','3z','4z','5z','6z','7z']
lines={"top":937,"upper":942,"mid":956,"downward":976}
if __name__ == '__main__':
    cards_images={'m':[{},{},{},{},{},{},{},{},{}],'p':[{},{},{},{},{},{},{},{},{}],'s':[{},{},{},{},{},{},{},{},{}],'z':[{},{},{},{},{},{},{}]}
    reference=np.array(Image.open('screenshots/screenshot.png'))
    with open('cards.json', 'r') as openfile:
        # Reading from json file
        cards_images = json.load(openfile)
    cards=['4m','4m','8m','9m','1p','3p','3s','3s','4s','6s','7s','2z','5z']
    for card_idx in range(len(cards)):
        for line_name,line in lines.items():
            white_points=[]
            for x in range(CARD_POSITION[card_idx]+1,CARD_POSITION[card_idx+1]-3):
                if sum(reference[line][x])>WHITE:
                    white_points.append(x-CARD_POSITION[card_idx])
            cards_images[cards[card_idx][1]][int(cards[card_idx][0])-1][line_name]=white_points
    card_image_json=json.dumps(cards_images)
    with open("cards.json", "w") as outfile:
        outfile.write(card_image_json)
        