from transitions import Machine
from stonewave.sql.udtfs.protocol.fsm.apply.apply_function import ApplyOperator
from stonewave.sql.udtfs.protocol.fsm.base_function_fsm import BaseFunctionFsm
from stonewave.sql.udtfs.logger import logger


class ApplyFunctionFsm(BaseFunctionFsm):
    states = ["start", "wait_for_next", "end"]

    def __init__(self, func, batch_sender):
        BaseFunctionFsm.__init__(self, func, batch_sender)
        self.result = None
        self.machine = Machine(model=self, states=ApplyFunctionFsm.states, initial="start")

        self.machine.add_transition(
            trigger="apply",
            source="start",
            dest="wait_for_next",
            after="apply_params",
        )

        self.machine.add_transition(
            trigger="apply",
            source="wait_for_next",
            dest="wait_for_next",
            after="apply_params",
        )

        self.machine.add_transition(
            trigger="next",
            source="wait_for_next",
            dest="wait_for_next",
            after="send_next_batch",
        )

        self.machine.add_transition(trigger="end", source="*", dest="end", before="end_evaluation")

    def apply_params(self, params, respond):
        apply_op = ApplyOperator(self.func, params)
        self.result = apply_op.execute()
        self.send_next_batch(params, respond)

    def send_next_batch(self, params, respond):
        try:
            batch = next(self.result)
            self._batch_sender.send(batch, respond)
        except StopIteration:
            respond("end")

    def end_evaluation(self, params, respond):
        logger.debug("end apply func")
        self._clean_up()
        respond("finish")

    def _clean_up(self):
        self.result = None
        self._batch_sender = None
        self.machine = None
        BaseFunctionFsm._clean_up(self)
