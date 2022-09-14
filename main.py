from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction


class EthUnitsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


def convert(vtype, val):
    if vtype == "wei":
        return val
    elif vtype == "gwei":
        return int(val * 1e9)
    elif vtype == "ether":
        return int(val * 1e18)


def format_results(val):
    return [
        ExtensionResultItem(
            name=str(val),
            description="wei",
            on_enter=CopyToClipboardAction(str(val)),
            highlightable=False,
            icon="eth.png",
        ),
        ExtensionResultItem(
            name=str(val / 1e9),
            description="gwei",
            on_enter=CopyToClipboardAction(str(val / 1e9)),
            highlightable=False,
            icon="eth.png",
        ),
        ExtensionResultItem(
            name=str(val / 1e18),
            description="ether",
            on_enter=CopyToClipboardAction(str(val / 1e18)),
            highlightable=False,
            icon="eth.png",
        )
    ]


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        argument = (event.get_argument() or '').encode('utf-8')
        keyword = event.get_keyword()

        keyword_id = keyword
        for kwId, kw in extension.preferences.items():
            if kw == keyword:
                keyword_id = kwId

        val = convert(keyword_id, float(argument))

        return RenderResultListAction(format_results(val))


if __name__ == '__main__':
    EthUnitsExtension().run()
