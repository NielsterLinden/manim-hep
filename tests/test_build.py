from __future__ import annotations

import numpy as np
import pytest
from manim import Circle, Dot, Mobject, Scene, Square, ValueTracker

from manim_hep.build import add_state, check_order, place


def _state():
    return {"back": Square(2), "mid": Circle(0.5), "top": Dot()}


def test_add_state_adds_in_dict_order_and_returns_the_state():
    scene = Scene()
    state = add_state(scene, _state)
    assert scene.mobjects == list(state.values())
    same = _state()
    assert add_state(Scene(), same) is same


def test_add_state_rejects_non_dicts():
    with pytest.raises(TypeError, match="dict of mobjects"):
        add_state(Scene(), lambda: [Square()])


def test_check_order_passes_and_ignores_placeholders_and_trackers():
    scene = Scene()
    state = add_state(scene, _state)
    scene.add(Mobject(), ValueTracker(1.0))  # what wait() and trackers leave behind
    check_order(scene, state)
    check_order(scene, list(state.values()))


def test_check_order_catches_a_swap():
    scene = Scene()
    state = _state()
    scene.add(state["mid"], state["back"], state["top"])
    with pytest.raises(AssertionError, match=r"draws \['mid', 'back', 'top'\]"):
        check_order(scene, state)


def test_check_order_catches_a_stray_mobject():
    scene = Scene()
    state = add_state(scene, _state)
    scene.add(Square())
    with pytest.raises(AssertionError, match="<Square>"):
        check_order(scene, state)


def test_check_order_uses_z_index():
    scene = Scene()
    state = _state()
    state["back"].set_z_index(-1)
    scene.add(state["mid"], state["back"], state["top"])
    check_order(scene, state)


def test_check_order_sorts_the_expected_state_by_z_index_too():
    scene = Scene()
    state = {"a": Square(), "top": Circle().set_z_index(1), "c": Dot()}
    add_state(scene, state)
    check_order(scene, state)  # drawn as a, c, top


def test_place_point_and_scaled_placement():
    sq = place(Square(1), (2, 1))
    assert np.allclose(sq.get_center(), [2, 1, 0])
    c = place(Circle(radius=1), (0.5, (3.0, -1.0)))
    assert np.allclose(c.get_center(), [3, -1, 0])
    assert c.width == pytest.approx(1.0)
    with pytest.raises(ValueError, match="2D or 3D point"):
        place(Square(), (1, 2, 3, 4))


def test_check_order_ignores_empty_groups_and_trackers_on_both_sides():
    from manim import VGroup

    scene = Scene()
    state = {"sq": Square(), "slot": VGroup(), "t": ValueTracker(0)}
    add_state(scene, state)
    check_order(scene, state)
