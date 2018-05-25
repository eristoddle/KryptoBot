from .bot import Bot

class MultiBot(Bot):

    strategies = []

    def __init__(self, strategies, config=None):
        super().__init__(strategy=None, config=config)
        self.strategies = strategies

    # override this to inherit
    def __start(self):
        for st in self.strategies:
            st.add_session(self.session)
            st.add_keys(self.config['apis'])
            st.run_simulation()
            st.start()
