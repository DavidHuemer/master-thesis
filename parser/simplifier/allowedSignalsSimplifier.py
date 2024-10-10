import parser.generated.JMLParser as JMLParser


class AllowedSignalsSimplifier:
    @staticmethod
    def simplify(signals_only: JMLParser.JMLParser.Signals_only_conditionContext):
        signals = signals_only.signals

        signal_children = signals.children
        filtered_signals = [signal.getText() for signal in signal_children if signal.getText() != ","]

        return filtered_signals
