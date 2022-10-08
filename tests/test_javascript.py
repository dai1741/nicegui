from datetime import datetime

from nicegui import ui
from nicegui.events import ValueChangeEventArguments

from .screen import Screen


def test_executing_javascript_on_button_press(screen: Screen):
    async def set_title() -> None:
        await ui.run_javascript('document.title = "A New Title"')
    ui.button('change title', on_click=set_title)

    screen.open('/')
    assert screen.selenium.title == 'NiceGUI'
    screen.click('change title')
    assert screen.selenium.title == 'A New Title'
    assert screen.selenium.title != 'NiceGUI'


def test_executing_javascript_on_value_change(screen: Screen):
    async def set_title(e: ValueChangeEventArguments) -> None:
        await ui.run_javascript(f'document.title = "{e.value}"')
    radio = ui.radio(['Page Title A', 'Page Title B'], on_change=set_title)
    # NOTE setting the value here will trigger on_change before the page is opened, so js needs to hold back until the page is loaded
    radio.value = 'Initial Page Title'

    screen.open('/')
    screen.wait(0.3)
    assert screen.selenium.title == 'Initial Page Title'
    screen.click('Title B')
    screen.wait(0.3)
    assert screen.selenium.title == 'Page Title B'
    screen.click('Title A')
    screen.wait(0.3)
    assert screen.selenium.title == 'Page Title A'


def test_retrieving_content_from_javascript(screen: Screen):
    async def write_time() -> None:
        response = await ui.await_javascript('Date.now()')
        ui.label(f'Browser time: {response}')

    ui.button('write time', on_click=write_time)

    screen.open('/')
    screen.click('write time')
    label = screen.find('Browser time').text
    js_time = datetime.fromtimestamp(int(label.split(': ')[1]) / 1000)
    assert abs((datetime.now() - js_time).total_seconds()) < 1, f'{js_time} should be close to now'
