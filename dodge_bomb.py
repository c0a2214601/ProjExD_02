import random
import sys


import pygame as pg


delta = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0)
        }


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内かそうでないかを判定し、真理値タプルを返す関数
    引数１：画面SurfaceのRect
    引数２：こうかとんまたは爆弾SurfaceのRect
    戻り値：横方向縦方向のはみ出し検知
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))  #練習1
    x, y = random.randint(0, 1600), random.randint(0, 900)
    #screen.blit(bb_img, [x, y])  #練習2
    vx, vy = +1, +1
    bb_rect = bb_img.get_rect()
    bb_rect.center = x, y  #練習3
    tmr = 0
    tr = True
    gotmr = 0
    go_img = pg.transform.rotozoom(kk_img, 180, 1.0)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1

        key_lst = pg.key.get_pressed()
        """
        if key_lst[pg.K_RIGHT]:
            kk_img = pg.transform.flip(kk_img, True, False)
        elif key_lst[pg.K_UP] and key_lst[pg.K_RIGHT]:
            kk_img = pg.transform.flip(kk_img, True, False)
            kk_img = pg.transform.rotozoom(kk_img, 45, 1.0)
        elif key_lst[pg.K_UP]:
            kk_img = pg.transform.flip(kk_img, True, False)
            kk_img = pg.transform.rotozoom(kk_img, 90, 1.0)
        elif key_lst[pg.K_DOWN] and key_lst[pg.K_RIGHT]:
            kk_img = pg.transform.flip(kk_img, True, False)
            kk_img = pg.transform.rotozoom(kk_img, 315, 1.0)
        elif key_lst[pg.K_DOWN]:
            kk_img = pg.transform.flip(kk_img, True, False)
            kk_img = pg.transform.rotozoom(kk_img, 270, 1.0)
        elif key_lst[pg.K_UP] and key_lst[pg.K_LEFT]:
            kk_img = pg.transform.rotozoom(kk_img, 315, 1.0)
        elif key_lst[pg.K_LEFT]:
            kk_img = pg.transform.rotozoom(kk_img, 45, 1.0)
        """
        
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bb_rect.move_ip(vx, vy)
        yoko, tate = check_bound(screen.get_rect(), bb_rect)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rect)
        if kk_rct.colliderect(bb_rect):
            tr = False
        if not tr:
            screen.blit(go_img, (900, 400))
            gotmr += 1
            if gotmr >= 500:
                return
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()