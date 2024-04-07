from datetime import datetime
from rich.live import Live
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from time import sleep
from weatherpy.table.shortTermForecast import tableSTFcst

console = Console()

def make_layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    return layout

def make_st_fcst_panel() -> Panel:
    st_fcst_table = tableSTFcst()
    st_fcst_panel = Panel(
        Align.center(
            Group("\n", Align.center(st_fcst_table)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="단기 예보 조회",
        border_style="bright_blue",
    )
    return st_fcst_panel

class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]WeatherPy[/b] - 날씨 조회 프로그램",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")

layout = make_layout()
layout["header"].update(Header())
layout["body"].update(Panel('', title='날씨 정보 조회', border_style="blue"))
layout['side'].update(Panel('', title="단기 예보 조회", border_style="blue"))
layout["footer"].update(Panel('ChatGPT AI 추천', border_style="blue"))

with Live(layout, refresh_per_second=1, screen=True) as live:
    while True:
        try:
            new_panel = make_st_fcst_panel()
            layout['side'].update(new_panel)
        except Exception as e:
            old_panel = layout['side'].renderable
            old_panel.title = f'단기 예보 조회'
            old_panel.subtitle = f'에러 발생: {e}'
            old_panel.border_style = 'red'
            layout["side"].update(old_panel)
        sleep(4)
