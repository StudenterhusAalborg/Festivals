from django import template

from northern_winter_beat.models import Artist

register = template.Library()


@register.filter
def artist_background_color(offset: int) -> str:
    """
    returns a string for the class of a given artist on the front page.
    This gives a color (sand, blue, blue-dark) plus
     a rotation (r-1 -> r-5 (between 1 and 5 degrees) to either -r (right) or left)
    :param offset: an integer that is used to generate the background stuff
    :return:
    """
    try:
        # random list that makes the colors look sorta random
        colors = ["blue", "blue-dark", "sand", "blue-dark", "blue-dark", "blue", "sand", "sand", "blue"]
        return colors[offset % len(colors)] + f" r-{1+offset % 5}" + ("-r" if offset % 2 else "")
    except:
        pass
    return "sand"
