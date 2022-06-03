# Pygame-Terraria
 Use pygame similar Terraria
 
## Test video
 https://blog.naver.com/arin12349/221587191262
 
## Manual
| Key | Action |
|---|------|
| W | Jump |
| A | Left |
| D | Right |
| Lclick | break |
| Rclick | build |
| Alt | show Range |
| number | inventory |
| v | all block +1 |

## block index
 | number | block |
 |---| --- |
 | 1 | air |
 | 2 | dirt|
 | 3 | grass |
 | 4 | cloud |
 

## Technologies
 ### Sprite
 ![image](https://user-images.githubusercontent.com/65750019/170968317-6c78dde0-d34f-4996-9df4-ca7c8bbb7335.png)
  
  Manage block image Sprite  
  Sprite is serialized images  
  block is 20 px * 20 px   
  slice each block can manage block easily  
  ``` PY
    strip = pygame.image.load("strip.png")
    image = pygame.Surface((20, 20))
    image.blit(sprite, (0,0), Rect(code * 20, 0, 20, 20))
    SURFACE.blit(image, (x, y))
  ```
 ### Move
  Check Character coordinate collision  
  If there is a block in the place it wants to move, it will not move.
  ``` PY
      def iscollide(self):
        tmpy = self.y
        blockx = int(self.x/50)
        for y in range(H):
            block = BLOCKS[y][blockx]
            if not block.code == 0:
                break
        tmp1 = block.y
        blockx = int((self.x+25)/50)
        for y in range(H):
            block = BLOCKS[y][blockx]
            if not block.code == 0:
                break
        tmp2 = block.y
        tmp1 = min(tmp1, tmp2)
        tmpy = tmp1 - 50
        return tmpy
  ```
  
 ### Customize map
  Map can easy to change  
  so adding random map easily
