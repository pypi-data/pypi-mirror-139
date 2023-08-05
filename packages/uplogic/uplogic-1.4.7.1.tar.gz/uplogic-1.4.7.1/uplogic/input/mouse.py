from math import pi
from bge import logic
from bge import events
from bge import render
from mathutils import Vector
from uplogic.utils import interpolate


MOUSE_EVENTS = logic.mouse.inputs
'''Reference to `bge.logic.mouse.inputs`
'''

LMB = events.LEFTMOUSE
RMB = events.RIGHTMOUSE
MMB = events.MIDDLEMOUSE


class ULMouseData():
    def __init__(self) -> None:
        self.position = get_mouse_position()
        self.movement = (0, 0)
        self.wheel = mouse_wheel()
        logic.getCurrentScene().post_draw.append(self.update)

    def update(self):
        old_pos = self.position
        new_pos = get_mouse_position()
        self.movement = (
            new_pos[0] - old_pos[0],
            new_pos[1] - old_pos[1]
        )
        self.position = new_pos
        self.wheel = mouse_wheel()

    def destroy(self):
        logic.getCurrentScene().post_draw.remove(self.update)


def set_mouse_position(x: int, y: int, absolute: bool = False):
    if absolute:
        render.setMousePosition(x, y)
        return
    render.setMousePosition(
        int(x * render.getWindowWidth()),
        int(y * render.getWindowHeight())
    )


def get_mouse_position(absolute: bool = False):
    pos = logic.mouse.position
    if absolute:
        return (
            int(pos[0] * render.getWindowWidth()),
            int(pos[1] * render.getWindowHeight())
        )
    return pos


def mouse_moved(tap: bool = False) -> bool:
    '''Detect mouse movement.

    :param tap: Only use the first consecutive `True` output

    :returns: boolean
    '''
    if tap:
        return (
            MOUSE_EVENTS[events.MOUSEX].activated or
            MOUSE_EVENTS[events.MOUSEY].activated
        )
    else:
        return (
            MOUSE_EVENTS[events.MOUSEX].active or
            MOUSE_EVENTS[events.MOUSEY].active or
            MOUSE_EVENTS[events.MOUSEX].activated or
            MOUSE_EVENTS[events.MOUSEY].activated
        )


def mouse_tap(button=events.LEFTMOUSE) -> bool:
    '''Detect mouse button tap.

    :param button: can be either `LMB`, `RMB` or `MMB` from `uplogic.input`

    :returns: boolean
    '''
    return (
        MOUSE_EVENTS[button].activated or
        MOUSE_EVENTS[button].activated
    )


def mouse_down(button=events.LEFTMOUSE) -> bool:
    '''Detect mouse button held down.

    :param button: can be either `LMB`, `RMB` or `MMB` from `uplogic.input`

    :returns: boolean
    '''
    return (
        MOUSE_EVENTS[button].active or
        MOUSE_EVENTS[button].activated or
        MOUSE_EVENTS[button].active or
        MOUSE_EVENTS[button].activated
    )


def mouse_up(button=events.LEFTMOUSE) -> bool:
    '''Detect mouse button released.

    :param button: can be either `LMB`, `RMB` or `MMB` from `uplogic.input`

    :returns: boolean
    '''
    return (
        MOUSE_EVENTS[button].released or
        MOUSE_EVENTS[button].released
    )


def mouse_wheel(tap: bool = False) -> int:
    '''Detect mouse wheel activity.

    :param tap: Only use the first consecutive `True` output

    :returns: -1 if wheel down, 0 if idle, 1 if wheel up
    '''
    if tap:
        return (
            MOUSE_EVENTS[events.WHEELUPMOUSE].activated -
            MOUSE_EVENTS[events.WHEELDOWNMOUSE].activated
        )
    else:
        return (
            (
                MOUSE_EVENTS[events.WHEELUPMOUSE].activated or
                MOUSE_EVENTS[events.WHEELUPMOUSE].active
            ) - (
                MOUSE_EVENTS[events.WHEELDOWNMOUSE].activated or
                MOUSE_EVENTS[events.WHEELDOWNMOUSE].active
            )
        )


