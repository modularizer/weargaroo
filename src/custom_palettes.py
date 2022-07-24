from components.display.colors import ColorPalette


class CustomColors(object):
    # 2/dark
    cafe_noir = 0x4e3b2d
    deep_champagne = 0xedcb96

    # 3/light
    lavendar_blue = 0xedcb96
    gainsboro = 0xe4dde3

    # 4/info
    steel_teal = 0x488286
    viridian_green = 0x129490

    # 5/warning
    cerise = 0xd73364
    china_pink = 0xe56399


class CustomPalettes(object):
    brown_rose = ColorPalette(
                    'black',
                    'white',
                    CustomColors.cafe_noir,
                    CustomColors.deep_champagne,
                    CustomColors.gainsboro,
                    CustomColors.viridian_green,
                    CustomColors.china_pink
                )