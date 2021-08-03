from task_builder import *

class TaskStructure:
	def load():
		shape_list = [StimShape.RECT, StimShape.CIRCLE]
		timeout_list = [2, 4, 6]
		blue = [0, 0, 1]
		red = [1, 0, 0]
		yellow = [1, 1, 0]
		P1 = StimParam(Param.SHAPE, ParamType.PSEUDORANDOM)
		P2 = StimParam(Param.TIMEOUT, ParamType.PSEUDORANDOM)
		params = [P1, P2]
		
		w1 = Window('on_release', [PseudoStim(P1, [
												StimParam(Param.POSITION, 
													ParamType.CONSTANT, 
													[0, 0]),
												StimParam(Param.COLOR,
													ParamType.CONSTANT,
													yellow),
												StimParam(Param.WIDTH,
													ParamType.CONSTANT,
													200),
												StimParam(Param.HEIGHT,
													ParamType.CONSTANT,
													200),
												StimParam(Param.RADIUS,
													ParamType.CONSTANT,
													100)
												]
							)]
		)
		w2 = Window('blank', [], [ StimParam(Param.TIMEOUT, ParamType.CONSTANT, 2) ])
		w3 = Window('on_click', [PseudoStim(P1, [
												StimParam(Param.POSITION, 
													ParamType.CONSTANT, 
													[0, 0]),
												StimParam(Param.COLOR,
													ParamType.CONSTANT,
													yellow),
												StimParam(Param.WIDTH,
													ParamType.CONSTANT,
													200),
												StimParam(Param.HEIGHT,
													ParamType.CONSTANT,
													200),
												StimParam(Param.RADIUS,
													ParamType.CONSTANT,
													100)
												]
							)]
		)
		w4 = Window('blank', [], [P2])
		w5 = Window('on_release', [PseudoStim(P1, [
												StimParam(Param.POSITION, 
													ParamType.CONSTANT, 
													[-300, 0]),
												StimParam(Param.COLOR,
													ParamType.CONSTANT,
													yellow),
												StimParam(Param.WIDTH,
													ParamType.CONSTANT,
													200),
												StimParam(Param.HEIGHT,
													ParamType.CONSTANT,
													200),
												StimParam(Param.RADIUS,
													ParamType.CONSTANT,
													100)
												], outcome=Outcome.SUCCESS),
								RandomStim([
												StimParam(Param.POSITION, 
													ParamType.CONSTANT, 
													[300, 0]),
												StimParam(Param.COLOR,
													ParamType.CONSTANT,
													red),
												StimParam(Param.WIDTH,
													ParamType.CONSTANT,
													200),
												StimParam(Param.HEIGHT,
													ParamType.CONSTANT,
													200),
												StimParam(Param.RADIUS,
													ParamType.CONSTANT,
													100)
												], shape_list, [P1], outcome=Outcome.FAIL)
							], [P2]
		)

		windows = [w1, w2, w3, w4, w5]
		return windows, params