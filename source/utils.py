def create_template_dict():
    templateDict = {}

    x = -1
    while x < 2:
        y = -x

        # =========================
        # WIN 4
        # =========================
        templateDict[(x, x, x, x)] = 1000000 * x

        # =========================
        # LIVE 3 (hở 2 đầu)
        # 0 xxx 0
        # =========================
        templateDict[(0, x, x, x, 0)] = 100000 * x

        # Các biến thể live 3
        templateDict[(0, x, x, 0, x, 0)] = 100000 * x
        templateDict[(0, x, 0, x, x, 0)] = 100000 * x

        # =========================
        # GO 3 (hở 1 đầu)
        # =========================
        templateDict[(y, x, x, x, 0)] = 10000 * x
        templateDict[(0, x, x, x, y)] = 10000 * x

        templateDict[(y, x, x, 0, x, 0)] = 10000 * x
        templateDict[(0, x, 0, x, x, y)] = 10000 * x

        #==========================
        #==========================
        #them
        templateDict[(y, x, x, x, 0,y)] = 500000 * x
        templateDict[(y, x, x, 0, x,y)] = 500000 * x
        templateDict[(y, x, 0, x, x,y)] = 500000 * x
        templateDict[(y, 0, x, x, x,y)] = 500000 * x
        # =========================

        # =========================
        # DEAD 3
        # =========================
        templateDict[(y, x, x, x, y)] = -100 * x

        # =========================
        # LIVE 2
        # =========================
        templateDict[(0, x, x, 0)] = 1000 * x
        templateDict[(0, x, 0, x, 0)] = 1000 * x

        # =========================
        # SLEEP 2
        # =========================
        templateDict[(y, x, x, 0)] = 100 * x
        templateDict[(0, x, x, y)] = 100 * x

        templateDict[(y, x, 0, x, 0)] = 100 * x
        templateDict[(0, x, 0, x, y)] = 100 * x

        # =========================
        # DEAD 2
        # =========================
        templateDict[(y, x, x, y)] = -10 * x
        x += 2
    return templateDict
