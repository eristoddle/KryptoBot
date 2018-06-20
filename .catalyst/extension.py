from catalyst.data.bundles.core import register_bundle
from catalyst.data.bundles.poloniex import PoloniexBundle
# from kryptobot.catalyst_extensions.bundles.bittrex import BittrexBundle

register_bundle(PoloniexBundle)
# register_bundle(BittrexBundle)