class ULMouseLook():

    def __init__(
        self,
        obj,
        head=None,
        sensitivity=1.0,
        use_cap_x=False,
        cap_x=[0, 0],
        use_cap_y=False,
        cap_y=[-89, 89],
        invert=[False, True],
        smoothing=0.0,
        local=False,
        front=1
    ) -> None:
        self.obj = obj
        self.head = head
        self.sensitivity = sensitivity
        self.use_cap_x = use_cap_x
        self.cap_x = cap_x
        self.use_cap_y = use_cap_y
        self.cap_y = cap_y
        self.invert = invert
        self.smoothing = smoothing
        self.initialized = False
        self.active = True
        self.front = front
        self._x = 0
        self._y = 0
        self.local = local
        self.get_data()
        self.mouse.position = self.screen_center
        logic.getCurrentScene().post_draw.append(self.update)

    def get_data(self):
        self.x = render.getWindowWidth()//2
        self.y = render.getWindowHeight()//2
        self.screen_center = (
            self.x / render.getWindowWidth(),
            self.y / render.getWindowHeight()
        )
        self.center = Vector(self.screen_center)
        self.mouse = logic.mouse

    def update(self):
        self.get_data()
        if not self.active:
            self.initialized = False
        elif not self.initialized:
            self.mouse.position = self.screen_center
            self.initialized = True
            return
        game_object_x = self.obj
        game_object_y = self.head if self.head else self.obj
        sensitivity = self.sensitivity * 1000
        use_cap_x = self.use_cap_x
        use_cap_y = self.use_cap_y
        cap_x = self.cap_x
        lowercapX = cap_x[0] * pi / 180
        uppercapX = cap_x[1] * pi / 180
        cap_y = self.cap_y
        lowercapY = cap_y[0] * pi / 180
        uppercapY = cap_y[1] * pi / 180
        invert = self.invert
        smooth = 1 - (self.smoothing * .99)

        if self.active:
            mouse_position = Vector(self.mouse.position)
            offset = (mouse_position - self.center) * -0.002
        else:
            offset = Vector((0, 0))

        if invert[1] is False:
            offset.y = -offset.y
        if invert[0] is True:
            offset.x = -offset.x
        offset *= sensitivity

        self._x = offset.x = interpolate(self._x, offset.x, smooth)
        self._y = offset.y = interpolate(self._y, offset.y, smooth)

        if use_cap_x:
            objectRotation = game_object_x.localOrientation.to_euler()

            if objectRotation.z + offset.x > uppercapX:
                offset.x = 0
                objectRotation.z = uppercapX
                game_object_x.localOrientation = objectRotation.to_matrix()

            if objectRotation.z + offset.x < lowercapX:
                offset.x = 0
                objectRotation.z = lowercapX
                game_object_x.localOrientation = objectRotation.to_matrix()

        game_object_x.applyRotation((0, 0, offset.x), self.local)

        rot_axis = 1 - self.front
        if use_cap_y:
            objectRotation = game_object_y.localOrientation.to_euler()

            if objectRotation[rot_axis] + offset.y > uppercapY:
                objectRotation[rot_axis] = uppercapY
                game_object_y.localOrientation = objectRotation.to_matrix()
                offset.y = 0

            if objectRotation[rot_axis] + offset.y < lowercapY:
                objectRotation[rot_axis] = lowercapY
                game_object_y.localOrientation = objectRotation.to_matrix()
                offset.y = 0

        rot = [0, 0, 0]
        rot[1-self.front] = offset.y
        game_object_y.applyRotation((*rot, ), True)
        if self.mouse.position != self.screen_center and self.active:
            self.mouse.position = self.screen_center
        self.done = True

